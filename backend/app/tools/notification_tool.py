from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.tools.base import BaseTool
from app.models.all_models import Notification


class NotificationCenterTool(BaseTool):
    tool_id = "notification_center"
    name = "In-App Notification Center"
    description = "Dispatches workspace notifications, alerts for required approvals, and marks alerts read."
    version = "1.0.0"
    risk_level = "LOW"
    requires_approval = False
    implementation_type = "local"

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["create_notification", "list_notifications", "mark_all_read"],
                    "description": "Notification action to perform"
                },
                "title": {
                    "type": "string",
                    "description": "Alert title"
                },
                "message": {
                    "type": "string",
                    "description": "Alert message body"
                },
                "notification_type": {
                    "type": "string",
                    "enum": ["INFO", "APPROVAL_REQUIRED", "TASK_COMPLETED", "TASK_FAILED"],
                    "default": "INFO"
                },
                "link_url": {
                    "type": "string",
                    "description": "Target UI link for notification click"
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
        action = params.get("action", "create_notification")
        db = context.get("db") if context else None
        user = context.get("user") if context else None

        if not db or not user:
            raise ValueError("Database and user context required for NotificationCenterTool.")

        if action == "create_notification":
            title = params.get("title", "Workspace Notification")
            message = params.get("message", "")
            ntype = params.get("notification_type", "INFO")
            link_url = params.get("link_url", "/app/activity")

            notif = Notification(
                user_id=user.id,
                title=title,
                message=message,
                notification_type=ntype,
                link_url=link_url,
                is_read=False
            )
            db.add(notif)
            db.commit()
            db.refresh(notif)
            return {
                "success": True,
                "action": action,
                "data": {
                    "notification_id": notif.id,
                    "title": notif.title,
                    "type": notif.notification_type,
                    "created_at": notif.created_at.isoformat()
                }
            }

        elif action == "list_notifications":
            items = db.query(Notification).filter(Notification.user_id == user.id).order_by(Notification.created_at.desc()).limit(15).all()
            return {
                "success": True,
                "action": action,
                "data": {
                    "count": len(items),
                    "notifications": [
                        {
                            "id": n.id,
                            "title": n.title,
                            "message": n.message,
                            "type": n.notification_type,
                            "is_read": n.is_read,
                            "link_url": n.link_url,
                            "created_at": n.created_at.isoformat()
                        }
                        for n in items
                    ]
                }
            }

        elif action == "mark_all_read":
            db.query(Notification).filter(Notification.user_id == user.id, Notification.is_read == False).update({"is_read": True})
            db.commit()
            return {
                "success": True,
                "action": action,
                "data": {"message": "All notifications marked as read"}
            }

        else:
            raise ValueError(f"Unsupported action: {action}")
