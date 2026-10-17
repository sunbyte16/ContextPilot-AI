import time
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.agents.providers.base import BaseLLMProvider


class LocalDemoProvider(BaseLLMProvider):
    provider_id = "local-demo"
    name = "Local Deterministic Agent Engine (Demo Mode)"

    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        context_memories: Optional[List[Dict[str, Any]]] = None,
        retrieved_documents: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        last_message = messages[-1]["content"] if messages else ""
        msg_lower = last_message.lower()

        citations = []
        is_plan_request = any(k in msg_lower for k in [
            "plan", "prepare", "workflow", "create a task", "analyze these",
            "summarize these documents", "schedule", "calculate", "budget"
        ])

        # If knowledge chunks were retrieved, build grounded citation response
        if retrieved_documents and len(retrieved_documents) > 0:
            doc_summaries = []
            for doc in retrieved_documents[:3]:
                citations.append({
                    "document_id": doc.get("document_id", ""),
                    "filename": doc.get("filename", "Document"),
                    "page_number": doc.get("page_number", 1),
                    "snippet": doc.get("snippet", "")[:250],
                    "relevance_score": doc.get("relevance_score", 0.9)
                })
                doc_summaries.append(f"According to **{doc.get('filename')}** (Page {doc.get('page_number', 1)}): \"{doc.get('snippet', '')[:180]}...\"")

            grounded_answer = (
                f"Based on your verified knowledge base documents:\n\n"
                + "\n\n".join(doc_summaries)
                + "\n\nI have cited the exact source passages above for your verification."
            )
            return {
                "content": grounded_answer,
                "intent": "grounded_qa",
                "is_plan_request": False,
                "citations": citations,
                "suggested_followups": [
                    "Can you summarize the main conclusions of this document?",
                    "Create a task plan based on these requirements",
                    "Search for other related topics in my documents"
                ]
            }

        # Intent: plan request
        if is_plan_request:
            content = (
                f"I've analyzed your objective: **\"{last_message}\"**.\n\n"
                "I have formulated a verified multi-step execution plan using our registered tools. "
                "You can inspect each step, verify the parameters and risk classifications, and approve "
                "consequential operations in the execution drawer."
            )
            return {
                "content": content,
                "intent": "plan_creation",
                "is_plan_request": True,
                "citations": [],
                "suggested_followups": [
                    "Review and approve pending steps",
                    "Execute the workflow now",
                    "Add an additional verification step"
                ]
            }

        # Conversational / informational
        memory_prefix = ""
        if context_memories:
            pinned = [m["title"] for m in context_memories if m.get("is_pinned")]
            if pinned:
                memory_prefix = f"*(Applied active memory context: {', '.join(pinned)})*\n\n"

        content = (
            f"{memory_prefix}Hello! I am your **ContextPilot AI** assistant. "
            "I can help you orchestrate multi-step workflows, query your documents, execute safe mathematical "
            "and analytical tools, and manage your tasks with strict human approval gates.\n\n"
            "Try asking me to:\n"
            "- *\"Prepare a study plan for my machine learning exam\"*\n"
            "- *\"Analyze quarterly cloud spend data and export report\"*\n"
            "- *\"Summarize my uploaded project documents\"*\n"
            "- *\"Calculate (14500 * 1.18) + sqrt(256)\"*"
        )

        return {
            "content": content,
            "intent": "chat",
            "is_plan_request": False,
            "citations": [],
            "suggested_followups": [
                "Prepare a study plan for my machine learning exam",
                "Analyze cloud spend data and export report",
                "How do human approval gates work in ContextPilot?"
            ]
        }

    def generate_plan(
        self,
        objective: str,
        available_tools: List[Dict[str, Any]],
        context_memories: Optional[List[Dict[str, Any]]] = None,
        retrieved_documents: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        obj_lower = objective.lower()

        # Build plan depending on content
        if "exam" in obj_lower or "study" in obj_lower:
            steps = [
                {
                    "step_order": 1,
                    "description": "Initialize server clock and timetable benchmarks",
                    "tool_name": "date_time",
                    "tool_input": {"operation": "current_time"},
                    "expected_output": "Server timestamp and reference calendar dates",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 2,
                    "description": f"Retrieve study materials and lecture notes regarding '{objective}'",
                    "tool_name": "knowledge_retriever",
                    "tool_input": {"query": objective, "top_k": 3},
                    "expected_output": "Relevant document chunks and citations",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 3,
                    "description": "Synthesize study curriculum into structured key takeaways",
                    "tool_name": "structured_summarizer",
                    "tool_input": {"text": f"Study curriculum syllabus for {objective}", "max_takeaways": 4},
                    "expected_output": "Concise key takeaways and review questions",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 4,
                    "description": "Export study plan checklist report to Markdown",
                    "tool_name": "export_tool",
                    "tool_input": {
                        "format": "markdown",
                        "content_type": "tasks_summary",
                        "title": f"Study Schedule: {objective}"
                    },
                    "expected_output": "Export file ready for download",
                    "risk_level": "MEDIUM",
                    "requires_approval": True  # Consequential approval gate
                }
            ]
            risk = "MEDIUM"
            complexity = "STANDARD"

        elif "data" in obj_lower or "spend" in obj_lower or "budget" in obj_lower or "calc" in obj_lower:
            steps = [
                {
                    "step_order": 1,
                    "description": "Compute statistical aggregation metrics on cost records",
                    "tool_name": "data_analysis",
                    "tool_input": {
                        "records": [
                            {"service": "AWS Bedrock", "cost": 312.40},
                            {"service": "Amazon S3", "cost": 48.20},
                            {"service": "EC2 Instances", "cost": 540.00},
                            {"service": "RDS Postgres", "cost": 210.80}
                        ],
                        "value_field": "cost",
                        "group_by_field": "service"
                    },
                    "expected_output": "Aggregated mean, median, sum, and variance metrics",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 2,
                    "description": "Evaluate 18% reserve margin projection using safe math",
                    "tool_name": "safe_calculator",
                    "tool_input": {"expression": "(312.40 + 48.20 + 540.00 + 210.80) * 1.18"},
                    "expected_output": "Exact projected reserve figure",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 3,
                    "description": "Dispatch financial audit alert to workspace notifications",
                    "tool_name": "notification_center",
                    "tool_input": {
                        "action": "create_notification",
                        "title": "Cloud Spend Analysis Completed",
                        "message": "Cost analysis has been compiled with verified formulas.",
                        "notification_type": "TASK_COMPLETED"
                    },
                    "expected_output": "Alert record created in workspace",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 4,
                    "description": "Generate financial executive summary export in JSON",
                    "tool_name": "export_tool",
                    "tool_input": {
                        "format": "json",
                        "content_type": "analysis_report",
                        "title": "Cloud Spend Audit 2026"
                    },
                    "expected_output": "Structured JSON download file",
                    "risk_level": "HIGH",
                    "requires_approval": True  # Strict approval gate
                }
            ]
            risk = "HIGH"
            complexity = "COMPLEX"

        else:
            steps = [
                {
                    "step_order": 1,
                    "description": "Record server execution start timestamp",
                    "tool_name": "date_time",
                    "tool_input": {"operation": "current_time"},
                    "expected_output": "Current server timestamp",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 2,
                    "description": f"Search knowledge base for background documents matching '{objective}'",
                    "tool_name": "knowledge_retriever",
                    "tool_input": {"query": objective, "top_k": 3},
                    "expected_output": "Knowledge context and citations",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 3,
                    "description": "Extract structured summary and actionable recommendations",
                    "tool_name": "structured_summarizer",
                    "tool_input": {"text": f"Execution roadmap for {objective}", "max_takeaways": 3},
                    "expected_output": "Action items and synthesis",
                    "risk_level": "LOW",
                    "requires_approval": False
                },
                {
                    "step_order": 4,
                    "description": "Publish completion alert to user notification center",
                    "tool_name": "notification_center",
                    "tool_input": {
                        "action": "create_notification",
                        "title": "Task Workflow Complete",
                        "message": f"Execution completed for: '{objective}'",
                        "notification_type": "TASK_COMPLETED"
                    },
                    "expected_output": "In-app notification created",
                    "risk_level": "LOW",
                    "requires_approval": False
                }
            ]
            risk = "LOW"
            complexity = "STANDARD"

        return {
            "objective": objective,
            "description": f"Agentic execution plan generated for: '{objective}'",
            "risk_level": risk,
            "estimated_complexity": complexity,
            "steps": steps
        }

    def test_connection(self) -> Dict[str, Any]:
        return {
            "status": "CONNECTED",
            "is_real": True,
            "provider": self.provider_id,
            "latency_ms": 1.2,
            "details": "Deterministic local demo provider is active and ready for offline execution without AWS credentials.",
            "last_checked": datetime.now(timezone.utc).isoformat()
        }
