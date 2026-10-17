# Contributing to ContextPilot AI 🧭

First off, thank you for considering contributing to **ContextPilot AI**! It is people like you that help make ContextPilot AI a robust, transparent, and trustworthy agentic AI platform.

Please review this document to understand the contribution workflow, code standards, and submission guidelines.

---

## 📜 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Submitting a Pull Request](#submitting-a-pull-request)
- [Development Setup](#development-setup)
- [Coding & Architectural Guidelines](#coding--architectural-guidelines)
  - [Backend Standards (Python / FastAPI)](#backend-standards-python--fastapi)
  - [Frontend Standards (React / TypeScript)](#frontend-standards-react--typescript)
  - [Agent & Tool Safety Principles](#agent--tool-safety-principles)
- [Testing Guidelines](#testing-guidelines)
- [Community & Contact](#community--contact)

---

## 📜 Code of Conduct

This project adheres to the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [sunil.sharma.dev@gmail.com](mailto:sunil.sharma.dev@gmail.com).

---

## 💡 How Can I Contribute?

### Reporting Bugs
Before filing an issue, please check existing GitHub issues to verify that the bug hasn't already been reported.

When opening an issue, please include:
- A clear, descriptive title.
- Steps to reproduce the problem.
- Expected vs. actual behavior.
- Environment details (OS, Python version, Node.js version, browser).
- Screenshots or console logs if applicable.

### Suggesting Enhancements
Feature requests are welcomed! When proposing a new feature or tool:
- Explain the user problem it solves.
- Describe the proposed architectural implementation.
- Consider security implications (e.g., does it require a human approval gate?).

### Submitting a Pull Request
1. Fork the repo and create your branch from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```
2. Implement your changes following our coding and test guidelines.
3. Ensure all automated tests pass:
   ```bash
   # Backend tests
   cd backend && pytest -v

   # Frontend tests & build
   cd ../frontend && npm run test && npm run build
   ```
4. Commit your changes using descriptive commit messages following Conventional Commits (e.g., `feat(tools): add web search tool with domain allowlisting`).
5. Push to your fork and submit a Pull Request targeting `main`.

---

## 🛠️ Development Setup

### 1. Prerequisites
- Python 3.11 or 3.12
- Node.js 18+ (Node 20 / 22 / 24 recommended)
- Git

### 2. Backend Local Setup
```bash
cd backend
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Frontend Local Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📐 Coding & Architectural Guidelines

### Backend Standards (Python / FastAPI)
- Use **Python 3.11+ type annotations** consistently.
- Schema definitions must use **Pydantic v2** with `ConfigDict(from_attributes=True)`.
- Database operations must utilize **SQLAlchemy 2.0 select syntax** (`select(Model).where(...)`).
- Multi-tenant isolation is mandatory: every endpoint dealing with user data must filter by `current_user.id`.

### Frontend Standards (React / TypeScript)
- Strict TypeScript (`strict: true`) with no arbitrary `any` types.
- Component styling via **Tailwind CSS** using standard tokens.
- Accessible UI components with keyboard navigation, visible focus rings, and proper ARIA attributes.
- Use **Lucide React** for icons; never use raw emojis to replace professional iconography.

### Agent & Tool Safety Principles
- **AST-Enforced Evaluation:** Any expression parsing must use Python's Abstract Syntax Tree. Never introduce `eval()`, `exec()`, or dynamic code execution.
- **Zero Host Shell:** Do not add tools that invoke bash, PowerShell, or command prompt directly.
- **Consequential Action Gates:** Any tool that modifies external data, exports records, or deletes entities must declare `requires_approval = True`.

---

## 🧪 Testing Guidelines

- Every new backend feature must be accompanied by automated unit or integration tests in `backend/tests/`.
- Test cases should cover:
  - Happy path execution.
  - Edge cases and invalid inputs.
  - Unauthorized access and cross-tenant isolation boundaries.
- Frontend components should include Vitest unit tests in `frontend/src/test/`.

---

## 🤝 Community & Contact

- **Lead Maintainer:** Sunil Sharma ([@sunbyte16](https://github.com/sunbyte16))
- **LinkedIn:** [Sunil Kumar](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
- **Portfolio:** [Sunil Sharma](https://lively-dodol-cc397c.netlify.app)
