from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.all_models import User, UserPreference, AuditEvent
from app.schemas.auth import UserCreate, UserLogin, UserResponse, UserUpdate, Token
from app.security.password import get_password_hash, verify_password
from app.security.jwt import create_access_token
from app.security.deps import get_current_user
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize default preferences
    pref = UserPreference(
        user_id=new_user.id,
        preferred_model="local-demo",
        response_style="precise",
        theme="dark"
    )
    db.add(pref)

    # Audit log
    audit = AuditEvent(
        user_id=new_user.id,
        event_type="AUTH_REGISTER",
        action="user_registered",
        details={"email": new_user.email}
    )
    db.add(audit)
    db.commit()

    return new_user


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is disabled.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user.id, expires_delta=access_token_expires)

    # Set secure HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False  # Allow local http testing
    )

    # Audit
    audit = AuditEvent(
        user_id=user.id,
        event_type="AUTH_LOGIN",
        action="user_logged_in",
        details={"email": user.email}
    )
    db.add(audit)
    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }


@router.post("/logout")
def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out."}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name
    if update_data.email is not None and update_data.email != current_user.email:
        existing = db.query(User).filter(User.email == update_data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email is already in use.")
        current_user.email = update_data.email

    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me")
def delete_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    response: Response = None
):
    db.delete(current_user)
    db.commit()
    if response:
        response.delete_cookie("access_token")
    return {"message": "Account and associated data deleted successfully."}
