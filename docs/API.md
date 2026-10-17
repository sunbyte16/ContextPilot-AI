# ContextPilot AI — REST API Reference

All versioned REST API endpoints are hosted under `/api/v1`. Interactive OpenAPI/Swagger documentation is served automatically at `/docs`.

## 1. Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | Registers new user account and creates default preferences | No |
| `POST` | `/login` | Authenticates credentials, returns Bearer token and sets HttpOnly cookie | No |
| `POST` | `/logout` | Clears authentication session cookie | Yes |
| `GET` | `/me` | Retrieves authenticated user profile and roles | Yes |
| `PUT` | `/me` | Updates user display name or email | Yes |
| `DELETE` | `/me` | Permanently deletes user account and cascaded data | Yes |

## 2. Conversations (`/api/v1/conversations`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Lists user's active conversations | Yes |
| `POST` | `/` | Initializes a new conversation thread | Yes |
| `GET` | `/{id}` | Retrieves conversation with full ordered message history | Yes |
| `PUT` | `/{id}` | Updates conversation title or archived status | Yes |
| `DELETE` | `/{id}` | Deletes conversation and messages | Yes |
| `POST` | `/{id}/messages` | Dispatches user message, runs orchestrator, returns assistant reply & plan references | Yes |

## 3. Tasks & Orchestration (`/api/v1/tasks`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Lists user's tasks with status, priority, and text search filters | Yes |
| `POST` | `/` | Submits objective to planning engine and generates structured steps | Yes |
| `GET` | `/{id}` | Retrieves full task details, ordered steps, approvals, and events | Yes |
| `PUT` | `/{id}` | Updates task priority or status | Yes |
| `POST` | `/{id}/execute` | Executes or resumes sequential step execution | Yes |
| `POST` | `/{id}/cancel` | Aborts execution of a running task | Yes |
| `POST` | `/{id}/retry` | Resets and retries failed steps | Yes |
| `POST` | `/{id}/approvals/{approval_id}` | Grants human approval or rejects a sensitive action | Yes |
| `GET` | `/{id}/events` | Retrieves real-time execution telemetry event stream | Yes |

## 4. Tools Registry (`/api/v1/tools`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Lists all 9 registered tools, schemas, and risk classifications | Yes |
| `POST` | `/execute` | Direct test execution via controlled dispatcher | Yes |

## 5. Context Memory (`/api/v1/memory`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Lists memories with category and search query filters | Yes |
| `POST` | `/` | Records a new context memory (Fact, Preference, Note, etc.) | Yes |
| `PUT` | `/{id}` | Updates an existing memory record | Yes |
| `DELETE` | `/{id}` | Deletes a memory record | Yes |
| `DELETE` | `/` | Clears all context memories for current user | Yes |

## 6. Knowledge Base & Grounded RAG (`/api/v1/knowledge`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Lists uploaded documents with chunk counts | Yes |
| `POST` | `/upload` | Multipart file upload (PDF, TXT, MD, JSON) with automatic chunking | Yes |
| `GET` | `/{id}` | Retrieves document metadata and extracted chunk index | Yes |
| `DELETE` | `/{id}` | Deletes document and derived chunks | Yes |
| `POST` | `/grounded-query` | Performs grounded semantic search, returning citations and verified answers | Yes |

## 7. Activity & Analytics (`/api/v1/activity`, `/api/v1/analytics`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/activity/audit` | Retrieves tamper-evident system audit log | Yes |
| `GET` | `/activity/notifications` | Lists workspace notifications | Yes |
| `POST` | `/activity/notifications/read-all` | Marks all notifications read | Yes |
| `GET` | `/analytics/summary` | Returns computed execution statistics and 7-day trend | Yes |

## 8. Settings & Demo Mode (`/api/v1/settings`, `/api/v1/demo`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/settings/preferences` | Retrieves user's reasoning and UI preferences | Yes |
| `PUT` | `/settings/preferences` | Updates preferred inference provider, response style, theme | Yes |
| `GET` | `/settings/integrations` | Returns live connection inspection for Bedrock, Local Engine, etc. | Yes |
| `POST` | `/settings/integrations/test` | Triggers live connectivity test for selected adapter | Yes |
| `POST` | `/demo/seed` | Seeds rich demo datasets (tasks, documents, memories) | Yes |
| `POST` | `/demo/reset` | Resets all tenant workspace data | Yes |
