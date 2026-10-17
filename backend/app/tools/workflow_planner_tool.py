from typing import Dict, Any, Optional, List
from app.tools.base import BaseTool


class WorkflowPlannerTool(BaseTool):
    tool_id = "workflow_planner"
    name = "Workflow & Step Planner"
    description = "Decomposes complex natural-language objectives into ordered, tool-mapped task steps with risk analysis."
    version = "1.0.0"
    risk_level = "LOW"
    requires_approval = False
    implementation_type = "local"

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "objective": {
                    "type": "string",
                    "description": "High-level goal or objective to decompose into an execution plan"
                },
                "risk_tolerance": {
                    "type": "string",
                    "enum": ["conservative", "standard", "automated"],
                    "default": "standard"
                }
            },
            "required": ["objective"]
        }

    def get_output_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "plan_summary": {"type": "string"},
                "steps": {"type": "array"},
                "overall_risk": {"type": "string"},
                "estimated_steps_count": {"type": "integer"}
            }
        }

    def execute(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        objective = params.get("objective", "").strip()
        if not objective:
            raise ValueError("Parameter 'objective' cannot be empty.")

        obj_lower = objective.lower()
        steps = []
        overall_risk = "LOW"

        # Adaptive rule-based planning for deterministic reliability
        if "exam" in obj_lower or "study" in obj_lower or "curriculum" in obj_lower:
            steps = [
                {
                    "step_order": 1,
                    "description": f"Gather current timestamp and schedule study milestones for '{objective}'",
                    "tool_name": "date_time",
                    "tool_input": {"operation": "current_time"},
                    "expected_output": "Current server timestamp and date benchmarks",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 2,
                    "description": "Retrieve relevant reference documents and subject notes from knowledge base",
                    "tool_name": "knowledge_retriever",
                    "tool_input": {"query": objective, "top_k": 3},
                    "expected_output": "Citations and reference passages from uploaded materials",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 3,
                    "description": "Synthesize key exam topics, formulas, and critical review points",
                    "tool_name": "structured_summarizer",
                    "tool_input": {"text": f"Study plan outline for: {objective}", "max_takeaways": 5},
                    "expected_output": "Key takeaways and structured study syllabus",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 4,
                    "description": "Generate in-app study reminder notification for scheduled study blocks",
                    "tool_name": "notification_center",
                    "tool_input": {
                        "action": "create_notification",
                        "title": "Study Plan Created",
                        "message": f"Structured study plan for '{objective}' is ready for review.",
                        "notification_type": "INFO"
                    },
                    "expected_output": "In-app reminder notification created",
                    "risk_level": "LOW",
                    "requires_approval": False
                }
            ]
        elif "data" in obj_lower or "analyze" in obj_lower or "spend" in obj_lower or "calc" in obj_lower or "budget" in obj_lower:
            steps = [
                {
                    "step_order": 1,
                    "description": "Inspect and compute statistical aggregations on data payload",
                    "tool_name": "data_analysis",
                    "tool_input": {
                        "data_type": "json_array",
                        "records": [
                            {"category": "Compute", "amount": 420.50},
                            {"category": "Storage", "amount": 135.20},
                            {"category": "Network", "amount": 84.10},
                            {"category": "Database", "amount": 310.00}
                        ],
                        "value_field": "amount"
                    },
                    "expected_output": "Summary statistics (total, average, median, range)",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 2,
                    "description": "Compute growth projection ratio using safe calculator",
                    "tool_name": "safe_calculator",
                    "tool_input": {"expression": "(420.50 + 135.20 + 84.10 + 310.00) * 1.15"},
                    "expected_output": "Adjusted projected budget calculation",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 3,
                    "description": "Export structured financial analysis report to markdown",
                    "tool_name": "export_tool",
                    "tool_input": {
                        "format": "markdown",
                        "content_type": "analysis_report",
                        "title": f"Budget Analysis: {objective}"
                    },
                    "expected_output": "Export file ready for download",
                    "risk_level": "MEDIUM",
                    "requires_approval": True
                }
            ]
            overall_risk = "MEDIUM"
        else:
            # General comprehensive workflow
            steps = [
                {
                    "step_order": 1,
                    "description": "Initialize server clock and timeline context",
                    "tool_name": "date_time",
                    "tool_input": {"operation": "current_time"},
                    "expected_output": "Current execution timestamp",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 2,
                    "description": f"Query existing knowledge base for context regarding '{objective}'",
                    "tool_name": "knowledge_retriever",
                    "tool_input": {"query": objective, "top_k": 3},
                    "expected_output": "Relevant documents and background context",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 3,
                    "description": "Synthesize findings into an actionable delivery summary",
                    "tool_name": "structured_summarizer",
                    "tool_input": {"text": f"Deliverable summary for: {objective}", "max_takeaways": 4},
                    "expected_output": "Actionable takeaways and synthesis",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 4,
                    "description": "Publish task completion notification to user workspace",
                    "tool_name": "notification_center",
                    "tool_input": {
                        "action": "create_notification",
                        "title": "Workflow Completed",
                        "message": f"Execution finished for: '{objective}'",
                        "notification_type": "TASK_COMPLETED"
                    },
                    "expected_output": "Workspace alert notification created",
                    "risk_level": "LOW",
                    "requires_approval": False
                }
            ]

        return {
            "success": True,
            "plan_summary": f"Generated {len(steps)}-step execution plan for objective: '{objective}'",
            "steps": steps,
            "overall_risk": overall_risk,
            "estimated_steps_count": len(steps)
        }
