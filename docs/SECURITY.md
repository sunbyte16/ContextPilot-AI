# ContextPilot AI — Security Architecture & Threat Model

ContextPilot AI adheres to rigorous security principles designed to prevent prompt injection, untrusted execution, credential exposure, and tenant data leaks.

## 1. Authentication & Tenant Isolation
- **Password Hashing**: Bcrypt with minimum 12 rounds of salting.
- **Session Tokens**: JWT with HMAC-SHA256 signing, stored in HttpOnly, SameSite=Lax cookies or Bearer Authorization headers.
- **Tenant Isolation**: Every database entity (`Task`, `Memory`, `Document`, `Conversation`) enforces foreign-key ownership by `User.id`. Endpoints extract the identity exclusively from the validated server-side token.

## 2. Server-Side Human Approval Gates
- Any tool labeled `risk_level == "HIGH"` or `requires_approval = True` (such as `export_tool` or data deletion) cannot execute autonomously.
- The approval check is strictly enforced on the server within `AgentOrchestrator.execute_task`. Bypassing or disabling the UI button cannot trigger execution.

## 3. Defense Against Prompt Injection
- **Untrusted Knowledge Documents**: Content extracted from uploaded PDFs or markdown files is treated as untrusted text. The agent's prompt architecture isolates document content within explicit quote boundaries and instructs models to disregard commands inside documents that attempt to override system policies.
- **AST-Parsed Calculator**: The calculator tool uses Python's `ast` module to evaluate mathematical syntax trees. Arbitrary identifiers, `__import__`, `eval`, `exec`, and file operations are completely blocked at the parser level.

## 4. Credential & Secret Redaction
- In-flight execution logs and database `ToolExecution` input payloads pass through a recursive sanitizer:
  ```python
  sensitive_keys = {"password", "secret", "token", "api_key", "authorization", "credential"}
  ```
- Any matching key is replaced with `******[REDACTED]******` prior to persistence.
