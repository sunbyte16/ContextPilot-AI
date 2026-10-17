import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Boolean, Integer, Float, DateTime, ForeignKey, Text, JSON, Enum
)
from sqlalchemy.orm import relationship
from app.db.session import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationships
    preference = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    memories = relationship("Memory", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("KnowledgeDocument", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    audit_events = relationship("AuditEvent", back_populates="user", cascade="all, delete-orphan")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    preferred_model = Column(String(100), default="local-demo")  # local-demo, bedrock-claude, bedrock-titan
    response_style = Column(String(50), default="precise")  # concise, balanced, detailed, precise
    memory_enabled = Column(Boolean, default=True)
    default_approval_behavior = Column(String(50), default="require_consequential")  # require_all, require_consequential, auto_approve_low
    execution_timeout_seconds = Column(Integer, default=120)
    theme = Column(String(20), default="dark")  # dark, light, system
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="preference")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), default="New Conversation")
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")
    tasks = relationship("Task", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    msg_metadata = Column(JSON, default=dict)  # citations, tool calls, task_id reference
    created_at = Column(DateTime(timezone=True), default=utc_now)

    conversation = relationship("Conversation", back_populates="messages")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="SET NULL"), nullable=True, index=True)
    objective = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="DRAFT", index=True)
    # DRAFT, AWAITING_APPROVAL, APPROVED, QUEUED, RUNNING, PAUSED, COMPLETED, PARTIALLY_COMPLETED, FAILED, CANCELLED
    risk_level = Column(String(20), default="LOW")  # LOW, MEDIUM, HIGH, CRITICAL
    priority = Column(String(20), default="MEDIUM")  # LOW, MEDIUM, HIGH, URGENT
    progress = Column(Integer, default=0)  # 0 to 100
    estimated_complexity = Column(String(50), default="STANDARD")  # SIMPLE, STANDARD, COMPLEX
    result_summary = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="tasks")
    conversation = relationship("Conversation", back_populates="tasks")
    steps = relationship("TaskStep", back_populates="task", cascade="all, delete-orphan", order_by="TaskStep.step_order")
    approvals = relationship("ApprovalRequest", back_populates="task", cascade="all, delete-orphan")
    execution_events = relationship("ExecutionEvent", back_populates="task", cascade="all, delete-orphan", order_by="ExecutionEvent.created_at")


class TaskStep(Base):
    __tablename__ = "task_steps"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    task_id = Column(String(36), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    step_order = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    tool_name = Column(String(100), nullable=True)
    tool_input = Column(JSON, default=dict)
    expected_output = Column(Text, nullable=True)
    actual_output = Column(JSON, nullable=True)
    status = Column(String(50), default="PENDING")
    # PENDING, AWAITING_APPROVAL, RUNNING, COMPLETED, FAILED, SKIPPED
    risk_level = Column(String(20), default="LOW")
    requires_approval = Column(Boolean, default=False)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=2)
    execution_time_ms = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    task = relationship("Task", back_populates="steps")
    approval_requests = relationship("ApprovalRequest", back_populates="step", cascade="all, delete-orphan")


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    task_id = Column(String(36), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    step_id = Column(String(36), ForeignKey("task_steps.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action_name = Column(String(150), nullable=False)
    action_purpose = Column(Text, nullable=False)
    target_resource = Column(String(255), nullable=True)
    parameters_summary = Column(JSON, default=dict)
    risk_level = Column(String(20), default="HIGH")
    status = Column(String(30), default="PENDING")  # PENDING, APPROVED, REJECTED, EXPIRED
    decision_notes = Column(Text, nullable=True)
    requested_at = Column(DateTime(timezone=True), default=utc_now)
    decided_at = Column(DateTime(timezone=True), nullable=True)

    task = relationship("Task", back_populates="approvals")
    step = relationship("TaskStep", back_populates="approval_requests")


class ToolExecution(Base):
    __tablename__ = "tool_executions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(String(36), nullable=True, index=True)
    step_id = Column(String(36), nullable=True, index=True)
    tool_name = Column(String(100), nullable=False, index=True)
    input_payload = Column(JSON, default=dict)
    output_payload = Column(JSON, default=dict)
    status = Column(String(30), default="SUCCESS")  # SUCCESS, FAILURE
    duration_ms = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    executed_at = Column(DateTime(timezone=True), default=utc_now)


class ExecutionEvent(Base):
    __tablename__ = "execution_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    task_id = Column(String(36), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    step_id = Column(String(36), nullable=True, index=True)
    event_type = Column(String(50), nullable=False)  # PLAN_GENERATED, STEP_START, TOOL_EXEC, APPROVAL_NEEDED, STEP_COMPLETED, TASK_COMPLETED, ERROR
    message = Column(Text, nullable=False)
    payload = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    task = relationship("Task", back_populates="execution_events")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    # AUTH_LOGIN, TASK_CREATED, APPROVAL_GRANTED, APPROVAL_REJECTED, TOOL_EXECUTED, MEMORY_MUTATED, DOC_UPLOADED, DOC_DELETED
    resource_type = Column(String(50), nullable=True)
    resource_id = Column(String(36), nullable=True)
    action = Column(String(100), nullable=False)
    details = Column(JSON, default=dict)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="audit_events")


class Memory(Base):
    __tablename__ = "memories"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(50), default="FACT")  # FACT, PREFERENCE, PROJECT_CONTEXT, NOTE, TASK_OUTCOME
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    confidence_score = Column(Float, default=1.0)
    source_reference = Column(String(255), nullable=True)
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="memories")


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, txt, md, json
    file_size_bytes = Column(Integer, default=0)
    storage_path = Column(String(500), nullable=False)
    processing_status = Column(String(30), default="PENDING")  # PENDING, PROCESSING, INDEXED, FAILED
    error_message = Column(Text, nullable=True)
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("knowledge_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    page_number = Column(Integer, default=1)
    content = Column(Text, nullable=False)
    chunk_metadata = Column(JSON, default=dict)

    document = relationship("KnowledgeDocument", back_populates="chunks")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="INFO")  # INFO, APPROVAL_REQUIRED, TASK_COMPLETED, TASK_FAILED
    link_url = Column(String(255), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="notifications")
