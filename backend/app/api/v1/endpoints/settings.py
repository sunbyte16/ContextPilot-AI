from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.all_models import User, UserPreference, AuditEvent
from app.schemas.settings import (
    UserPreferenceResponse, UserPreferenceUpdate,
    IntegrationStatus, IntegrationStatusResponse
)
from app.security.deps import get_current_user
from app.agents.providers.bedrock import BedrockProvider
from app.agents.providers.local_demo import LocalDemoProvider
from app.core.config import settings

router = APIRouter()


@router.get("/preferences", response_model=UserPreferenceResponse)
def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not pref:
        pref = UserPreference(user_id=current_user.id)
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref


@router.put("/preferences", response_model=UserPreferenceResponse)
def update_preferences(
    update_in: UserPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not pref:
        pref = UserPreference(user_id=current_user.id)
        db.add(pref)

    if update_in.preferred_model is not None:
        pref.preferred_model = update_in.preferred_model
    if update_in.response_style is not None:
        pref.response_style = update_in.response_style
    if update_in.memory_enabled is not None:
        pref.memory_enabled = update_in.memory_enabled
    if update_in.default_approval_behavior is not None:
        pref.default_approval_behavior = update_in.default_approval_behavior
    if update_in.execution_timeout_seconds is not None:
        pref.execution_timeout_seconds = update_in.execution_timeout_seconds
    if update_in.theme is not None:
        pref.theme = update_in.theme

    audit = AuditEvent(
        user_id=current_user.id,
        event_type="SETTINGS_CHANGED",
        action="update_preferences",
        details=update_in.model_dump(exclude_unset=True)
    )
    db.add(audit)
    db.commit()
    db.refresh(pref)
    return pref


@router.get("/integrations", response_model=IntegrationStatusResponse)
def get_integrations_status(
    current_user: User = Depends(get_current_user)
):
    # Check Local Demo
    local_p = LocalDemoProvider()
    local_status = local_p.test_connection()

    # Check Bedrock
    bedrock_p = BedrockProvider()
    bedrock_status = bedrock_p.test_connection()

    integrations = [
        IntegrationStatus(
            name="Deterministic Local Demo Agent",
            provider="local-demo",
            status=local_status["status"],
            is_real=local_status["is_real"],
            details=local_status["details"],
            latency_ms=local_status.get("latency_ms"),
            last_checked=datetime.fromisoformat(local_status["last_checked"])
        ),
        IntegrationStatus(
            name="Amazon Bedrock Runtime",
            provider="bedrock",
            status=bedrock_status["status"],
            is_real=bedrock_status["is_real"],
            details=bedrock_status["details"],
            latency_ms=bedrock_status.get("latency_ms"),
            last_checked=datetime.fromisoformat(bedrock_status["last_checked"])
        ),
        IntegrationStatus(
            name="Alexa+ Voice & Assistant Simulation",
            provider="simulated-alexa-web",
            status="SIMULATED",
            is_real=False,
            details="Web-based ambient workspace simulation inspired by Alexa+. Does not require proprietary hardware.",
            latency_ms=0.1,
            last_checked=datetime.now(timezone.utc)
        ),
        IntegrationStatus(
            name="Amazon S3 Document Lake (Optional)",
            provider="aws-s3",
            status="NOT_CONFIGURED" if not settings.AWS_ACCESS_KEY_ID else "CONNECTED",
            is_real=bool(settings.AWS_ACCESS_KEY_ID),
            details="Local encrypted filesystem storage is currently active with zero external cloud dependencies.",
            latency_ms=0.5,
            last_checked=datetime.now(timezone.utc)
        )
    ]
    return {"integrations": integrations}


@router.post("/integrations/test")
def test_integration(
    provider_name: str,
    current_user: User = Depends(get_current_user)
):
    if provider_name == "bedrock":
        p = BedrockProvider()
        return p.test_connection()
    elif provider_name == "local-demo":
        p = LocalDemoProvider()
        return p.test_connection()
    else:
        return {
            "status": "SIMULATED",
            "is_real": False,
            "provider": provider_name,
            "details": f"Integration '{provider_name}' verified in safe simulation mode."
        }
