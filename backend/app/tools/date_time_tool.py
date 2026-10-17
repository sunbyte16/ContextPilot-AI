from datetime import datetime, timezone
import dateutil.parser
from typing import Dict, Any, Optional
from app.tools.base import BaseTool


class DateTimeTool(BaseTool):
    tool_id = "date_time"
    name = "Date and Time Utility"
    description = "Provides server time, calculates date/time differences, and formats timestamps."
    version = "1.0.0"
    risk_level = "LOW"
    requires_approval = False
    implementation_type = "local"

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["current_time", "calculate_difference", "format_date"],
                    "description": "The date/time operation to perform"
                },
                "start_date": {
                    "type": "string",
                    "description": "ISO format date string for difference calculation"
                },
                "end_date": {
                    "type": "string",
                    "description": "ISO format date string for difference calculation"
                },
                "date_string": {
                    "type": "string",
                    "description": "Date string to format"
                },
                "format_pattern": {
                    "type": "string",
                    "description": "Target strftime format pattern (e.g. %Y-%m-%d %H:%M:%S)"
                }
            },
            "required": ["operation"]
        }

    def get_output_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "result": {"type": "object"},
                "operation": {"type": "string"}
            }
        }

    def execute(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        op = params.get("operation", "current_time")
        now = datetime.now(timezone.utc)

        if op == "current_time":
            return {
                "success": True,
                "operation": op,
                "result": {
                    "utc_iso": now.isoformat(),
                    "utc_formatted": now.strftime("%A, %B %d, %Y %H:%M:%S UTC"),
                    "unix_timestamp": int(now.timestamp()),
                    "year": now.year,
                    "month": now.month,
                    "day": now.day,
                    "weekday": now.strftime("%A")
                }
            }

        elif op == "calculate_difference":
            start_str = params.get("start_date")
            end_str = params.get("end_date")
            if not start_str or not end_str:
                raise ValueError("Both 'start_date' and 'end_date' are required for calculate_difference.")
            
            d1 = dateutil.parser.isoparse(start_str)
            d2 = dateutil.parser.isoparse(end_str)
            diff = d2 - d1
            total_seconds = diff.total_seconds()

            return {
                "success": True,
                "operation": op,
                "result": {
                    "days": diff.days,
                    "hours": total_seconds / 3600,
                    "minutes": total_seconds / 60,
                    "total_seconds": total_seconds,
                    "is_past": total_seconds < 0,
                    "human_readable": f"{abs(diff.days)} days and {int((abs(total_seconds) % 86400) // 3600)} hours"
                }
            }

        elif op == "format_date":
            date_str = params.get("date_string")
            pattern = params.get("format_pattern", "%Y-%m-%d %H:%M:%S")
            if not date_str:
                raise ValueError("'date_string' is required for format_date.")
            dt = dateutil.parser.parse(date_str)
            return {
                "success": True,
                "operation": op,
                "result": {
                    "formatted": dt.strftime(pattern),
                    "iso": dt.isoformat()
                }
            }

        else:
            raise ValueError(f"Unsupported operation: {op}")
