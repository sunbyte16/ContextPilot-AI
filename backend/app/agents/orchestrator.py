import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.all_models import (
    User, Conversation, Message, Task, TaskStep, ApprovalRequest,
    ExecutionEvent, AuditEvent, Memory, KnowledgeDocument, DocumentChunk, Notification
)
from app.tools.registry import tool_registry
from app.agents.providers.factory import get_llm_provider


class AgentOrchestrator:

    def process_user_message(
        self,
        user: User,
        db: Session,
        content: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Processes conversational input, coordinates memory/RAG, and plans workflows."""
        # 1. Ensure conversation exists
        conv = None
        if conversation_id:
            conv = db.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user.id
            ).first()
        if not conv:
            conv = Conversation(
                user_id=user.id,
                title=content[:40] + ("..." if len(content) > 40 else "")
            )
            db.add(conv)
            db.commit()
            db.refresh(conv)

        # 2. Persist user message
        user_msg = Message(
            conversation_id=conv.id,
            sender="user",
            content=content,
            msg_metadata={}
        )
        db.add(user_msg)
        db.commit()

        # 3. Retrieve user memories
        memories = db.query(Memory).filter(Memory.user_id == user.id).all()
        mem_data = [{"title": m.title, "content": m.content, "category": m.category, "is_pinned": m.is_pinned} for m in memories]

        # 4. Check for knowledge queries
        retrieved_docs = []
        doc_count = db.query(KnowledgeDocument).filter(
            KnowledgeDocument.user_id == user.id,
            KnowledgeDocument.processing_status == "INDEXED"
        ).count()
        if doc_count > 0:
            retriever_tool = tool_registry.get_tool("knowledge_retriever")
            if retriever_tool:
                try:
                    rag_res = retriever_tool.execute({"query": content, "top_k": 3}, context={"user": user, "db": db})
                    if rag_res.get("success") and rag_res.get("citations"):
                        retrieved_docs = rag_res["citations"]
                except Exception:
                    pass

        # 5. Fetch Provider
        pref_model = user.preference.preferred_model if user.preference else None
        provider = get_llm_provider(pref_model)

        # 6. Generate Assistant Response
        history_msgs = db.query(Message).filter(Message.conversation_id == conv.id).order_by(Message.created_at.asc()).limit(10).all()
        history_payload = [{"role": m.sender, "content": m.content} for m in history_msgs]

        chat_result = provider.generate_chat_response(
            messages=history_payload,
            context_memories=mem_data,
            retrieved_documents=retrieved_docs
        )

        task_id = None
        # 7. If objective implies a structured task, generate plan!
        if chat_result.get("is_plan_request"):
            available_tools = tool_registry.list_tools(db=db)
            plan_data = provider.generate_plan(
                objective=content,
                available_tools=available_tools,
                context_memories=mem_data,
                retrieved_documents=retrieved_docs
            )

            # Create Task
            task = Task(
                user_id=user.id,
                conversation_id=conv.id,
                objective=content,
                description=plan_data.get("description", f"Execution plan for: {content}"),
                status="DRAFT",
                risk_level=plan_data.get("risk_level", "LOW"),
                estimated_complexity=plan_data.get("estimated_complexity", "STANDARD"),
                progress=0
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            task_id = task.id

            # Create Steps
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

                # If step requires approval, create ApprovalRequest
                if step.requires_approval or step.risk_level in ["HIGH", "CRITICAL"]:
                    has_approval_gate = True
                    appr = ApprovalRequest(
                        task_id=task.id,
                        step_id=step.id,
                        user_id=user.id,
                        action_name=f"Execute {step.tool_name or 'step'}",
                        action_purpose=step.description,
                        target_resource=step.tool_name,
                        parameters_summary=step.tool_input,
                        risk_level=step.risk_level,
                        status="PENDING"
                    )
                    db.add(appr)

            if has_approval_gate:
                task.status = "AWAITING_APPROVAL"
            else:
                task.status = "APPROVED"
            db.commit()

            # Record event
            event = ExecutionEvent(
                task_id=task.id,
                event_type="PLAN_GENERATED",
                message=f"Plan generated with {len(plan_data.get('steps', []))} steps. Status: {task.status}",
                payload={"steps_count": len(plan_data.get("steps", []))}
            )
            db.add(event)
            db.commit()

        # 8. Save Assistant Message
        assistant_msg = Message(
            conversation_id=conv.id,
            sender="assistant",
            content=chat_result["content"],
            msg_metadata={
                "task_id": task_id,
                "citations": chat_result.get("citations", []),
                "intent": chat_result.get("intent", "chat"),
                "suggested_followups": chat_result.get("suggested_followups", [])
            }
        )
        db.add(assistant_msg)
        db.commit()
        db.refresh(assistant_msg)

        return {
            "conversation_id": conv.id,
            "message_id": assistant_msg.id,
            "content": assistant_msg.content,
            "task_id": task_id,
            "citations": chat_result.get("citations", []),
            "suggested_followups": chat_result.get("suggested_followups", [])
        }

    def execute_task(self, task_id: str, user: User, db: Session) -> Dict[str, Any]:
        """Executes approved task steps sequentially with approval enforcement."""
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
        if not task:
            raise ValueError("Task not found.")

        if task.status in ["COMPLETED", "CANCELLED"]:
            return {"status": task.status, "message": f"Task is already {task.status}."}

        task.status = "RUNNING"
        db.commit()

        steps = db.query(TaskStep).filter(TaskStep.task_id == task.id).order_by(TaskStep.step_order.asc()).all()
        total_steps = len(steps)
        completed_steps = sum(1 for s in steps if s.status == "COMPLETED")

        for step in steps:
            if step.status == "COMPLETED":
                continue

            # Check approval requirement
            if step.requires_approval or step.risk_level in ["HIGH", "CRITICAL"]:
                # Verify if an approval has been granted
                appr = db.query(ApprovalRequest).filter(
                    ApprovalRequest.task_id == task.id,
                    ApprovalRequest.step_id == step.id,
                    ApprovalRequest.status == "APPROVED"
                ).first()

                if not appr:
                    # Halt execution and await approval
                    step.status = "AWAITING_APPROVAL"
                    task.status = "AWAITING_APPROVAL"
                    event = ExecutionEvent(
                        task_id=task.id,
                        step_id=step.id,
                        event_type="APPROVAL_REQUIRED",
                        message=f"Step {step.step_order} '{step.description}' requires explicit user approval.",
                        payload={"tool": step.tool_name, "risk": step.risk_level}
                    )
                    db.add(event)
                    db.commit()
                    return {
                        "status": "AWAITING_APPROVAL",
                        "current_step_order": step.step_order,
                        "step_id": step.id,
                        "message": f"Paused at Step {step.step_order} awaiting human approval."
                    }

            # Execute step
            step.status = "RUNNING"
            step.started_at = datetime.now(timezone.utc)
            db.commit()

            start_t = time.time()
            # Dispatch tool
            if step.tool_name:
                dispatch_res = tool_registry.dispatch(
                    tool_id=step.tool_name,
                    params=step.tool_input or {},
                    user=user,
                    db=db,
                    task_id=task.id,
                    step_id=step.id,
                    is_approved=True
                )
                step.execution_time_ms = dispatch_res["duration_ms"]
                step.actual_output = dispatch_res["output"]

                if dispatch_res["status"] == "FAILURE":
                    step.status = "FAILED"
                    step.error_message = dispatch_res.get("error", "Tool execution failed")
                    task.status = "FAILED"
                    task.error_message = f"Failed at step {step.step_order}: {step.error_message}"
                    event = ExecutionEvent(
                        task_id=task.id,
                        step_id=step.id,
                        event_type="ERROR",
                        message=f"Step {step.step_order} failed: {step.error_message}",
                        payload={"error": step.error_message}
                    )
                    db.add(event)
                    db.commit()
                    return {
                        "status": "FAILED",
                        "failed_step_order": step.step_order,
                        "error": step.error_message
                    }

            step.status = "COMPLETED"
            step.completed_at = datetime.now(timezone.utc)
            completed_steps += 1
            task.progress = int((completed_steps / total_steps) * 100)

            event = ExecutionEvent(
                task_id=task.id,
                step_id=step.id,
                event_type="STEP_COMPLETED",
                message=f"Step {step.step_order} completed successfully ({step.tool_name or 'internal'}).",
                payload={"duration_ms": step.execution_time_ms}
            )
            db.add(event)
            db.commit()

        # If all steps completed
        task.status = "COMPLETED"
        task.progress = 100
        task.completed_at = datetime.now(timezone.utc)
        task.result_summary = (
            f"All {total_steps} plan steps executed and verified successfully. "
            f"Completed tools: {', '.join([s.tool_name for s in steps if s.tool_name])}."
        )

        final_event = ExecutionEvent(
            task_id=task.id,
            event_type="TASK_COMPLETED",
            message=task.result_summary,
            payload={"completed_steps": total_steps}
        )
        db.add(final_event)

        # Notify user
        notif = Notification(
            user_id=user.id,
            title="Task Completed",
            message=f"'{task.objective}' has successfully finished execution.",
            notification_type="TASK_COMPLETED",
            link_url=f"/app/tasks/{task.id}"
        )
        db.add(notif)
        db.commit()

        return {
            "status": "COMPLETED",
            "progress": 100,
            "result_summary": task.result_summary
        }

    def handle_approval_decision(
        self,
        task_id: str,
        approval_id: str,
        approved: bool,
        decision_notes: Optional[str],
        user: User,
        db: Session
    ) -> Dict[str, Any]:
        """Processes human approval or rejection for a sensitive action."""
        appr = db.query(ApprovalRequest).filter(
            ApprovalRequest.id == approval_id,
            ApprovalRequest.task_id == task_id,
            ApprovalRequest.user_id == user.id
        ).first()

        if not appr:
            raise ValueError("Approval request not found.")

        appr.status = "APPROVED" if approved else "REJECTED"
        appr.decision_notes = decision_notes
        appr.decided_at = datetime.now(timezone.utc)

        audit = AuditEvent(
            user_id=user.id,
            event_type="APPROVAL_GRANTED" if approved else "APPROVAL_REJECTED",
            resource_type="approval_request",
            resource_id=appr.id,
            action="approve_action" if approved else "reject_action",
            details={
                "task_id": task_id,
                "step_id": appr.step_id,
                "action_name": appr.action_name,
                "decision_notes": decision_notes
            }
        )
        db.add(audit)

        task = db.query(Task).filter(Task.id == task_id).first()
        if not approved:
            task.status = "CANCELLED"
            task.error_message = f"Action rejected by user: {decision_notes or 'No reason provided'}"
            db.commit()
            return {"status": "REJECTED", "message": "Action was rejected and task cancelled."}

        task.status = "APPROVED"
        db.commit()

        # Trigger continuation of execution
        return self.execute_task(task_id, user, db)


orchestrator = AgentOrchestrator()
