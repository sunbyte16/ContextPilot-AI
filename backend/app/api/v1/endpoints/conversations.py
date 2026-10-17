from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.all_models import User, Conversation, Message
from app.schemas.conversation import (
    ConversationResponse, ConversationDetailResponse,
    ConversationCreate, ConversationUpdate, MessageCreate
)
from app.security.deps import get_current_user
from app.agents.orchestrator import orchestrator

router = APIRouter()


@router.get("/", response_model=List[ConversationResponse])
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    convs = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.updated_at.desc()).all()

    result = []
    for c in convs:
        count = db.query(Message).filter(Message.conversation_id == c.id).count()
        result.append({
            "id": c.id,
            "user_id": c.user_id,
            "title": c.title,
            "is_archived": c.is_archived,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
            "message_count": count
        })
    return result


@router.post("/", response_model=ConversationResponse)
def create_conversation(
    conv_in: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = Conversation(
        user_id=current_user.id,
        title=conv_in.title or "New Conversation"
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return {
        "id": conv.id,
        "user_id": conv.user_id,
        "title": conv.title,
        "is_archived": conv.is_archived,
        "created_at": conv.created_at,
        "updated_at": conv.updated_at,
        "message_count": 0
    }


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = db.query(Message).filter(
        Message.conversation_id == conv.id
    ).order_by(Message.created_at.asc()).all()

    return {
        "id": conv.id,
        "user_id": conv.user_id,
        "title": conv.title,
        "is_archived": conv.is_archived,
        "created_at": conv.created_at,
        "updated_at": conv.updated_at,
        "message_count": len(messages),
        "messages": messages
    }


@router.put("/{conversation_id}", response_model=ConversationResponse)
def update_conversation(
    conversation_id: str,
    update_data: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if update_data.title is not None:
        conv.title = update_data.title
    if update_data.is_archived is not None:
        conv.is_archived = update_data.is_archived

    db.commit()
    db.refresh(conv)
    return {
        "id": conv.id,
        "user_id": conv.user_id,
        "title": conv.title,
        "is_archived": conv.is_archived,
        "created_at": conv.created_at,
        "updated_at": conv.updated_at,
        "message_count": len(conv.messages)
    }


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.delete(conv)
    db.commit()
    return {"message": "Conversation deleted successfully"}


@router.post("/{conversation_id}/messages")
def send_message(
    conversation_id: str,
    msg_in: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = orchestrator.process_user_message(
        user=current_user,
        db=db,
        content=msg_in.content,
        conversation_id=conversation_id
    )
    return result
