from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.tools.base import BaseTool
from app.models.all_models import Task, TaskStep, User


class TaskManagerTool(BaseTool):
    tool_id = "task_manager"
    name = "Task Manager Utility"
    description = "Manages user tasks, retrieves status, updates priorities, or marks tasks completed."
    version = "1.0.0"
    risk_level = "MEDIUM"
    requires_approval = False
    implementation_type = "local"

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["list_tasks", "get_task", "create_task", "update_task_status"],
                    "description": "The task management action to perform"
                },
                "task_id": {
                    "type": "string",
                    "description": "ID of the target task (for get_task or update_task_status)"
                },
                "objective": {
                    "type": "string",
                    "description": "Objective for a newly created task"
                },
                "priority": {
                    "type": "string",
                    "enum": ["LOW", "MEDIUM", "HIGH", "URGENT"],
                    "description": "Task priority level"
                },
                "status": {
                    "type": "string",
                    "enum": ["DRAFT", "AWAITING_APPROVAL", "APPROVED", "RUNNING", "COMPLETED", "FAILED", "CANCELLED"],
                    "description": "New status for update_task_status"
                }
            },
            "required": ["action"]
        }

    def get_output_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "action": {"type": "string"},
                "data": {"type": "object"}
            }
        }

    def execute(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        action = params.get("action")
        db = context.get("db") if context else None
        user = context.get("user") if context else None

        if not db or not user:
            raise ValueError("Database and user context are required for TaskManagerTool.")

        if action == "list_tasks":
            tasks = db.query(Task).filter(Task.user_id == user.id).order_by(Task.created_at.desc()).limit(10).all()
            return {
                "success": True,
                "action": action,
                "data": {
                    "count": len(tasks),
                    "tasks": [
                        {
                            "id": t.id,
                            "objective": t.objective,
                            "status": t.status,
                            "priority": t.priority,
                            "progress": t.progress,
                            "created_at": t.created_at.isoformat() if t.created_at else None
                        }
                        for t in tasks
                    ]
                }
            }

        elif action == "get_task":
            task_id = params.get("task_id")
            if not task_id:
                raise ValueError("task_id is required for get_task")
            t = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
            if not t:
                raise ValueError(f"Task with ID {task_id} not found")
            return {
                "success": True,
                "action": action,
                "data": {
                    "id": t.id,
                    "objective": t.objective,
                    "status": t.status,
                    "priority": t.priority,
                    "progress": t.progress,
                    "step_count": len(t.steps) if t.steps else 0
                }
            }

        elif action == "create_task":
            obj = params.get("objective")
            if not obj:
                raise ValueError("objective is required for create_task")
            prio = params.get("priority", "MEDIUM")
            new_task = Task(
                user_id=user.id,
                objective=obj,
                priority=prio,
                status="DRAFT"
            )
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
            return {
                "success": True,
                "action": action,
                "data": {
                    "id": new_task.id,
                    "objective": new_task.objective,
                    "status": new_task.status,
                    "priority": new_task.priority
                }
            }

        elif action == "update_task_status":
            task_id = params.get("task_id")
            new_status = params.get("status")
            if not task_id or not new_status:
                raise ValueError("Both task_id and status are required for update_task_status")
            t = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
            if not t:
                raise ValueError(f"Task {task_id} not found")
            t.status = new_status
            if new_status == "COMPLETED":
                t.progress = 100
                t.completed_at = datetime.now(timezone.utc)
            db.commit()
            return {
                "success": True,
                "action": action,
                "data": {
                    "id": t.id,
                    "status": t.status,
                    "progress": t.progress
                }
            }

        else:
            raise ValueError(f"Unsupported action: {action}")
