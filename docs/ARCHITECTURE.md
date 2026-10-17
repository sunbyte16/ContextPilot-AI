# ContextPilot AI — System Architecture

ContextPilot AI is architected as a modular, high-fidelity agentic AI platform designed for the Amazon Developer Hackathon. It bridges natural-language intent with reliable, approval-gated tool execution.

## High-Level Architectural Diagram

```mermaid
flowchart TD
    subgraph Client["Presentation Layer (React 18 + Vite)"]
        Landing["Landing Page (/)"]
        AuthUI["Auth Pages (/login, /register)"]
        Dashboard["Dashboard (/app)"]
        Chat["Conversational Assistant (/app/assistant)"]
        Tasks["Task Monitor (/app/tasks, /app/tasks/:id)"]
        MemoryUI["Context Memory (/app/memory)"]
        KnowledgeUI["Knowledge RAG (/app/knowledge)"]
        ToolsUI["Tool Registry (/app/tools)"]
        TelemetryUI["Activity & Audit (/app/activity)"]
        AnalyticsUI["Analytics & Metrics (/app/analytics)"]
    end

    subgraph Gateway["API Layer (FastAPI)"]
        AuthMiddleware["JWT Authentication & Tenant Isolation"]
        Routers["REST Endpoints (/api/v1/*)"]
    end

    subgraph CoreEngine["Agent & Orchestration Engine"]
        Orchestrator["Agent Orchestrator"]
        LLMFactory["LLM Provider (LocalDemo / Bedrock)"]
        ApprovalGate["Server-Side Human Approval Gate"]
        Dispatcher["Controlled Tool Dispatcher"]
    end

    subgraph Tools["Sandboxed Tool Ecosystem (9 Tools)"]
        T1["DateTime Utility"]
        T2["Safe Calculator (AST)"]
        T3["Task Manager"]
        T4["Knowledge Retriever (BM25)"]
        T5["Structured Summarizer"]
        T6["Workflow Planner"]
        T7["Tabular Data Analyzer"]
        T8["Notification Center"]
        T9["Report Exporter (Markdown/JSON/CSV)"]
    end

    subgraph Storage["Persistence & Isolation"]
        DB[(SQLite / PostgreSQL via SQLAlchemy)]
        DocStore["Encrypted Document & Chunks Store"]
    end

    Client --> Gateway
    Gateway --> AuthMiddleware --> Routers
    Routers --> Orchestrator
    Orchestrator --> LLMFactory
    Orchestrator --> ApprovalGate
    ApprovalGate --> Dispatcher
    Dispatcher --> Tools
    Orchestrator --> DB
    Dispatcher --> DB
    Routers --> DocStore
```

## Architectural Pillars

1. **Strict Server-Side Safety Gate**:
   - Agent models cannot unilaterally execute consequential operations. If a step is marked `requires_approval=True` or has `risk_level == "HIGH"`, the backend halts pipeline execution and persists an `ApprovalRequest`.
   - The pipeline remains in `AWAITING_APPROVAL` status until a signed human approval payload is received.

2. **Per-User Tenant Isolation**:
   - All database tables enforce foreign-key ownership by `user_id`. Queries filter explicitly by authenticated identity derived from the verified JWT access token.
   - Cross-user data leakage is strictly blocked.

3. **Multi-Provider LLM Abstraction**:
   - `BaseLLMProvider` decouples the system from proprietary APIs.
   - `LocalDemoProvider`: Deterministic, rich offline execution engine requiring zero cloud credentials or paid tokens.
   - `BedrockProvider`: Genuine Amazon Bedrock Converse API adapter supporting Claude 3 Sonnet and Amazon Titan.

4. **Verifiable Execution Outcomes**:
   - The orchestrator verifies task completion based strictly on actual tool outputs returned from the sandboxed dispatchers rather than model hallucination.
