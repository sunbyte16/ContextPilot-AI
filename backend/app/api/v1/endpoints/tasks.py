from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.all_models import (
    User, Task, TaskStep, ApprovalRequest, ExecutionEvent, AuditEvent
)
from app.schemas.task import (
    TaskResponse, TaskDetailResponse, TaskCreate, TaskUpdate,
    ApprovalDecisionRequest, ApprovalRequestResponse
)
from app.schemas.audit import ExecutionEventResponse
from app.security.deps import get_current_user
from app.agents.orchestrator import orchestrator
from app.tools.registry import tool_registry
from app.agents.providers.factory import get_llm_provider

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    status_filter: Optional[str] = Query(None, alias="status"),
    priority_filter: Optional[str] = Query(None, alias="priority"),
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    if status_filter:
        query = query.filter(Task.status == status_filter.upper())
    if priority_filter:
        query = query.filter(Task.priority == priority_filter.upper())
    if search:
        query = query.filter(Task.objective.ilike(f"%{search}%"))

    tasks = query.order_by(Task.created_at.desc()).all()
    result = []
    for t in tasks:
        step_count = len(t.steps) if t.steps else 0
        t_dict = {
            "id": t.id,
            "user_id": t.user_id,
            "conversation_id": t.conversation_id,
            "objective": t.objective,
            "description": t.description,
            "status": t.status,
            "risk_level": t.risk_level,
            "priority": t.priority,
            "progress": t.progress,
            "estimated_complexity": t.estimated_complexity,
            "result_summary": t.result_summary,
            "error_message": t.error_message,
            "created_at": t.created_at,
            "updated_at": t.updated_at,
            "completed_at": t.completed_at,
            "step_count": step_count
        }
        result.append(t_dict)
    return result


@router.post("/", response_model=TaskDetailResponse)
def create_task_plan(
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    provider = get_llm_provider(current_user.preference.preferred_model if current_user.preference else None)
    available_tools = tool_registry.list_tools(db=db)
    
    plan_data = provider.generate_plan(
        objective=task_in.objective,
        available_tools=available_tools
    )

    task = Task(
        user_id=current_user.id,
        conversation_id=task_in.conversation_id,
        objective=task_in.objective,
        description=plan_data.get("description", f"Plan for: {task_in.objective}"),
        status="DRAFT",
        risk_level=plan_data.get("risk_level", "LOW"),
        priority=task_in.priority or "MEDIUM",
        estimated_complexity=plan_data.get("estimated_complexity", "STANDARD"),
        progress=0
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    has_approval_gate = False
    for step_spec in plan_data.get("steps", []):
        step = TaskStep(
            task_id=task.id,
            step_order=step_spec["step_order"],
            description=step_spec["description"],
            tool_name=step_spec.get("tool_name"),
            tool_input=step_spec.get("tool_input", {}),
            expected_output=step_spec.get("expected_output"),
            status="PENDING",
            risk_level=step_spec.get("risk_level", "LOW"),
            requires_approval=step_spec.get("requires_approval", False)
        )
        db.add(step)
        db.commit()
        db.refresh(step)

        if step.requires_approval or step.risk_level in ["HIGH", "CRITICAL"]:
            has_approval_gate = True
            appr = ApprovalRequest(
                task_id=task.id,
                step_id=step.id,
                user_id=current_user.id,
                action_name=f"Execute {step.tool_name or 'step'}",
                action_purpose=step.description,
                target_resource=step.tool_name,
                parameters_summary=step.tool_input,
                risk_level=step.risk_level,
                status="PENDING"
            )
            db.add(appr)

    task.status = "AWAITING_APPROVAL" if has_approval_gate else "APPROVED"
    event = ExecutionEvent(
        task_id=task.id,
        event_type="PLAN_GENERATED",
        message=f"Plan generated with {len(plan_data.get('steps', []))} steps. Status: {task.status}",
        payload={"steps_count": len(plan_data.get("steps", []))}
    )
    db.add(event)
    db.commit()
    db.refresh(task)

    return task


@router.get("/{task_id}", response_model=TaskDetailResponse)
def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskDetailResponse)
def update_task(
    task_id: str,
    update_in: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if update_in.objective is not None:
        task.objective = update_in.objective
    if update_in.priority is not None:
        task.priority = update_in.priority
    if update_in.status is not None:
        task.status = update_in.status

    db.commit()
    db.refresh(task)
    return task


@router.post("/{task_id}/execute")
def execute_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return orchestrator.execute_task(task_id, current_user, db)


@router.post("/{task_id}/cancel")
def cancel_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = "CANCELLED"
    event = ExecutionEvent(
        task_id=task.id,
        event_type="TASK_CANCELLED",
        message="Task execution was explicitly cancelled by the user.",
        payload={}
    )
    db.add(event)
    db.commit()
    return {"message": "Task cancelled successfully", "status": "CANCELLED"}


@router.post("/{task_id}/retry")
def retry_failed_step(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Reset any failed steps to PENDING
    failed_steps = db.query(TaskStep).filter(
        TaskStep.task_id == task_id,
        TaskStep.status == "FAILED"
    ).all()

    for s in failed_steps:
        s.status = "PENDING"
        s.error_message = None
        s.retry_count += 1

    task.status = "RUNNING"
    task.error_message = None
    db.commit()

    return orchestrator.execute_task(task_id, current_user, db)


@router.post("/{task_id}/approvals/{approval_id}")
def decide_approval(
    task_id: str,
    approval_id: str,
    decision_in: ApprovalDecisionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return orchestrator.handle_approval_decision(
        task_id=task_id,
        approval_id=approval_id,
        approved=decision_in.approved,
        decision_notes=decision_in.decision_notes,
        user=current_user,
        db=db
    )


@router.get("/{task_id}/events", response_model=List[ExecutionEventResponse])
def get_task_events(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    events = db.query(ExecutionEvent).filter(
        ExecutionEvent.task_id == task_id
    ).order_by(ExecutionEvent.created_at.asc()).all()

    return events
