from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class ToolDefinitionResponse(BaseModel):
    tool_id: str
    name: str
    description: str
    version: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    permission_level: str
    risk_level: str
    requires_approval: bool
    is_available: bool
    implementation_type: str  # local, external, simulated
    last_executed_at: Optional[datetime] = None


class ToolExecutionRequest(BaseModel):
    tool_name: str
    input_payload: Dict[str, Any]
    task_id: Optional[str] = None
    step_id: Optional[str] = None


class ToolExecutionResponse(BaseModel):
    id: str
    tool_name: str
    status: str  # SUCCESS, FAILURE
    duration_ms: int
    output_payload: Dict[str, Any]
    error_message: Optional[str] = None
    executed_at: datetime

    model_config = ConfigDict(from_attributes=True)
