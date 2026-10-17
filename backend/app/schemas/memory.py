from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class MemoryCreate(BaseModel):
    category: str = Field(default="FACT", description="FACT, PREFERENCE, PROJECT_CONTEXT, NOTE, TASK_OUTCOME")
    title: str = Field(..., max_length=255)
    content: str
    source_reference: Optional[str] = None
    is_pinned: Optional[bool] = False


class MemoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    is_pinned: Optional[bool] = None


class MemoryResponse(BaseModel):
    id: str
    user_id: str
    category: str
    title: str
    content: str
    confidence_score: float
    source_reference: Optional[str] = None
    is_pinned: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
