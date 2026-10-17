from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender: str  # user, assistant, system
    content: str
    msg_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    is_archived: Optional[bool] = None


class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)


class ConversationDetailResponse(ConversationResponse):
    messages: List[MessageResponse] = []
