# ContextPilot AI — Live Evaluation & Demo Walkthrough Script

**Platform:** ContextPilot AI — Agentic AI Assistant Platform  
**Hackathon:** Amazon Developer Hackathon  
**Target Duration:** 3 – 5 Minutes  
**Mode Supported:** 100% Offline Local Demo Mode (Zero API keys required) or AWS Bedrock Mode  

---

## Prerequisites & Launching the Application

1. **Start the Backend:**
   ```bash
   cd backend
   # Activate virtualenv
   # Windows:
   .\.venv\Scripts\Activate.ps1
   # Linux/macOS: source .venv/bin/activate

   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
   *Health Check:* Open [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) to verify `{"status": "HEALTHY", "version": "1.0.0"}`.

2. **Start the Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```
   *Open:* Navigate to [http://localhost:5173](http://localhost:5173).

---

## 3-Minute Hackathon Demo Script

### Step 1: Landing Page & Instant Demo Sign-In (0:00 – 0:30)
1. **Visit [http://localhost:5173](http://localhost:5173)**.
   - Note the **ContextPilot AI** branding, refined dark/light theme toggle, and transparent badge: *"Alexa+-Inspired Agentic Assistant (Simulated Web App)"*.
2. Click **"Get Started"** or navigate to `/login`.
3. Click the **"Fill Demo Account"** button (pre-fills `demo@contextpilot.ai` / `DemoPass123!`).
4. Click **"Sign In"**. You are routed immediately to `/app` (Dashboard).

---

### Step 2: One-Click Demo Scenario Seed (0:30 – 0:50)
1. In the top navigation bar, click the **"Seed Demo Data"** button (sparkles icon).
2. A toast confirms: *"Demo environment loaded with sample tasks, knowledge documents, memories, and audit logs."*
3. Notice the live dashboard metrics update:
   - **Active Tasks**, **Knowledge Documents**, **Stored Memories**, and **Execution Success Rate**.
   - Notice the **Alexa+ Simulation Mode** active indicator in the header.

---

### Step 3: Conversational Agent & Multi-Step Tool Planning (0:50 – 1:40)
1. Navigate to **Assistant** (`/app/assistant`) via the left sidebar.
2. In the input box, type or paste the following multi-step goal:
   > *"Plan a 3-week study schedule for AWS Bedrock AI agents, calculate total study hours at 2.5 hours per day for 21 days, and save it as a high-priority task."*
3. Click **Send** or press `Enter`.
4. Observe the agent response in real time:
   - **Step-by-Step Plan:** The agent identifies required tools: `date_time`, `safe_calculator` (`2.5 * 21 = 52.5`), `workflow_planner`, and `task_manager`.
   - **Execution Traces:** Click **"Show Execution Details"** underneath the message to inspect:
     - Exact tool inputs & outputs.
     - Execution latency in milliseconds.
     - Deterministic or model-based reasoning.
   - **Memory Extraction:** Notice the agent automatically saves key user goals and time commitments into long-term contextual memory.

---

### Step 4: Grounded RAG & Exact Document Citations (1:40 – 2:20)
1. Navigate to **Knowledge Base** (`/app/knowledge`).
2. Notice the pre-indexed sample document: `Amazon_Bedrock_Agent_Guide.md` (2 chunks, 100% processed).
3. In the grounded query sandbox on the right, enter:
   > *"What are the core components of Amazon Bedrock Agents?"*
4. Click **"Search Knowledge Base"**.
5. Observe the result:
   - Verified grounded snippet quoting Foundation Model, Action Groups, and Knowledge Bases.
   - **Exact Citation Badge:** `Document: Amazon_Bedrock_Agent_Guide.md | Chunk: 1 | Relevance: 0.89`.
6. Enter an irrelevant query not present in the document:
   > *"What is the recipe for chocolate chip cookies?"*
7. Observe that ContextPilot AI refuses to hallucinate:
   > *"No relevant evidence found in uploaded knowledge documents. The query cannot be answered based on verified context."*

---

### Step 5: Human Approval Gate & Risk Governance (2:20 – 3:00)
1. Return to **Assistant** or go to **Tasks** (`/app/tasks`).
2. Enter the prompt:
   > *"Export our cloud infrastructure spending report to JSON format."*
3. The agent decomposes the request and flags that data export contains sensitive operational information, triggering a **High Risk Approval Gate**.
4. A card appears: **`APPROVAL REQUIRED: Tool 'export_tool'`**.
5. Click **"View Task"** or navigate to `/app/tasks`.
6. Select the task in the list.
7. Inspect the **Approval Request Modal / Drawer**:
   - Tool Name: `export_tool`
   - Proposed Payload: `{"format": "json", "dataset": "cloud_spend"}`
   - Risk Assessment: `Requires human verification prior to exporting structured records.`
8. Click **"Approve & Execute"**.
9. The task transitions from `AWAITING_APPROVAL` $\to$ `IN_PROGRESS` $\to$ `COMPLETED`.
10. The exported file download link and checksum are rendered directly in the execution history.

---

### Step 6: Tool Testbench & Interactive Verification (3:00 – 3:30)
1. Navigate to **Tool Registry** (`/app/tools`).
2. View the 9 registered and sandboxed tools:
   - `date_time`, `safe_calculator`, `task_manager`, `knowledge_retriever`, `structured_summarizer`, `workflow_planner`, `data_analysis`, `notification_center`, `export_tool`.
3. Click on **`safe_calculator`**:
   - Enter expression: `(14500 * 0.18) + (3200 / 4)`
   - Click **Run Tool**.
   - Result: `3410.0` returned in `< 5ms` with zero host shell execution.
4. Try typing an unauthorized import or dangerous command like `import os; os.system('dir')`:
   - Tool safely rejects: *"Disallowed syntax: Import and attribute operations are forbidden in sandboxed calculator."*

---

### Step 7: Activity Audit Log & Real Analytics (3:30 – 4:00)
1. Navigate to **Activity** (`/app/activity`):
   - Review the immutable audit stream: every user authentication, task creation, tool invocation, and approval decision is logged with timestamps, IP addresses, and user IDs.
2. Navigate to **Analytics** (`/app/analytics`):
   - View real **Recharts** visualizations:
     - Task Completion Rate over time.
     - Tool Invocation Distribution (bar chart).
     - Average Latency by Tool (ms).
     - Token & Execution Efficiency.

---

### Step 8: Settings & Dual Model Provider Demonstration (4:00 – 4:30)
1. Navigate to **Settings** (`/app/settings`).
2. View the **AI Model Provider** section:
   - Default: **Local Demo Provider** (Deterministic, offline, 0 cost).
   - Alternative: **Amazon Bedrock Provider** (Live AWS Bedrock Converse API with Claude 3 / Titan).
3. Test AWS Bedrock connection:
   - If AWS keys are present in `.env`, click **"Test Connection"** to verify Bedrock API handshake.
   - If offline, the interface explains that AWS keys are missing and retains the safe offline provider without crashing or throwing errors.

---

## Summary Checklist for Evaluators

| Criteria | Demonstrated In |
|---|---|
| **Autonomous Multi-Step Planning** | Assistant Page & Execution Traces |
| **Sandboxed Tool Invocation** | Safe Calculator & Tools Registry |
| **Server-Side Human Approval Gates** | Task Export Approval Workflow |
| **Grounded RAG with Citations** | Knowledge Base Page & Search Sandbox |
| **Zero Hallucination Honesty** | Non-relevant query test in Knowledge Base |
| **Persistent Long-Term Memory** | Memory Management Page |
| **Tamper-Evident Auditability** | Activity Logs & Telemetry Inspector |
| **100% Offline Local Mode** | Operates cleanly without external API keys |
| **AWS Bedrock Real Integration** | `BedrockProvider` using `boto3` Converse API |
| **Production Architecture** | FastAPI + React 18 + TypeScript + Tailwind CSS |
