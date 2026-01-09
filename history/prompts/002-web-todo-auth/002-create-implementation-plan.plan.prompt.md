---
id: 002
title: Create Implementation Plan
stage: plan
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-web-todo-auth
branch: 002-web-todo-auth
user: admin
command: sp.plan
labels: ["plan", "phase-2", "architecture", "web", "todo", "auth", "jwt"]
links:
  spec: specs/002-web-todo-auth/spec.md
  plan: specs/002-web-todo-auth/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-web-todo-auth/plan.md
  - specs/002-web-todo-auth/research.md
  - specs/002-web-todo-auth/data-model.md
  - specs/002-web-todo-auth/quickstart.md
  - specs/002-web-todo-auth/contracts/openapi.yaml
tests:
  - Constitution check (all 5 principles verified)
---

## Prompt

Create:
- Architecture plan:
  - Next.js frontend with Better Auth
  - FastAPI backend with JWT middleware
  - SQLModel + Neon PostgreSQL
- Spec breakdown:
  - Overview
  - Task CRUD
  - Authentication
  - API endpoints
  - Database schema
  - UI structure

Decisions needing documentation:
- JWT verification strategy (middleware vs dependency)
- User ID source (JWT vs URL validation)
- Monorepo vs separate repos (monorepo chosen)
- API route structure

Implementation strategy:
- Write specs first
- Reference specs explicitly during implementation
- Implement backend before frontend
- Iterate via spec updates only

Testing strategy:
- Auth required → 401 without JWT
- User isolation enforced on all endpoints
- CRUD operations validated per user
- Manual review of Claude Code diffs

Phases:
- Specs → Tasks → Backend → Frontend → Review

## Response snapshot

Created comprehensive implementation plan for Full-Stack Multi-User Todo Web Application (Phase II).

**Plan Artifacts Created**:
- `plan.md` - Main architectural plan with all specifications
- `research.md` - Technical research findings
- `data-model.md` - Database schema and SQLModel entities
- `quickstart.md` - Setup and usage instructions
- `contracts/openapi.yaml` - OpenAPI 3.0 specification

**Architecture**:
- **Frontend**: Next.js 15+ App Router with Better Auth
- **Backend**: FastAPI 0.100+ with JWT middleware
- **Database**: SQLModel + Neon Serverless PostgreSQL
- **Structure**: Monorepo (backend/ + frontend/ under phase-2/)

**Key Decisions Documented**:

| Decision | Choice | Rationale |
|----------|--------|-----------|
| JWT Verification | Middleware | Consistent auth, DRY, fails fast |
| User ID Source | JWT Claims | Stateless, no extra DB lookup |
| Repo Structure | Monorepo | Phase independence, single context |
| API Routes | Flat | Simplicity for Phase II scope |

**Technical Details**:
- 4 authentication endpoints (register, login, me)
- 6 todo CRUD endpoints (list, create, get, update, partial-update, delete)
- User entity with UUID, email, bcrypt password hash
- TodoTask entity with user_id FK, CASCADE delete
- JWT token with 24-hour expiration
- Input validation via Pydantic schemas

**Constitution Check**: All 5 principles verified
- Documentation-First: ✅ spec.md → plan.md → tasks.md sequence
- Phase Independence: ✅ Out-of-scope items documented
- Spec-Driven Development: ✅ All FRs traced to implementation
- Security-First: ✅ JWT middleware enforced
- Progressive Complexity: ✅ No Phase III+ features

**Testing Strategy**:
- Unit tests for individual functions
- Integration tests for all API endpoints
- User isolation tests (CRITICAL - SC-002)
- Manual review checklist for spec compliance

**Implementation Phases**:
1. Planning (COMPLETED)
2. Tasks (NEXT - run `/sp.tasks`)
3. Backend Implementation
4. Frontend Implementation
5. Review and Validation

## Outcome

- ✅ Impact: Complete architectural plan ready for task breakdown - all 12 FRs mapped to implementation
- 🧪 Tests: Constitution check passed (5/5 principles), no violations
- 📁 Files: plan.md (354 lines), research.md, data-model.md, quickstart.md, openapi.yaml (240 lines)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks from plan.md
- 🧠 Reflection: Plan establishes solid foundation with monorepo structure, JWT middleware auth, and SQLModel entities. Key decisions well-documented with trade-offs. Testing strategy emphasizes user isolation as critical path. Next step is `/sp.tasks` to decompose into actionable implementation items.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan created successfully with all decisions resolved
- Graders run and results (PASS/FAIL): Constitution check - PASS (5/5 principles)
- Prompt variant (if applicable): Comprehensive architecture planning with SDD workflow
- Next experiment (smallest change to try): Generate tasks.md with explicit FR mappings for traceability
