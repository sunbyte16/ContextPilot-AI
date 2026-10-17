from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.all_models import User
from app.schemas.tool import ToolDefinitionResponse, ToolExecutionRequest, ToolExecutionResponse
from app.security.deps import get_current_user
from app.tools.registry import tool_registry

router = APIRouter()


@router.get("/", response_model=List[ToolDefinitionResponse])
def list_tools(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return tool_registry.list_tools(db=db)


@router.post("/execute", response_model=ToolExecutionResponse)
def execute_tool_endpoint(
    req: ToolExecutionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tool = tool_registry.get_tool(req.tool_name)
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool '{req.tool_name}' not found."
        )

    # If the tool requires approval and this is a direct execution, verify permission
    if tool.requires_approval and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Tool '{tool.name}' requires execution within an approved task workflow."
        )

    try:
        res = tool_registry.dispatch(
            tool_id=req.tool_name,
            params=req.input_payload,
            user=current_user,
            db=db,
            task_id=req.task_id,
            step_id=req.step_id,
            is_approved=True
        )
        return {
            "id": res["execution_id"],
            "tool_name": res["tool_id"],
            "status": res["status"],
            "duration_ms": res["duration_ms"],
            "output_payload": res["output"],
            "error_message": res.get("error"),
            "executed_at": res["executed_at"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
