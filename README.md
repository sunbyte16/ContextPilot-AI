<div align="center">

# 🧭 ContextPilot AI

### *Autonomous Multi-Step Agentic AI Assistant Platform with Human-in-the-Loop Governance & Grounded RAG*

**Amazon Developer Hackathon Submission**

---

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3.1-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5.3-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4.1-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Amazon Bedrock](https://img.shields.io/badge/AWS-Amazon_Bedrock-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/bedrock)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2.7-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

**Crafted by [𝕊𝕦𝕟𝕚𝕝 𝕊𝕙𝕒𝕣𝕞𝕒](https://lively-dodol-cc397c.netlify.app)**

[![GitHub](https://img.shields.io/badge/GitHub-sunbyte16-181717?style=flat-square&logo=github)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil_Kumar-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Sunil_Sharma-FF5722?style=flat-square&logo=netlify)](https://lively-dodol-cc397c.netlify.app)

<br/>

> **"Transform natural-language goals into verifiable plans, coordinate sandboxed tools, preserve context, enforce server-side human approval for consequential operations, and verify outcomes with zero hallucination."**

<br/>

<p align="center">
  <img src="images/07_dashboard_overview.png" alt="ContextPilot AI Dashboard" width="95%" style="border-radius: 12px; border: 1px solid #1e293b; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);" />
</p>

</div>

---

## 📑 Table of Contents

- [📌 Executive Summary](#-executive-summary)
- [📖 The Project Story (About.md)](About.md)
- [📸 Visual Tour & User Interface Showcase](#-visual-tour--user-interface-showcase)
- [✨ Key Architectural Innovations](#-key-architectural-innovations)
- [📐 Modern System Architecture](#-modern-system-architecture)
  - [1. End-to-End System Architecture](#1-end-to-end-system-architecture)
  - [2. Autonomous Agent Lifecycle & Decision Sequence](#2-autonomous-agent-lifecycle--decision-sequence)
  - [3. Human-in-the-Loop State Machine](#3-human-in-the-loop-state-machine)
  - [4. Grounded RAG & Citation Engine Pipeline](#4-grounded-rag--citation-engine-pipeline)
- [🛠️ Tool Ecosystem & Sandboxing](#️-tool-ecosystem--sandboxing)
- [🧰 Technology Stack](#-technology-stack)
- [🚀 Quickstart Guide](#-quickstart-guide)
  - [Prerequisites](#prerequisites)
  - [1. Backend Setup](#1-backend-setup)
  - [2. Frontend Setup](#2-frontend-setup)
- [⚡ 3-Minute Hackathon Demo Walkthrough](#-3-minute-hackathon-demo-walkthrough)
- [☁️ AWS Bedrock Integration](#️-aws-bedrock-integration)
- [🐳 Docker Deployment](#-docker-deployment)
- [🧪 Testing & Verification Evidence](#-testing--verification-evidence)
- [🔒 Security & Safety Guarantees](#-security--safety-guarantees)
- [📂 Project Directory Tree](#-project-directory-tree)
- [🤝 Contributing & Community Guidelines](#-contributing--community-guidelines)
- [👨‍💻 Author & Connect](#-author--connect)
- [📄 License & Disclaimer](#-license--disclaimer)

---

## 📌 Executive Summary

**ContextPilot AI** is an intelligent, autonomous agentic AI assistant platform built for the **Amazon Developer Hackathon**. 

Rather than functioning as a standard conversational chatbot that produces unstructured text predictions, ContextPilot AI acts as a **true execution partner**:
1. **Understands High-Level Goals:** Parses complex intent, decomposes requests into dependency-ordered Directed Acyclic Graphs (DAGs) of tasks and subtasks.
2. **Executes Sandboxed Tools:** Coordinates 9 type-safe, auditable tools spanning math parsing, date-time manipulation, knowledge retrieval, tabular analytics, and report export.
3. **Guards Consequential Operations:** Employs **server-side Human-in-the-Loop (HITL) approval gates** that automatically halt execution when sensitive operations (e.g. data export, file mutations) are detected.
4. **Remembers Long-Term Context:** Maintains persistent user preferences, past constraints, and episodic memory across sessions.
5. **Eliminates Hallucinations:** Implements Grounded Retrieval-Augmented Generation (RAG) with exact document chunk citations. If evidence is missing, the system explicitly refuses to guess.
6. **Dual AI Engine:** Runs **100% offline out-of-the-box** using a deterministic `LocalDemoProvider` (zero API keys or costs required), and connects seamlessly to **Amazon Bedrock** (Anthropic Claude 3 / Amazon Titan via AWS SDK `boto3` Converse API) when cloud credentials are configured.

> [!NOTE]
> **Hackathon Simulation Disclosure:**  
> ContextPilot AI is designed as an **Alexa+-inspired simulated web application**. It runs natively on standard development laptops without requiring physical Amazon Echo, Fire TV, Bee wearable, or Ring devices. Audio and conversational interactions are simulated within the web UI.

> [!TIP]
> **📖 Read the Project Story:**  
> Discover what inspired ContextPilot AI, key architectural learnings, the engineering journey, and technical breakthroughs in [**About.md**](About.md).

---

## 📸 Visual Tour & User Interface Showcase

Experience the production polish and design system of ContextPilot AI across its complete suite of **23 application views, modals, telemetry dashboards, and interactive states**:

### 🧭 Core Platform & Mission Control

<details open>
<summary><b>1. Mission Control & Operational Dashboard (<code>images/07_dashboard_overview.png</code>)</b></summary>
<br/>

The executive workspace command center providing real-time pipeline telemetry, quick action launchers, active task metrics, and environment status.

<p align="center">
  <img src="images/07_dashboard_overview.png" alt="Mission Control Dashboard" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details open>
<summary><b>2. Conversational Agent & Multi-Step Planner (<code>images/08_assistant_chat.png</code>)</b></summary>
<br/>

Conversational workspace where high-level natural language objectives are analyzed, decomposed into DAG execution steps, and displayed with intent badges and citations.

<p align="center">
  <img src="images/08_assistant_chat.png" alt="Conversational Agent Workspace" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details open>
<summary><b>3. Live Assistant Multi-Step Execution & Trace (<code>images/09_assistant_active_execution.png</code>)</b></summary>
<br/>

Active conversation stream showing multi-step plan synthesis, tool coordination, and transparent verification traces.

<p align="center">
  <img src="images/09_assistant_active_execution.png" alt="Active Assistant Execution" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details open>
<summary><b>4. Autonomous Task & Plan Monitor (<code>images/10_task_workflows.png</code>)</b></summary>
<br/>

Real-time task tracking interface visualizing scheduled milestones, execution priority, percentage completion, and risk classifications.

<p align="center">
  <img src="images/10_task_workflows.png" alt="Task Workflows Monitor" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details open>
<summary><b>5. Human-in-the-Loop Server-Side Approval Gate (<code>images/11_task_detail_approval.png</code>)</b></summary>
<br/>

When consequential operations (e.g. `export_tool`) are detected, execution strictly yields into `AWAITING_APPROVAL`. Users review exact proposed parameters and risk levels before authorizing execution.

<p align="center">
  <img src="images/11_task_detail_approval.png" alt="Human Approval Checkpoint" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

### 🧠 Intelligence, Tools & Grounded RAG

<details>
<summary><b>6. Knowledge Base & Grounded RAG Overview (<code>images/12_knowledge_rag.png</code>)</b></summary>
<br/>

Document ingestion manager showing indexed PDFs and Markdown documents with chunk counts and storage metrics.

<p align="center">
  <img src="images/12_knowledge_rag.png" alt="Knowledge Base & Grounded RAG" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>7. Grounded Q&A Verification with Citations (<code>images/13_knowledge_rag_search.png</code>)</b></summary>
<br/>

Grounded search sandbox where questions are answered strictly from verified document chunks with source filenames and page citations. Refuses to guess if evidence is insufficient.

<p align="center">
  <img src="images/13_knowledge_rag_search.png" alt="Grounded Q&A Verification" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>8. Persistent Contextual Memory Hub (<code>images/14_memory_hub.png</code>)</b></summary>
<br/>

Curated user memory system tracking user preferences, project constraints, and episodic facts with category badges (`FACT`, `PREFERENCE`, `PROJECT CONTEXT`, `NOTE`).

<p align="center">
  <img src="images/14_memory_hub.png" alt="Contextual Memory Hub" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>9. Sandboxed Tool Safety Registry (<code>images/15_tool_registry.png</code>)</b></summary>
<br/>

Comprehensive registry for all 9 registered execution dispatchers, enforcing strict input/output schemas and AST security boundaries.

<p align="center">
  <img src="images/15_tool_registry.png" alt="Tool Registry & Safety Testbench" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>10. Interactive Tool Execution Testbench (<code>images/16_tool_testbench_modal.png</code>)</b></summary>
<br/>

Live modal testbench allowing interactive parameter testing, sandboxed invocation, and real-time JSON result inspection.

<p align="center">
  <img src="images/16_tool_testbench_modal.png" alt="Tool Execution Testbench Modal" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

### 📊 Telemetry, Security & Governance

<details>
<summary><b>11. Immutable Activity & Audit Trail (<code>images/17_activity_audit.png</code>)</b></summary>
<br/>

Tamper-evident audit log recording every user authentication, task transition, tool invocation, and human approval decision.

<p align="center">
  <img src="images/17_activity_audit.png" alt="Activity & Audit Stream" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>12. Real-Time System Notification Center (<code>images/18_activity_notifications.png</code>)</b></summary>
<br/>

Centralized notification inbox organizing approval requests, execution alerts, and system health status.

<p align="center">
  <img src="images/18_activity_notifications.png" alt="Notification Center" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>13. Real-Time Telemetry & Recharts Analytics (<code>images/19_analytics_telemetry.png</code>)</b></summary>
<br/>

Live execution metrics computed directly from database records, including 7-day completion trends, tool invocation frequency, and pipeline status breakdowns.

<p align="center">
  <img src="images/19_analytics_telemetry.png" alt="Analytics & Telemetry" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

### ⚙️ Configuration & Enterprise Controls

<details>
<summary><b>14. Settings: User Profile & Tenant Info (<code>images/20_settings_profile.png</code>)</b></summary>
<br/>

User account preferences, profile credentials, and workspace tenant isolation configuration.

<p align="center">
  <img src="images/20_settings_profile.png" alt="User Profile Settings" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>15. Settings: Assistant Preferences & Autonomy Gates (<code>images/21_settings_assistant.png</code>)</b></summary>
<br/>

Granular controls over agent execution autonomy, auto-approval thresholds for low-risk actions, and default planning strategies.

<p align="center">
  <img src="images/21_settings_assistant.png" alt="Assistant Preferences" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>16. Settings: Model Providers & AWS Bedrock (<code>images/22_settings_provider.png</code>)</b></summary>
<br/>

Seamlessly toggle between deterministic offline `LocalDemoProvider` and live AWS Bedrock `BedrockProvider` with interactive connectivity testing.

<p align="center">
  <img src="images/22_settings_provider.png" alt="Model Providers & AWS Bedrock" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>17. Comprehensive Documentation & User Guide (<code>images/23_help_guide.png</code>)</b></summary>
<br/>

In-app documentation, architectural guides, security policies, and keyboard shortcuts.

<p align="center">
  <img src="images/23_help_guide.png" alt="Documentation & User Guide" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

### 🌐 Public Portal & Onboarding Experience

<details>
<summary><b>18. Product Landing Page Hero (<code>images/01_landing_page.png</code>)</b></summary>
<br/>

Polished product landing page explaining the verifiable agentic lifecycle, features, and hackathon scope.

<p align="center">
  <img src="images/01_landing_page.png" alt="Product Landing Page Hero" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>19. Product Landing Page Features & Architecture (<code>images/02_landing_features.png</code>)</b></summary>
<br/>

In-depth feature breakdown, multi-step agent flow visualizer, and technology architecture highlights.

<p align="center">
  <img src="images/02_landing_features.png" alt="Product Landing Page Features" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>20. User Authentication & 1-Click Demo Login (<code>images/03_login_page.png</code>)</b></summary>
<br/>

Secure sign-in with instant demo credential autofill for immediate evaluation by hackathon reviewers.

<p align="center">
  <img src="images/03_login_page.png" alt="Sign In Page" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>21. Account Registration (<code>images/04_register_page.png</code>)</b></summary>
<br/>

User registration screen with password complexity validation and tenant initialization.

<p align="center">
  <img src="images/04_register_page.png" alt="Registration Page" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>22. Data Privacy & Sovereignty Policy (<code>images/05_privacy_policy.png</code>)</b></summary>
<br/>

Detailed explanation of local data persistence, sandboxed execution safety, and zero telemetry sharing.

<p align="center">
  <img src="images/05_privacy_policy.png" alt="Privacy Policy" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

<br/>

<details>
<summary><b>23. Terms of Service & Simulation Disclosure (<code>images/06_terms_of_service.png</code>)</b></summary>
<br/>

Comprehensive terms of service with explicit Alexa+-inspired simulation disclosures.

<p align="center">
  <img src="images/06_terms_of_service.png" alt="Terms of Service" width="100%" style="border-radius: 8px; border: 1px solid #1e293b;" />
</p>
</details>

---

## ✨ Key Architectural Innovations

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                           ContextPilot AI                              │
  ├────────────────────────────────────────────────────────────────────────┤
  │  🎯 Goal Decomposition       ⚡ Sandboxed Tool Execution              │
  │  🛡️ Server-Side HITL Gates   🧠 Persistent Episodic Memory            │
  │  📚 Grounded RAG Citations   📊 Real-Time Execution Telemetry         │
  │  🔌 Dual Engine (Offline/AWS)🔒 Multi-Tenant Data Isolation           │
  └────────────────────────────────────────────────────────────────────────┘
```

| Capability | Engineering Implementation | Hackathon Advantage |
|---|---|---|
| **Autonomous Planning** | Dynamic goal decomposition into multi-step execution graphs. | Decomposes high-level intent into deterministic tool steps. |
| **Human-in-the-Loop** | Server-side `AWAITING_APPROVAL` barrier blocks execution until signed approval. | Eliminates rogue agent execution and unauthorized data mutation. |
| **Sandboxed AST Tools** | Python Abstract Syntax Tree (`ast.parse`) mathematical parser; zero host shell. | Math evaluation without arbitrary code execution vulnerabilities. |
| **Grounded RAG** | `pypdf` text stream parser + Sliding chunk indexer + BM25 precision matching. | Page-level verifiable citations; zero hallucination honesty. |
| **Contextual Memory** | Tagged key-value memory store persisted in relational database per user. | Learns user constraints and applies them across conversations. |
| **Dual AI Provider** | Abstracted `BaseLLMProvider` with `LocalDemoProvider` & `BedrockProvider`. | Guaranteed zero-friction local reviewer evaluation + genuine AWS power. |
| **Audit & Telemetry** | Append-only `AuditEvent` and `ExecutionEvent` streams with millisecond latency. | Full transparency into agent reasoning and tool performance. |

---

## 📐 Modern System Architecture

### 1. End-to-End System Architecture

```mermaid
flowchart TD
    classDef client fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef gateway fill:#0f172a,stroke:#818cf8,stroke-width:2px,color:#f8fafc;
    classDef agent fill:#1e1b4b,stroke:#c084fc,stroke-width:2px,color:#f8fafc;
    classDef tools fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#f8fafc;
    classDef storage fill:#312e81,stroke:#a5b4fc,stroke-width:2px,color:#f8fafc;
    classDef aws fill:#451a03,stroke:#fb923c,stroke-width:2px,color:#f8fafc;

    subgraph ClientLayer ["Client Workspace (React 18 + TypeScript + Vite)"]
        UI["Modern Responsive UI Shell"]:::client
        ChatComp["Conversational Assistant"]:::client
        TaskComp["Task & Workflow Inspector"]:::client
        ApprovalModal["Human Approval Modal / Drawer"]:::client
        RAGComp["Knowledge Base & Citation Sandbox"]:::client
        AnalyticsComp["Recharts Telemetry Dashboard"]:::client
    end

    subgraph APILayer ["API Gateway & Security Layer (FastAPI 0.111)"]
        Router["FastAPI REST Router (/api/v1)"]:::gateway
        AuthModule["JWT HS256 Auth & Bcrypt Security"]:::gateway
        TenantIsolation["Multi-Tenant Isolation Filter (user_id)"]:::gateway
        Validation["Pydantic v2 Schema Validation"]:::gateway
    end

    subgraph AgentEngine ["ContextPilot Agent Core"]
        Orchestrator["Agent Orchestrator Engine"]:::agent
        Planner["Goal Decomposition & DAG Planner"]:::agent
        MemoryInject["Context & Memory Injector"]:::agent
        ApprovalGate{"Server-Side Approval Checkpoint"}:::agent
    end

    subgraph ToolRegistry ["Sandboxed Tool Ecosystem"]
        T1["safe_calculator (AST)"]:::tools
        T2["date_time (Clock/Diff)"]:::tools
        T3["task_manager (CRUD)"]:::tools
        T4["knowledge_retriever (BM25)"]:::tools
        T5["structured_summarizer"]:::tools
        T6["workflow_planner"]:::tools
        T7["data_analysis (Stats)"]:::tools
        T8["notification_center"]:::tools
        T9["export_tool (Gated)"]:::tools
    end

    subgraph LLMProviders ["Dual Model Provider Engine"]
        LocalLLM["LocalDemoProvider (Offline / Deterministic)"]:::aws
        BedrockLLM["BedrockProvider (AWS SDK boto3 Converse API)"]:::aws
    end

    subgraph DataLayer ["Persistence & Knowledge Engine"]
        DB[("SQLAlchemy 2.0 (SQLite / PostgreSQL)")]:::storage
        DocStore["Document Chunker & BM25 Inverted Index"]:::storage
        AuditLog["Immutable Audit & Telemetry Store"]:::storage
    end

    %% Connections
    UI --> Router
    Router --> AuthModule --> TenantIsolation --> Validation
    Validation --> Orchestrator
    
    Orchestrator --> MemoryInject
    MemoryInject <--> DB
    Orchestrator --> Planner
    Planner --> LocalLLM
    Planner --> BedrockLLM
    
    Planner --> ApprovalGate
    ApprovalGate -- "Low Risk / Pre-Approved" --> ToolRegistry
    ApprovalGate -- "Consequential / High Risk" --> ApprovalModal
    ApprovalModal -- "User Approves" --> ApprovalGate
    
    ToolRegistry --> T1 & T2 & T3 & T4 & T5 & T6 & T7 & T8 & T9
    T4 <--> DocStore
    ToolRegistry --> DB
    ToolRegistry --> AuditLog
    AuditLog --> AnalyticsComp
```

---

### 2. Autonomous Agent Lifecycle & Decision Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Reviewer
    participant UI as Frontend Workspace (React)
    participant API as FastAPI Gateway
    participant Agent as Agent Orchestrator
    participant Provider as Model Provider (Local / Bedrock)
    participant Gate as Approval Checkpoint
    participant Tool as Tool Registry
    participant DB as Relational DB & Audit Log

    User->>UI: Submits natural-language goal
    UI->>API: POST /api/v1/conversations/{id}/messages
    API->>API: Verify JWT & extract tenant user_id
    API->>Agent: Dispatch goal with session context
    Agent->>DB: Fetch user preferences & long-term memory
    Agent->>Provider: Request plan decomposition with memory context
    Provider-->>Agent: Returns structured multi-step plan & tool calls
    Agent->>DB: Create Task & TaskSteps (status=PENDING)
    
    loop For Each Step in Plan
        Agent->>Gate: Evaluate step risk & required tool
        alt High Risk Tool (e.g. export_tool, mutation)
            Gate->>DB: Set Task status = AWAITING_APPROVAL
            Gate->>UI: Prompt User for explicit authorization
            User->>UI: Inspect proposed payload & Click "Approve"
            UI->>API: POST /api/v1/tasks/{id}/approve
            API->>Gate: Authorization confirmed
            Gate->>DB: Set status = IN_PROGRESS
        end
        Agent->>Tool: Execute sandboxed tool with inputs
        Tool-->>Agent: Return verified execution output & latency
        Agent->>DB: Record ToolExecution & ExecutionEvent
    end

    Agent->>DB: Extract new conversational facts to Memory
    Agent->>DB: Set Task status = COMPLETED
    Agent-->>UI: Stream complete execution response with citations & traces
    UI-->>User: Renders verified response + interactive audit drawer
```

---

### 3. Human-in-the-Loop State Machine

```mermaid
stateDiagram-v2
    [*] --> PENDING: User submits complex objective
    PENDING --> IN_PROGRESS: Orchestrator schedules plan
    
    state RiskCheck <<choice>>
    IN_PROGRESS --> RiskCheck: Inspect next tool action
    
    RiskCheck --> TOOL_EXECUTION: Safe Tool (e.g. calculator, date_time, RAG)
    RiskCheck --> AWAITING_APPROVAL: Consequential Tool (e.g. export_tool)
    
    state AWAITING_APPROVAL {
        [*] --> UserNotification
        UserNotification --> PayloadInspection: User views inputs & risk
        PayloadInspection --> [*]
    }
    
    AWAITING_APPROVAL --> TOOL_EXECUTION: User Clicks "Approve & Execute"
    AWAITING_APPROVAL --> CANCELLED: User Clicks "Reject" or Timeout
    
    TOOL_EXECUTION --> STEP_VERIFIED: Tool returns valid output
    TOOL_EXECUTION --> FAILED: Sandboxed error or exception
    
    state MoreSteps <<choice>>
    STEP_VERIFIED --> MoreSteps: Check remaining DAG steps
    MoreSteps --> IN_PROGRESS: Next step available
    MoreSteps --> COMPLETED: All steps finished
    
    COMPLETED --> [*]
    CANCELLED --> [*]
    FAILED --> [*]
```

---

### 4. Grounded RAG & Citation Engine Pipeline

```mermaid
flowchart LR
    classDef input fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef process fill:#1e1b4b,stroke:#c084fc,stroke-width:2px,color:#f8fafc;
    classDef decision fill:#312e81,stroke:#fbbf24,stroke-width:2px,color:#f8fafc;
    classDef output fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#f8fafc;
    classDef refuse fill:#450a0a,stroke:#f87171,stroke-width:2px,color:#f8fafc;

    subgraph Ingestion ["1. Document Ingestion & Chunking"]
        DocFile["Uploaded PDF / MD / TXT"]:::input --> Parser["pypdf & Text Stream Extractor"]:::process
        Parser --> SlidingChunker["Sliding Window Chunker (500 chars / 50 overlap)"]:::process
        SlidingChunker --> ChunkDB[("Chunk Store with Page Metadata")]:::process
    end

    subgraph Retrieval ["2. Precision BM25 Retrieval"]
        UserQuery["User Natural Query"]:::input --> StopWords["Stop-Word Removal & Keyword Tokenizer"]:::process
        StopWords --> BM25["BM25 Ranking Engine"]:::process
        ChunkDB --> BM25
        BM25 --> Threshold{"Relevance Score >= Threshold?"}:::decision
    end

    subgraph Synthesis ["3. Grounded Synthesis"]
        Threshold -- "YES" --> GroundedGen["Synthesize Answer with Direct Quotations"]:::output
        GroundedGen --> Citations["Attach Verifiable Citations (Doc Name, Chunk ID, Page)"]:::output
        Threshold -- "NO" --> Refusal["Zero-Hallucination Refusal: 'Evidence Not Found'"]:::refuse
    end
```

---

## 🛠️ Tool Ecosystem & Sandboxing

ContextPilot AI includes **9 production-grade, sandboxed tools** registered in `app/tools/registry.py`:

| Tool Identifier | Module | Description | Sandboxing & Safety Guarantee |
|---|---|---|---|
| `safe_calculator` | `safe_calculator.py` | Evaluates arithmetic, percentages, averages, and basic math. | **Python AST parsing (`ast.parse`)**. Zero `eval()`, zero `exec()`, forbidden imports or attribute access. |
| `date_time` | `date_time_tool.py` | Current server time, timezone offsets, and date calculations. | Read-only server clock access. Cannot modify system time. |
| `task_manager` | `task_manager_tool.py` | Autonomous task and subtask creation, status updates, priority tracking. | Scoped strictly to the authenticated `user_id`. Cannot access other tenants. |
| `knowledge_retriever` | `knowledge_retriever_tool.py` | BM25 keyword matching across indexed user documents with page numbers. | Queries isolated document chunks with non-stop word validation. |
| `structured_summarizer` | `structured_summarizer_tool.py` | Extracts concise summaries, key takeaways, and action items from text. | Purely functional text processing. No external network access. |
| `workflow_planner` | `workflow_planner_tool.py` | Decomposes goals into dependency-aware milestones with risk classification. | Deterministic structured schema generation with Pydantic validation. |
| `data_analysis` | `data_analysis_tool.py` | Computes statistical summaries, mean, median, min, max, standard deviation. | Safe numeric computation over tabular JSON arrays. |
| `notification_center` | `notification_tool.py` | Dispatches in-app alerts and notifications to the user interface. | Internal database record creation. No external SMS or spam egress. |
| `export_tool` | `export_tool.py` | Generates structured Markdown, JSON, or CSV data exports. | **Mandatory Human Approval Gate**. Halts execution until explicit user sign-off. |

---

## 🧰 Technology Stack

```
Frontend:   [React 18] ── [TypeScript 5.5] ── [Vite] ── [Tailwind CSS] ── [Recharts] ── [Lucide]
               │
REST API:      ▼ (Bearer JWT Auth)
Backend:    [FastAPI 0.111] ── [Pydantic v2] ── [SQLAlchemy 2.0] ── [pypdf] ── [AST Sandbox]
               │
Storage:       ▼
Database:   [SQLite 3 (Local WAL Mode)]  /  [PostgreSQL 16 (Docker Production)]
               │
AI Engine:     ▼
Providers:  [LocalDemoProvider (Deterministic)]  ◄──►  [Amazon Bedrock (boto3 Converse API)]
```

---

## 🚀 Quickstart Guide

Get ContextPilot AI running locally in **less than 3 minutes** with zero cloud setup.

### Prerequisites
- **Python 3.11** or **3.12**
- **Node.js 18+** (Node 20, 22, or 24 recommended)
- **Git**

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/sunbyte16/ContextPilot-AI.git
cd ContextPilot-AI/backend

# Create and activate virtual environment
# On Windows (PowerShell):
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# On Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Start the FastAPI backend server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- **Backend API:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **System Health Endpoint:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

### 2. Frontend Setup

In a new terminal window:

```bash
cd ContextPilot-AI/frontend

# Install frontend packages
npm install

# Start Vite development server
npm run dev
```

- **Frontend Application:** [http://localhost:5173](http://localhost:5173)

---

## ⚡ 3-Minute Hackathon Demo Walkthrough

Follow this step-by-step evaluator journey to test all core agentic capabilities:

1. **One-Click Demo Sign In:**
   - Navigate to [http://localhost:5173/login](http://localhost:5173/login).
   - Click the **"Fill Demo Account"** button (`demo@contextpilot.ai` / `DemoPass123!`).
   - Click **"Sign In"**. You are routed immediately to the workspace dashboard.

2. **Seed Realistic Demo Data:**
   - In the top header bar, click the **"Seed Demo Data"** button (sparkles icon).
   - Notice the live metrics update: Active Tasks, Knowledge Documents, Stored Memories, and Execution Success Rate.
   - Note the **"Alexa+ Simulation Mode"** pill indicating safe offline mode.

3. **Autonomous Planning & Tool Invocation (`/app/assistant`):**
   - Type or paste:
     > *"Plan a 3-week study schedule for AWS Bedrock AI agents, calculate total study hours at 2.5 hours per day for 21 days, and save it as a high-priority task."*
   - Observe the agent autonomously invoke `date_time`, calculate `2.5 * 21 = 52.5 hours` via `safe_calculator`, structure milestones via `workflow_planner`, and record the task via `task_manager`.
   - Click **"Show Execution Details"** to view millisecond tool latencies and inputs.

4. **Grounded RAG with Citations (`/app/knowledge`):**
   - In the query sandbox, ask:
     > *"What are the core components of Amazon Bedrock Agents?"*
   - Observe the grounded response with an **exact citation badge** pointing to `Amazon_Bedrock_Agent_Guide.md (Chunk 1)`.
   - Now query an ungrounded topic: *"What is the recipe for chocolate chip cookies?"*
   - Observe the zero-hallucination refusal: ContextPilot AI refuses to fabricate facts without evidence.

5. **Server-Side Human Approval Gate (`/app/tasks`):**
   - In `/app/assistant`, send:
     > *"Export our cloud infrastructure spending report to JSON format."*
   - The agent flags `export_tool` as consequential and transitions the task into `AWAITING_APPROVAL`.
   - Click into `/app/tasks`, review the proposed parameters and risk rating in the modal, and click **"Approve & Execute"**.
   - Watch the task transition to `COMPLETED` and generate a verified download link with a SHA-256 checksum.

---

## ☁️ AWS Bedrock Integration

ContextPilot AI connects natively to Amazon Bedrock using the official AWS SDK `boto3`.

1. Copy `.env.example` to `backend/.env`:
   ```bash
   cp .env.example backend/.env
   ```
2. Configure your AWS credentials in `backend/.env`:
   ```ini
   LLM_PROVIDER=bedrock
   BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   ```
3. Restart the backend. In the ContextPilot AI UI under **Settings** (`/app/settings`), click **"Test Connection"** to verify live communication with AWS Bedrock.

*For complete IAM policies and model configurations, see [docs/AWS_INTEGRATION.md](docs/AWS_INTEGRATION.md).*

---

## 🐳 Docker Deployment

To launch the complete application with PostgreSQL in production mode:

```bash
docker-compose up --build -d
```

- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **PostgreSQL Database:** `localhost:5432`

---

## 🧪 Testing & Verification Evidence

### Backend Pytest Suite (12/12 Passing)
```bash
cd backend
pytest -v
```
```
collected 12 items

tests/test_analytics_and_demo.py::test_demo_seed_and_analytics_summary PASSED       [  8%]
tests/test_auth.py::test_register_and_login PASSED                                  [ 16%]
tests/test_auth.py::test_protected_routes PASSED                                    [ 25%]
tests/test_memory_and_rag.py::test_memory_crud_flow PASSED                          [ 33%]
tests/test_memory_and_rag.py::test_knowledge_upload_and_grounded_rag PASSED         [ 41%]
tests/test_security_and_isolation.py::test_cross_user_tenant_isolation PASSED       [ 50%]
tests/test_security_and_isolation.py::test_sensitive_payload_sanitization PASSED   [ 58%]
tests/test_tasks_and_approvals.py::test_task_plan_and_human_approval_gate PASSED   [ 66%]
tests/test_tasks_and_approvals.py::test_task_approval_rejection_cancels_task PASSED[ 75%]
tests/test_tools.py::test_date_time_tool PASSED                                     [ 83%]
tests/test_tools.py::test_safe_calculator_tool PASSED                               [ 91%]
tests/test_tools.py::test_data_analysis_tool PASSED                                 [100%]

======================== 12 passed, 1 warning in 6.28s ========================
```

### Frontend Tests & Production Build
```bash
cd frontend
npm run test    # Vitest component test suite (2/2 passing)
npm run build   # TypeScript & Vite production bundler (succeeded, dist/ generated)
```

---

## 🔒 Security & Safety Guarantees

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                           SECURITY POSTURE                             │
  ├────────────────────────────────────────────────────────────────────────┤
  │  🛡️ AST Math Sandboxing        🚫 Zero Host Shell Execution            │
  │  🔐 Multi-Tenant DB Isolation  🛑 Server-Side Approval Gates           │
  │  🔑 Zero Frontend Secrets      📜 Append-Only Audit Trail              │
  └────────────────────────────────────────────────────────────────────────┘
```

1. **AST Math Sandboxing:** Eliminates `eval()`, `exec()`, and dynamic code execution. Python Abstract Syntax Tree parsing strictly enforces mathematical nodes.
2. **Zero Shell Execution:** No shell, bash, or PowerShell execution capabilities are exposed to the agent.
3. **Strict Per-User Tenant Isolation:** Database queries enforce ownership via JWT user claims.
4. **Server-Side Approval Checks:** Approval logic is enforced in the FastAPI backend, making client-side bypass impossible.
5. **No Secret Leaks:** Client apps receive zero credentials; all LLM and AWS calls execute strictly on the backend.

---

## 📂 Project Directory Tree

```
ContextPilot-AI/
├── .github/workflows/          # CI/CD GitHub Actions workflow
├── backend/
│   ├── app/
│   │   ├── agents/             # Orchestrator & LLM providers (LocalDemo, Bedrock)
│   │   ├── api/v1/endpoints/   # Modular FastAPI endpoints (auth, tasks, tools, rag...)
│   │   ├── core/               # App configuration & settings
│   │   ├── db/                 # Database engine & session maker
│   │   ├── knowledge/          # Document chunker & processor
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic v2 schemas
│   │   ├── security/           # Bcrypt hashing & JWT auth dependencies
│   │   ├── tools/              # 9 sandboxed, audited tools
│   │   └── main.py             # FastAPI entrypoint
│   ├── tests/                  # Pytest test suites (12 tests)
│   ├── Dockerfile              # Backend container definition
│   └── requirements.txt        # Pinned Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/         # Design system (ui/, layout/)
│   │   ├── context/            # AuthContext, ThemeContext
│   │   ├── pages/              # 17 responsive application views
│   │   ├── services/           # Typed API HTTP client
│   │   └── App.tsx             # Root router & shell
│   ├── Dockerfile              # Frontend container definition
│   ├── tailwind.config.js      # Custom theme colors & typography
│   └── vite.config.ts          # Vite bundler configuration
├── docs/                       # Comprehensive documentation
│   ├── AGENT_DESIGN.md         # Autonomous loop, state machine, approval gates
│   ├── API.md                  # Comprehensive OpenAPI specification
│   ├── ARCHITECTURE.md         # Component diagrams & data flows
│   ├── AWS_INTEGRATION.md      # Amazon Bedrock & AWS SDK integration guide
│   ├── DEMO_SCRIPT.md          # 3-minute hackathon evaluation script
│   ├── KNOWN_LIMITATIONS.md    # Transparent system boundaries
│   ├── SECURITY.md             # Threat model, sandboxing, isolation
│   └── TESTING.md              # Test matrix & verification instructions
├── sample_data/                # Sample knowledge docs & dataset files
├── docker-compose.yml          # Multi-container orchestration
└── README.md                   # This document
```

---

## 🤝 Contributing & Community Guidelines

Contributions are welcomed! We strive to make ContextPilot AI an inclusive, safe, and community-driven agentic AI platform.

- **[Contribution Guide (CONTRIBUTING.md)](CONTRIBUTING.md):** Detailed step-by-step instructions for development setup, PR workflow, and architectural rules.
- **[Code of Conduct (CODE_OF_CONDUCT.md)](CODE_OF_CONDUCT.md):** Contributor Covenant v2.1 standards and pledge.
- **[Security Policy (.github/SECURITY.md)](.github/SECURITY.md):** Vulnerability disclosure protocol and contact channels.
- **Issue Templates:** Standardized [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) & [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) templates.
- **Pull Request Template:** [PR Checklist](.github/PULL_REQUEST_TEMPLATE.md) enforcing AST sandboxing, human approval checks, and tests.

---

## 👨‍💻 Author & Connect

<div align="center">

### Crafted by **𝕊𝕦𝕟𝕚𝕝 𝕊𝕙𝕒𝕣𝕞𝕒**
*Principal Software Architect & Full-Stack AI Engineer*

[![GitHub](https://img.shields.io/badge/GitHub-sunbyte16-181717?style=for-the-badge&logo=github)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil_Kumar-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Sunil_Sharma-FF5722?style=for-the-badge&logo=netlify)](https://lively-dodol-cc397c.netlify.app)

*Feel free to reach out for collaborations, architecture discussions, or agentic AI research!*

</div>

---

## 📄 License & Disclaimer

- **License:** Licensed under the [MIT License](LICENSE).
- **Hackathon Disclaimer:** This project is an independent hackathon prototype submission for the **Amazon Developer Hackathon**. It is not an official Amazon product, nor is it officially certified by or affiliated with Amazon.com, Inc. or the Amazon Alexa team.
