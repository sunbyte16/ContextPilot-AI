# ContextPilot AI — Known Limitations & System Boundaries

**Project:** ContextPilot AI  
**Version:** 1.0.0 (Hackathon Release)  
**Status:** Functional, Tested, and Production-Ready  

In strict accordance with the hackathon principles of engineering honesty and verifiable execution, this document enumerates the design choices, simulation boundaries, and operational considerations of ContextPilot AI.

---

## 1. Product Category & Alexa+ Simulation Boundary

- **Simulated Web Application:** ContextPilot AI is inspired by next-generation voice-and-agent interfaces like Alexa+. It runs entirely as a standard web application on local developer laptops or cloud instances.
- **No Physical Hardware Required:** It does **not** integrate with or require Amazon Echo speakers, Fire TV devices, Bee wearables, or Ring cameras.
- **Audio Simulation:** Speech synthesis and voice input in the web interface rely on standard HTML5 Web Speech API (when available in modern browsers) and synthesized visual cues rather than proprietary Alexa hardware far-field microphone arrays.
- **Not an Official Amazon Product:** ContextPilot AI is an independent software submission developed for the Amazon Developer Hackathon. It does not claim official certification or endorsement by Amazon.com, Inc.

---

## 2. Model Providers & Offline Operation

### Local Demo Provider (`LocalDemoProvider`)
- **Purpose:** Enables 100% offline development, testing, and continuous integration without requiring AWS accounts, Bedrock model access permissions, or credit card charges.
- **Mechanism:** Employs deterministic rule-based intent recognition, regex pattern matching, structured plan generation, and context injection.
- **Limitation:** Does not possess general knowledge outside its domain templates. Free-form conversational queries outside task planning, data calculation, memory storage, and knowledge search will return fallback educational responses directing the user to supported agentic workflows.

### Amazon Bedrock Provider (`BedrockProvider`)
- **Requirement:** Requires genuine AWS IAM credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) and an active AWS Region (`AWS_REGION`, e.g., `us-east-1` or `us-west-2`) with model access granted in the AWS Bedrock Console for `anthropic.claude-3-sonnet-20240229-v1:0` or Amazon Titan.
- **Network Dependency:** When active, the system requires outbound HTTPS access (port 443) to AWS Bedrock endpoints. If offline or credentials are misconfigured, the application gracefully alerts the user and falls back to `LocalDemoProvider`.

---

## 3. Sandboxing & Security Boundaries

### Tool Execution Safety
- **Safe Calculator:** Employs Python `ast.parse` restricted exclusively to literal values, arithmetic operators (`+`, `-`, `*`, `/`, `//`, `%`, `**`), and math functions (`abs`, `round`, `sum`, `min`, `max`). Any attempt to access `__import__`, `eval`, `exec`, attribute traversal, or OS commands is halted before evaluation.
- **No Host Shell Access:** The agentic orchestrator possesses **no** arbitrary bash, shell, or PowerShell execution tools. It cannot execute uncontrolled commands on the host machine.
- **Server-Side Approval Gates:** The human approval gate for consequential tools (such as `export_tool`) is enforced in the FastAPI backend logic. The agent orchestrator cannot bypass an approval request programmatically; execution strictly yields until an authorized user invokes `/api/v1/tasks/{id}/approve`.

---

## 4. Document Processing & Grounded RAG

### File Ingestion & Parsing
- **PDF & Markdown:** Uses `pypdf` for text stream extraction and native UTF-8 decoders for markdown and text files.
- **Scanned Image PDFs:** PDFs consisting purely of scanned images without an embedded text layer (OCR) will yield minimal or empty extracted text chunks. Full image OCR (e.g., Tesseract or Amazon Textract) was omitted to keep the application lightweight and installable without complex C++ binary dependencies.
- **Chunking Strategy:** Fixed-window character chunking (500 characters with 50-character sliding overlap). Very short documents (< 50 characters) produce a single chunk.
- **Search Scoring:** Uses an enhanced BM25 keyword algorithm with stop-word filtering. It guarantees high-precision keyword recall without requiring external vector databases (e.g., Pinecone or pgvector), but does not perform cross-lingual semantic embedding similarity in offline mode.

---

## 5. Storage & Concurrency

### Local SQLite vs PostgreSQL
- **Default Local Mode:** Uses SQLite (`contextpilot.db`) with write-ahead logging (WAL) when run locally. SQLite provides zero-configuration local execution, but serializes concurrent write transactions across threads.
- **Production Mode:** A production-grade `docker-compose.yml` is provided to spin up PostgreSQL 16. In PostgreSQL mode, row-level locking and concurrent transactions are supported out of the box.

---

## 6. Real-Time Telemetry & WebSockets

- **Polling vs WebSockets:** Real-time task progress and step updates are delivered via short-interval HTTP polling and optimistic UI updates. WebSockets or SSE (Server-Sent Events) can be layered onto the existing event bus (`ExecutionEvent` table) in future iterations.

---

## 7. Automated Testing Scope

- **Backend:** 12 automated unit and integration tests verify authentication, multi-tenant isolation, tool sandboxing, AST security, BM25 retrieval, and approval workflows.
- **Frontend:** Vitest tests verify unit component rendering and theme contexts.
- **Mocking Policy:** External AWS Bedrock network calls are mocked during automated CI/CD runs to prevent test failures when running in air-gapped CI environments.
