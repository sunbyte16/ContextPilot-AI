import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.all_models import ToolExecution, AuditEvent, User
from app.tools.base import BaseTool
from app.tools.date_time_tool import DateTimeTool
from app.tools.safe_calculator import SafeCalculatorTool
from app.tools.task_manager_tool import TaskManagerTool
from app.tools.knowledge_retriever_tool import KnowledgeRetrieverTool
from app.tools.structured_summarizer_tool import StructuredSummarizerTool
from app.tools.workflow_planner_tool import WorkflowPlannerTool
from app.tools.data_analysis_tool import DataAnalysisTool
from app.tools.notification_tool import NotificationCenterTool
from app.tools.export_tool import ExportTool


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        tools: List[BaseTool] = [
            DateTimeTool(),
            SafeCalculatorTool(),
            TaskManagerTool(),
            KnowledgeRetrieverTool(),
            StructuredSummarizerTool(),
            WorkflowPlannerTool(),
            DataAnalysisTool(),
            NotificationCenterTool(),
            ExportTool(),
        ]
        for t in tools:
            self._tools[t.tool_id] = t

    def get_tool(self, tool_id: str) -> Optional[BaseTool]:
        return self._tools.get(tool_id)

    def list_tools(self, db: Optional[Session] = None) -> List[Dict[str, Any]]:
        result = []
        for tool_id, tool in self._tools.items():
            last_exec = None
            if db:
                last_record = db.query(ToolExecution).filter(
                    ToolExecution.tool_name == tool_id
                ).order_by(ToolExecution.executed_at.desc()).first()
                if last_record:
                    last_exec = last_record.executed_at
            result.append(tool.to_metadata(last_executed_at=last_exec))
        return result

    def dispatch(
        self,
        tool_id: str,
        params: Dict[str, Any],
        user: User,
        db: Session,
        task_id: Optional[str] = None,
        step_id: Optional[str] = None,
        is_approved: bool = False
    ) -> Dict[str, Any]:
        """Controlled, audited tool execution dispatcher."""
        tool = self.get_tool(tool_id)
        if not tool:
            raise ValueError(f"Tool '{tool_id}' is not registered in the system.")

        # Server-side safety gate: check approval requirement
        if tool.requires_approval and not is_approved:
            raise PermissionError(f"Tool '{tool.name}' requires explicit human approval before execution.")

        context = {
            "user": user,
            "db": db,
            "task_id": task_id,
            "step_id": step_id,
        }

        start_time = time.time()
        status = "SUCCESS"
        error_msg = None
        result_payload = {}

        try:
            result_payload = tool.execute(params, context=context)
        except Exception as e:
            status = "FAILURE"
            error_msg = str(e)
            result_payload = {
                "success": False,
                "error": error_msg,
                "tool_id": tool_id
            }

        duration_ms = int((time.time() - start_time) * 1000)

        # Sanitize parameters for storage (redact any sensitive keys)
        sanitized_input = self._sanitize_payload(params)

        # Record persistent ToolExecution
        tool_exec = ToolExecution(
            user_id=user.id,
            task_id=task_id,
            step_id=step_id,
            tool_name=tool_id,
            input_payload=sanitized_input,
            output_payload=result_payload,
            status=status,
            duration_ms=duration_ms,
            error_message=error_msg,
            executed_at=datetime.now(timezone.utc)
        )
        db.add(tool_exec)

        # Record AuditEvent
        audit = AuditEvent(
            user_id=user.id,
            event_type="TOOL_EXECUTED",
            resource_type="tool",
            resource_id=tool_id,
            action=f"execute_{tool_id}",
            details={
                "status": status,
                "duration_ms": duration_ms,
                "task_id": task_id,
                "step_id": step_id
            }
        )
        db.add(audit)
        db.commit()
        db.refresh(tool_exec)

        return {
            "execution_id": tool_exec.id,
            "tool_id": tool_id,
            "status": status,
            "duration_ms": duration_ms,
            "output": result_payload,
            "error": error_msg,
            "executed_at": tool_exec.executed_at.isoformat()
        }

    def _sanitize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            return {"payload": str(payload)}
        sanitized = {}
        sensitive_keys = {"password", "secret", "token", "api_key", "authorization", "credential"}
        for k, v in payload.items():
            if any(s in k.lower() for s in sensitive_keys):
                sanitized[k] = "******[REDACTED]******"
            elif isinstance(v, dict):
                sanitized[k] = self._sanitize_payload(v)
            else:
                sanitized[k] = v
        return sanitized


tool_registry = ToolRegistry()
