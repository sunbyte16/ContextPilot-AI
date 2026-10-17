from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class UserPreferenceUpdate(BaseModel):
    preferred_model: Optional[str] = None
    response_style: Optional[str] = None
    memory_enabled: Optional[bool] = None
    default_approval_behavior: Optional[str] = None
    execution_timeout_seconds: Optional[int] = None
    theme: Optional[str] = None


class UserPreferenceResponse(BaseModel):
    preferred_model: str
    response_style: str
    memory_enabled: bool
    default_approval_behavior: str
    execution_timeout_seconds: int
    theme: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IntegrationStatus(BaseModel):
    name: str
    provider: str
    status: str  # CONNECTED, SIMULATED, NOT_CONFIGURED, ERROR
    is_real: bool
    details: str
    latency_ms: Optional[float] = None
    last_checked: datetime


class IntegrationStatusResponse(BaseModel):
    integrations: List[IntegrationStatus]
