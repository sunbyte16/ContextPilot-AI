import os
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.all_models import (
    User, Conversation, Message, Task, TaskStep, ApprovalRequest,
    ExecutionEvent, AuditEvent, Memory, KnowledgeDocument, DocumentChunk, Notification
)
from app.security.deps import get_current_user
from app.knowledge.document_processor import process_document

router = APIRouter()


@router.post("/seed")
def seed_demo_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Seed Conversation
    conv = Conversation(
        user_id=current_user.id,
        title="Welcome & Quickstart"
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)

    msg1 = Message(
        conversation_id=conv.id,
        sender="user",
        content="Prepare a study plan for my machine learning exam."
    )
    msg2 = Message(
        conversation_id=conv.id,
        sender="assistant",
        content="I've analyzed your objective and drafted a 4-step execution plan using registered tools: Date/Time utility, Knowledge Retriever, Structured Summarizer, and Report Exporter. Please inspect the planned steps in the Task Monitor.",
        msg_metadata={"intent": "plan_creation", "citations": []}
    )
    db.add(msg1)
    db.add(msg2)

    # 2. Seed Completed Task
    task1 = Task(
        user_id=current_user.id,
        conversation_id=conv.id,
        objective="Prepare study plan for Machine Learning exam",
        description="Comprehensive 4-step syllabus breakdown and schedule benchmarks.",
        status="COMPLETED",
        risk_level="MEDIUM",
        priority="HIGH",
        progress=100,
        estimated_complexity="STANDARD",
        result_summary="All 4 plan steps executed and verified successfully. Completed tools: date_time, knowledge_retriever, structured_summarizer, export_tool.",
        completed_at=datetime.now(timezone.utc)
    )
    db.add(task1)
    db.commit()
    db.refresh(task1)

    step1 = TaskStep(
        task_id=task1.id,
        step_order=1,
        description="Initialize server clock and schedule milestones",
        tool_name="date_time",
        tool_input={"operation": "current_time"},
        expected_output="Current server timestamp",
        actual_output={"utc_iso": datetime.now(timezone.utc).isoformat(), "weekday": "Thursday"},
        status="COMPLETED",
        risk_level="LOW",
        execution_time_ms=12
    )
    step2 = TaskStep(
        task_id=task1.id,
        step_order=2,
        description="Retrieve core ML concepts and model architectures from knowledge base",
        tool_name="knowledge_retriever",
        tool_input={"query": "machine learning exam", "top_k": 3},
        expected_output="Verified study citations",
        actual_output={"citations_found": 3, "top_match": "Supervised Learning Fundamentals"},
        status="COMPLETED",
        risk_level="LOW",
        execution_time_ms=45
    )
    step3 = TaskStep(
        task_id=task1.id,
        step_order=3,
        description="Synthesize key exam topics into structured takeaways",
        tool_name="structured_summarizer",
        tool_input={"text": "Machine learning study curriculum", "max_takeaways": 4},
        expected_output="Synthesized takeaways",
        actual_output={"takeaways_count": 4, "executive_summary": "Core topics: Loss functions, Optimization, Transformers"},
        status="COMPLETED",
        risk_level="LOW",
        execution_time_ms=28
    )
    step4 = TaskStep(
        task_id=task1.id,
        step_order=4,
        description="Export study checklist to Markdown",
        tool_name="export_tool",
        tool_input={"format": "markdown", "title": "ML Exam Plan"},
        expected_output="Downloadable report",
        actual_output={"filename": "ml_exam_plan.md", "size_bytes": 1420},
        status="COMPLETED",
        risk_level="MEDIUM",
        requires_approval=True,
        execution_time_ms=56
    )
    db.add_all([step1, step2, step3, step4])

    # 3. Seed Task Awaiting Approval
    task2 = Task(
        user_id=current_user.id,
        objective="Analyze quarterly cloud spend and export financial audit",
        description="Calculates AWS and infrastructure costs with safe math and exports a sensitive audit report.",
        status="AWAITING_APPROVAL",
        risk_level="HIGH",
        priority="HIGH",
        progress=50,
        estimated_complexity="COMPLEX"
    )
    db.add(task2)
    db.commit()
    db.refresh(task2)

    t2_step1 = TaskStep(
        task_id=task2.id,
        step_order=1,
        description="Compute statistical metrics across cloud services",
        tool_name="data_analysis",
        tool_input={"records": [{"service": "Bedrock", "cost": 312.40}, {"service": "S3", "cost": 48.20}], "value_field": "cost"},
        actual_output={"count": 2, "sum": 360.60, "mean": 180.30},
        status="COMPLETED",
        risk_level="LOW",
        execution_time_ms=22
    )
    t2_step2 = TaskStep(
        task_id=task2.id,
        step_order=2,
        description="Compute 18% reserve margin with safe calculator",
        tool_name="safe_calculator",
        tool_input={"expression": "360.60 * 1.18"},
        actual_output={"result": 425.508, "formatted": "425.508"},
        status="COMPLETED",
        risk_level="LOW",
        execution_time_ms=10
    )
    t2_step3 = TaskStep(
        task_id=task2.id,
        step_order=3,
        description="Generate external financial executive audit report in JSON",
        tool_name="export_tool",
        tool_input={"format": "json", "content_type": "analysis_report", "title": "Quarterly Cloud Spend 2026"},
        expected_output="JSON audit artifact",
        status="AWAITING_APPROVAL",
        risk_level="HIGH",
        requires_approval=True
    )
    db.add_all([t2_step1, t2_step2, t2_step3])
    db.commit()

    # Approval Request for t2_step3
    appr = ApprovalRequest(
        task_id=task2.id,
        step_id=t2_step3.id,
        user_id=current_user.id,
        action_name="Export Financial Audit Report (JSON)",
        action_purpose="Generates and packages financial cloud expenditure metrics into a downloadable JSON file.",
        target_resource="export_tool",
        parameters_summary={"format": "json", "title": "Quarterly Cloud Spend 2026"},
        risk_level="HIGH",
        status="PENDING"
    )
    db.add(appr)

    # 4. Seed Knowledge Document
    sample_doc_content = """# Amazon Bedrock and Agentic AI Architecture

## 1. Overview
Amazon Bedrock provides fully managed access to foundational models (FMs) through a unified API. In ContextPilot AI, Amazon Bedrock powers natural-language reasoning, multi-step plan generation, and contextual intent detection.

## 2. Guardrails and Safety Policies
All model calls adhere to strict human-in-the-loop validation:
- Read-only operations (such as calculating formulas or querying local time) can execute safely.
- Consequential actions (such as generating external reports, deleting data, or dispatching external notifications) require explicit human approval.

## 3. Grounded Retrieval
When users ask domain-specific questions, ContextPilot AI retrieves indexed passages, checks for evidence sufficiency, and includes verbatim source citations with page numbers. If no relevant evidence exists in the indexed documents, the agent explicitly discloses insufficient evidence.
"""
    doc = KnowledgeDocument(
        user_id=current_user.id,
        filename="Amazon_Bedrock_Agent_Guide.md",
        file_type="md",
        file_size_bytes=len(sample_doc_content.encode("utf-8")),
        storage_path="sample_data/Amazon_Bedrock_Agent_Guide.md",
        processing_status="INDEXED",
        chunk_count=3
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    c1 = DocumentChunk(
        document_id=doc.id,
        chunk_index=0,
        page_number=1,
        content="Amazon Bedrock provides fully managed access to foundational models (FMs) through a unified API. In ContextPilot AI, Amazon Bedrock powers natural-language reasoning and multi-step planning.",
        chunk_metadata={"source": "Amazon_Bedrock_Agent_Guide.md", "page": 1}
    )
    c2 = DocumentChunk(
        document_id=doc.id,
        chunk_index=1,
        page_number=2,
        content="All model calls adhere to strict human-in-the-loop validation: Read-only operations execute safely, whereas consequential actions require explicit human approval.",
        chunk_metadata={"source": "Amazon_Bedrock_Agent_Guide.md", "page": 2}
    )
    c3 = DocumentChunk(
        document_id=doc.id,
        chunk_index=2,
        page_number=3,
        content="When users ask domain-specific questions, ContextPilot AI retrieves indexed passages and includes verbatim citations. If evidence is lacking, it explicitly states insufficient evidence.",
        chunk_metadata={"source": "Amazon_Bedrock_Agent_Guide.md", "page": 3}
    )
    db.add_all([c1, c2, c3])

    # 5. Seed Memories
    mem1 = Memory(
        user_id=current_user.id,
        category="FACT",
        title="Upcoming Machine Learning Exam Date",
        content="Exam scheduled for December 15, 2026. Focus areas: Transformers, Loss functions, and Evaluation metrics.",
        is_pinned=True
    )
    mem2 = Memory(
        user_id=current_user.id,
        category="PREFERENCE",
        title="Cloud Budget Cap",
        content="Monthly cloud infrastructure budget cap is $1,500.00. Notify if projected expenses exceed 85%.",
        is_pinned=True
    )
    mem3 = Memory(
        user_id=current_user.id,
        category="NOTE",
        title="Preferred Report Format",
        content="Default to GitHub-flavored Markdown for export summaries with explicit metric tables.",
        is_pinned=False
    )
    db.add_all([mem1, mem2, mem3])

    # 6. Seed Notifications
    notif1 = Notification(
        user_id=current_user.id,
        title="Approval Required",
        message="Task 'Analyze quarterly cloud spend' requires approval for Step 3.",
        notification_type="APPROVAL_REQUIRED",
        link_url=f"/app/tasks/{task2.id}",
        is_read=False
    )
    notif2 = Notification(
        user_id=current_user.id,
        title="Study Plan Ready",
        message="Your machine learning study plan has completed all 4 execution steps.",
        notification_type="TASK_COMPLETED",
        link_url=f"/app/tasks/{task1.id}",
        is_read=True
    )
    db.add_all([notif1, notif2])
    db.commit()

    return {
        "success": True,
        "message": "Demo data successfully seeded for this account.",
        "seeded": {
            "tasks": 2,
            "conversations": 1,
            "documents": 1,
            "chunks": 3,
            "memories": 3,
            "notifications": 2
        }
    }


@router.post("/reset")
def reset_demo_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(Task).filter(Task.user_id == current_user.id).delete()
    db.query(Conversation).filter(Conversation.user_id == current_user.id).delete()
    db.query(Memory).filter(Memory.user_id == current_user.id).delete()
    db.query(KnowledgeDocument).filter(KnowledgeDocument.user_id == current_user.id).delete()
    db.query(Notification).filter(Notification.user_id == current_user.id).delete()
    db.commit()
    return {"success": True, "message": "All workspace data reset to clean state."}
