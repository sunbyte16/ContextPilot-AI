# ContextPilot AI — Testing & Verification Guide

ContextPilot AI includes comprehensive backend and frontend test suites verifying authorization, task state machines, human approval gates, tool correctness, contextual memory, and tenant isolation.

## 1. Running Backend Tests (Pytest)

Navigate to the `backend` folder and run the test suite:

```bash
cd backend
.\.venv\Scripts\pytest.exe -v
```

### Verified Test Modules
- `tests/test_auth.py`: User registration, duplicate email rejection, login token generation, password verification, route protection.
- `tests/test_tasks_and_approvals.py`: Task plan generation, verification of step schemas, server-side approval gates stopping execution, approval authorization, rejection workflow.
- `tests/test_tools.py`: Safe mathematical AST evaluator (normal expressions, exponentiation limits, division by zero, prevention of `__import__`), date/time formatting, tabular data statistics.
- `tests/test_memory_and_rag.py`: Memory CRUD, category filtering, document uploading and chunking, grounded Q&A with verbatim citations, insufficient evidence handling.
- `tests/test_security_and_isolation.py`: Strict cross-user tenant isolation (User A cannot list or read User B's tasks or memories), secret parameter sanitization.
- `tests/test_analytics_and_demo.py`: Demo data seeding, metric calculation, notification read tracking, clean reset.

## 2. Running Frontend Tests (Vitest)

Navigate to the `frontend` directory:

```bash
cd frontend
npm run test
```

## 3. Building for Production

Test frontend production compilation:

```bash
cd frontend
npm run build
```
