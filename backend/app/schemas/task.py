from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict


class TaskStepCreate(BaseModel):
    step_order: int
    description: str
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    expected_output: Optional[str] = None
    risk_level: Optional[str] = "LOW"
    requires_approval: Optional[bool] = False


class TaskStepResponse(BaseModel):
    id: str
    task_id: str
    step_order: int
    description: str
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    expected_output: Optional[str] = None
    actual_output: Optional[Dict[str, Any]] = None
    status: str
    risk_level: str
    requires_approval: bool
    retry_count: int
    max_retries: int
    execution_time_ms: int
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ApprovalRequestResponse(BaseModel):
    id: str
    task_id: str
    step_id: Optional[str] = None
    action_name: str
    action_purpose: str
    target_resource: Optional[str] = None
    parameters_summary: Optional[Dict[str, Any]] = None
    risk_level: str
    status: str
    decision_notes: Optional[str] = None
    requested_at: datetime
    decided_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ApprovalDecisionRequest(BaseModel):
    approved: bool
    decision_notes: Optional[str] = None


class TaskCreate(BaseModel):
    objective: str
    conversation_id: Optional[str] = None
    priority: Optional[str] = "MEDIUM"


class TaskUpdate(BaseModel):
    objective: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class TaskResponse(BaseModel):
    id: str
    user_id: str
    conversation_id: Optional[str] = None
    objective: str
    description: Optional[str] = None
    status: str
    risk_level: str
    priority: str
    progress: int
    estimated_complexity: str
    result_summary: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    step_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)


class TaskDetailResponse(TaskResponse):
    steps: List[TaskStepResponse] = []
    approvals: List[ApprovalRequestResponse] = []
