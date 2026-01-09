# Implementation Plan: Full-Stack Multi-User Todo Web Application

**Branch**: `002-web-todo-auth` | **Date**: 2026-01-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/sp.specify` command output

## Summary

Transform the Phase I in-memory Python console Todo application into a full-stack web application with multi-user authentication and persistent storage. The system will expose RESTful API endpoints for todo CRUD operations, enforce JWT-based authentication on all protected routes, and persist user data in Neon PostgreSQL. The frontend will be built with Next.js App Router and integrate with Better Auth for authentication state management.

## Technical Context

**Language/Version**: Python 3.13+ (FastAPI), TypeScript 5.x (Next.js)
**Primary Dependencies**: FastAPI 0.100+, SQLModel, Better Auth, Next.js 15+, PostgreSQL client
**Storage**: Neon Serverless PostgreSQL (PostgreSQL 15+)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web browsers (modern), Linux server (API)
**Project Type**: Full-stack web application (monorepo)
**Performance Goals**: API response <500ms p95, support 100 concurrent users
**Constraints**: JWT secret via environment variables, no hardcoded credentials
**Scale/Scope**: Individual user focus, no team/collaboration features

## Constitution Check

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| Documentation-First | spec.md exists before implementation | ✅ PASS | spec.md created 2026-01-06 |
| Phase Independence | Phase II features isolated from future phases | ✅ PASS | Out-of-scope items documented |
| Spec-Driven Development | Plan derived from spec requirements | ✅ PASS | All FRs traced to implementation |
| Security-First | Auth required on all API routes | ✅ PASS | JWT middleware enforced |
| Progressive Complexity | No Phase III+ features in scope | ✅ PASS | AI, k8s explicitly excluded |

**GATE**: All constitution checks pass. Proceed to Phase 1 design.

## Project Structure

### Documentation (this feature)

```
specs/002-web-todo-auth/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Technical research notes
├── data-model.md        # Database schema and models
├── quickstart.md        # Setup and run instructions
├── contracts/           # API contracts (OpenAPI)
│   └── openapi.yaml     # OpenAPI 3.0 specification
└── tasks.md             # (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (monorepo structure)

```
phase-2/
├── backend/                      # FastAPI application
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── models/               # SQLModel entities
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User entity
│   │   │   └── todo.py           # TodoTask entity
│   │   ├── schemas/              # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User-related schemas
│   │   │   └── todo.py           # Todo-related schemas
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py           # Authentication endpoints
│   │   │   └── todos.py          # Todo CRUD endpoints
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py         # Environment configuration
│   │   │   ├── security.py       # JWT handling, password hashing
│   │   │   └── database.py       # Database connection
│   │   └── deps.py               # FastAPI dependencies
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py           # Pytest fixtures
│   │   ├── test_auth.py          # Authentication tests
│   │   └── test_todos.py         # Todo CRUD tests
│   ├── requirements.txt          # Python dependencies
│   └── pyproject.toml            # Python project config
│
├── frontend/                     # Next.js application
│   ├── src/
│   │   ├── app/                  # Next.js App Router
│   │   │   ├── layout.tsx        # Root layout with auth provider
│   │   │   ├── page.tsx          # Home page (redirect or dashboard)
│   │   │   ├── globals.css       # Global styles
│   │   │   ├── login/
│   │   │   │   └── page.tsx      # Login page
│   │   │   ├── register/
│   │   │   │   └── page.tsx      # Registration page
│   │   │   └── dashboard/
│   │   │       ├── layout.tsx    # Dashboard layout (auth guard)
│   │   │       ├── page.tsx      # Task list
│   │   │       └── components/   # Dashboard components
│   │   ├── components/
│   │   │   ├── ui/               # Reusable UI components
│   │   │   ├── auth/             # Auth-related components
│   │   │   └── todo/             # Todo-specific components
│   │   ├── lib/
│   │   │   ├── api.ts            # API client with JWT handling
│   │   │   ├── auth.ts           # Better Auth configuration
│   │   │   └── utils.ts          # Utility functions
│   │   └── types/
│   │       └── index.ts          # TypeScript type definitions
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.js
│
├── .env.example                  # Environment template
├── docker-compose.yml            # Local development (optional)
└── README.md                     # Phase documentation
```

**Structure Decision**: Monorepo with separate `backend/` and `frontend/` directories under `phase-2/`. This allows independent development and deployment while sharing documentation and configuration at the feature level.

---

## Detailed Specification Breakdown

### 1. Overview

**Purpose**: Provide a web-based todo application where users can create accounts, authenticate via JWT tokens, and manage their personal tasks with full CRUD capabilities.

**Architecture Overview**:
```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │   Login  │  │ Register │  │Dashboard │  │ Task Editor  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘   │
│       │             │             │                │           │
│       └─────────────┴─────────────┴────────────────┘           │
│                           │                                     │
│              ┌────────────▼────────────┐                       │
│              │   Better Auth + JWT     │                       │
│              │   (Client-side token)   │                       │
│              └────────────┬────────────┘                       │
└───────────────────────────┼────────────────────────────────────┘
                            │ HTTP + JWT Header
┌───────────────────────────▼────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    JWT Middleware                       │   │
│  │              (Validates token, extracts user ID)        │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                      │
│  ┌────────────────────────▼───────────────────────────────┐    │
│  │                    API Endpoints                        │    │
│  │  POST /auth/register  │  POST /auth/login               │    │
│  │  GET  /todos          │  POST /todos                    │    │
│  │  GET  /todos/:id      │  PUT   /todos/:id               │    │
│  │  DELETE /todos/:id    │  PATCH /todos/:id               │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
│              ┌────────────▼────────────┐                         │
│              │   SQLModel + SQLAlchemy │                         │
│              │   (PostgreSQL via    │                         │
│              │    Neon connection)    │                         │
│              └────────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow for Authenticated Request**:
1. User logs in via frontend → receives JWT token
2. Frontend stores token (HTTP-only cookie or memory)
3. Frontend includes token in `Authorization: Bearer <token>` header
4. Backend middleware validates token and extracts `user_id`
5. CRUD operations are scoped to `user_id` via SQL WHERE clauses

### 2. Authentication

**Authentication Flow**:

```
┌─────────────────────────────────────────────────────────────────┐
│                     Authentication Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Registration:                                                  │
│  ┌─────────┐    POST /auth/register    ┌──────────────────┐    │
│  │Frontend │ ───────────────────────► │ Backend          │    │
│  │         │ ◄─────────────────────── │ 1. Validate input│    │
│  │         │    201 Created + Token   │ 2. Hash password │    │
│  │         │                          │ 3. Create User   │    │
│  │         │                          │ 4. Generate JWT  │    │
│  └─────────┘                          └──────────────────┘    │
│                                                                 │
│  Login:                                                         │
│  ┌─────────┐    POST /auth/login       ┌──────────────────┐    │
│  │Frontend │ ───────────────────────► │ Backend          │    │
│  │         │ ◄─────────────────────── │ 1. Find user     │    │
│  │         │    200 OK + Token        │ 2. Verify bcrypt │    │
│  │         │                          │ 3. Generate JWT  │    │
│  └─────────┘                          └──────────────────┘    │
│                                                                 │
│  Authenticated Request:                                         │
│  ┌─────────┐    GET /todos             ┌──────────────────┐    │
│  │Frontend │ ───────────────────────► │ Backend          │    │
│  │         │    Authorization: Bearer  │ 1. Extract token │    │
│  │         │ ◄─────────────────────── │ 2. Verify JWT    │    │
│  │         │    200 OK + JSON         │ 3. Get user_id   │    │
│  └─────────┘                          │ 4. Query todos   │    │
│                                        └──────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**JWT Token Structure**:
```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "exp": 1735689600,
  "iat": 1735603200
}
```

**Security Measures**:
- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens expire after 24 hours
- JWT secret stored in `JWT_SECRET` environment variable
- Authentication errors don't reveal whether email exists

### 3. API Endpoints

**Authentication Endpoints**:

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| POST | `/auth/register` | Create new account | `{email, password}` | 201 + `{token, user}` |
| POST | `/auth/login` | Authenticate user | `{email, password}` | 200 + `{token, user}` |
| GET | `/auth/me` | Get current user | - | 200 + `{user}` |

**Todo Endpoints** (all require `Authorization: Bearer <token>`):

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| GET | `/todos` | List all user's tasks | - | 200 + `[todos]` |
| POST | `/todos` | Create new task | `{title, description?}` | 201 + `{todo}` |
| GET | `/todos/{id}` | Get specific task | - | 200 + `{todo}` |
| PUT | `/todos/{id}` | Replace task | `{title, description, completed}` | 200 + `{todo}` |
| PATCH | `/todos/{id}` | Partial update | `{title?, description?, completed?}` | 200 + `{todo}` |
| DELETE | `/todos/{id}` | Delete task | - | 204 No Content |

**Error Responses**:

| Status | Error Type | Example |
|--------|------------|---------|
| 400 | ValidationError | `{"detail": "Title is required"}` |
| 401 | Unauthorized | `{"detail": "Not authenticated"}` |
| 403 | Forbidden | `{"detail": "Not authorized to access this resource"}` |
| 404 | NotFound | `{"detail": "Task not found"}` |
| 409 | Conflict | `{"detail": "Email already registered"}` |
| 422 | UnprocessableEntity | `{"detail": [{"loc": ["body", "email"], "msg": "invalid email"}]}` |

### 4. Database Schema

**User Table**:
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

**TodoTask Table**:
```sql
CREATE TABLE todo_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_todos_user_id ON todo_tasks(user_id);
CREATE INDEX idx_todos_user_completed ON todo_tasks(user_id, completed);
```

**SQLModel Entities**:

```python
# user.py
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: list["TodoTask"] = Relationship(back_populates="user", cascade_delete="all")

# todo.py
class TodoTask(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", on_delete=CASCADE)
    title: str = Field(max_length=500)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="tasks")
```

### 5. UI Structure

**Page Hierarchy**:
```
├── (public)/
│   ├── page.tsx              # Landing page → redirects if logged in
│   ├── login/
│   │   └── page.tsx          # Login form
│   └── register/
│       └── page.tsx          # Registration form
│
└── (authenticated)/
    └── dashboard/
        ├── layout.tsx        # Auth guard, navigation
        ├── page.tsx          # Task list view
        └── components/
            ├── TaskList.tsx
            ├── TaskItem.tsx
            ├── TaskForm.tsx
            └── Header.tsx
```

**Key UI Flows**:

```
Login Flow:
1. User visits /login
2. Enters email + password
3. Clicks "Sign In"
4. Frontend POSTs to /auth/login
5. On success: store JWT, redirect to /dashboard
6. On failure: show error message

Dashboard Flow:
1. User accesses /dashboard
2. Layout checks auth state
3. If not authenticated: redirect to /login
4. If authenticated: fetch todos via GET /todos
5. Display task list with actions
6. User can: create, edit, delete, toggle completion

Task Creation:
1. User clicks "Add Task"
2. Modal/form appears with title + optional description
3. User submits form
4. Frontend POSTs to /todos with JWT
5. On success: add task to list
6. On failure: show validation error
```

---

## Key Decisions Requiring Documentation

### Decision 1: JWT Verification Strategy

**Options**:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. Middleware | Global JWT validation before route handlers | Consistent, DRY, fails fast | Less granular control per endpoint |
| B. Dependency | Per-route dependency injection of current user | Flexible, explicit | Repetitive code, easy to forget |

**Decision**: **Option A - Middleware**

**Rationale**:
- Consistency: All protected endpoints have identical auth behavior
- Security: Impossible to accidentally expose an endpoint
- Simplicity: Less code to maintain
- Performance: Token validated once per request

**Implementation**:
```python
# FastAPI middleware or dependency
async def get_current_user(token: str = Depends(JWTBearer())) -> User:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    user_id: str = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
```

### Decision 2: User ID Source

**Options**:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. JWT Claims | Extract user_id from JWT token | Stateless, no DB lookup per operation | Revocation delayed until token expires |
| B. URL/Path | Require user_id in request (e.g., `/users/{id}/todos`) | Explicit, auditable | Trust issues, easy to get wrong |
| C. Session DB | Store session in Redis/database | Immediate revocation | Additional infrastructure, stateful |

**Decision**: **Option A - JWT Claims**

**Rationale**:
- Stateless: No session storage required
- Performance: No extra DB lookup for user identification
- Simplicity: User ID always available from token
- Trade-off: Token revocation delayed (acceptable for this phase)

**Mitigation**: Short token lifetime (24 hours) limits revocation delay

### Decision 3: Monorepo vs Separate Repos

**Options**:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. Monorepo | Single repo with backend/ and frontend/ | Shared docs, coordinated releases, simpler CI | Larger repo, potential coupling |
| B. Separate Repos | Independent backend and frontend repos | Clear boundaries, independent scaling | Version synchronization, duplicated docs |

**Decision**: **Option A - Monorepo**

**Rationale** (per constitution - Phase Independence):
- Phase-specific documentation stays with implementation
- Easier to demonstrate complete phase functionality
- Single git history for the feature
- Simpler for hackathon evaluation (one clone, one context)

**Trade-offs Accepted**:
- Slightly larger repository size (acceptable)
- Potential for coupling (mitigated by API contract)

### Decision 4: API Route Structure

**Options**:

| Option | Structure | Example | Pros | Cons |
|--------|-----------|---------|------|------|
| A. Flat | All endpoints at root | `/todos`, `/auth/login` | Simple, intuitive | Namespace pollution |
| B. Grouped | Logical grouping | `/api/v1/todos`, `/api/v1/auth` | Organized, extensible | Slightly more verbose |

**Decision**: **Option A - Flat (with versioning readiness)**

**Rationale**:
- Simplicity for Phase II scope
- Flat structure maps directly to frontend API calls
- Versioning can be added later (`/v2/` prefix) without breaking changes

**Implementation**:
```
/auth/register
/auth/login
/auth/me
/todos
/todos/{id}
```

---

## Implementation Strategy

### Core Principles

1. **Write specs first**: All implementation decisions trace to spec.md requirements
2. **Reference specs explicitly**: Each task in tasks.md references relevant FRs
3. **Backend before frontend**: API contract defined first, frontend integrates against it
4. **Iterate via spec updates**: Changes require spec update first, then implementation

### Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Implementation Workflow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. SPECS → Generate tasks.md from plan.md                      │
│            └─► Each task maps to FR(s)                          │
│                                                                 │
│  2. BACKEND (iterative, per endpoint)                           │
│     a. Implement database models (SQLModel)                     │
│     b. Implement schemas (Pydantic)                             │
│     c. Implement API endpoint                                   │
│     d. Write integration tests                                  │
│     e. Verify with curl/integration tests                       │
│                                                                 │
│  3. FRONTEND (iterative, per page)                              │
│     a. Create API client utilities                              │
│     b. Implement auth pages (login/register)                    │
│     c. Implement dashboard and task components                  │
│     d. Verify end-to-end flow                                   │
│                                                                 │
│  4. REVIEW → Manual diff review, spec compliance check          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Spec Traceability Example

```
FR-002: System MUST authenticate users via JWT tokens
  ↓
  Plan Section: "Authentication > JWT Token Structure"
  ↓
  Task: "Implement JWT security module (encode/decode/verify)"
  ↓
  Implementation: security.py with jwt.encode/jwt.decode
  ↓
  Test: test_auth.py::test_valid_token_authenticates_user
```

---

## Testing Strategy

### Test Categories

| Category | Scope | Tools | Coverage Goal |
|----------|-------|-------|---------------|
| Unit | Individual functions/classes | pytest, Jest | 80% |
| Integration | API endpoints | pytest (requests), Supertest | 100% of endpoints |
| E2E | Full user flows | Manual + curl scripts | All user stories |

### Critical Test Cases

**Authentication Tests**:

```python
# test_auth.py
def test_register_creates_account():
    """FR-001: Users can register with email/password"""
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "secure123"})
    assert response.status_code == 201
    assert "token" in response.json()

def test_login_with_valid_credentials():
    """FR-002: Login returns JWT token"""
    # ... setup user, then test login

def test_login_with_invalid_credentials():
    """FR-002: Invalid login returns 401, no email enumeration"""
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "wrong"})
    assert response.status_code == 401
    assert "detail" in response.json()
```

**User Isolation Tests** (CRITICAL - SC-002):

```python
# test_user_isolation.py
def test_user_cannot_access_other_users_todos():
    """SC-002: Zero cross-user data access"""
    user_a = register_user("user_a@example.com")
    user_b = register_user("user_b@example.com")

    # User A creates a task
    task_a = create_todo(user_a["token"], title="User A's task")

    # User B tries to access User A's task
    response = client.get(f"/todos/{task_a['id']}", headers={"Authorization": f"Bearer {user_b['token']}"})
    assert response.status_code == 404  # Not found (or 403 forbidden)

    # User B lists todos - should only see their own
    response = client.get("/todos", headers={"Authorization": f"Bearer {user_b['token']}"})
    todos = response.json()
    task_ids = [t["id"] for t in todos]
    assert task_a["id"] not in task_ids

def test_anonymous_request_rejected():
    """SC-003: Anonymous requests get 401"""
    response = client.get("/todos")
    assert response.status_code == 401
```

**CRUD Operation Tests**:

```python
# test_todos.py
def test_create_todo():
    """FR-004: Users can create tasks with title"""
    token = login_user()
    response = client.post("/todos", json={"title": "New task"}, headers=auth_header(token))
    assert response.status_code == 201
    assert response.json()["title"] == "New task"

def test_list_todos_shows_only_owned():
    """FR-005: List returns only user's tasks"""
    # ... test implementation

def test_update_todo_modifies_only_owned():
    """FR-006: Update modifies only user's task"""
    # ... test implementation

def test_delete_todo_removes_owned():
    """FR-007: Delete removes user's task"""
    # ... test implementation
```

### Manual Review Checklist

- [ ] JWT token attached to all authenticated requests
- [ ] User isolation verified (create user A task, access as user B)
- [ ] Anonymous requests rejected with 401
- [ ] All CRUD operations persist to database
- [ ] Server restart preserves data
- [ ] Frontend redirects to login when not authenticated

---

## Phases

### Phase 1: Planning (COMPLETED)
- [x] Create specification (spec.md)
- [x] Create implementation plan (plan.md)
- [x] Create quality checklist

### Phase 2: Tasks (NEXT)
- [ ] Run `/sp.tasks` to generate implementation tasks
- [ ] Each task maps to specific FRs
- [ ] Dependencies documented per task

### Phase 3: Backend Implementation
- [ ] Database models (SQLModel entities)
- [ ] Configuration (environment variables)
- [ ] Security module (JWT, password hashing)
- [ ] Authentication endpoints (register, login, me)
- [ ] Todo CRUD endpoints with user isolation
- [ ] Integration tests for all endpoints
- [ ] API documentation (OpenAPI)

### Phase 4: Frontend Implementation
- [ ] Next.js setup with TypeScript
- [ ] API client with JWT handling
- [ ] Better Auth integration
- [ ] Login and registration pages
- [ ] Dashboard with task list
- [ ] Task creation/editing components
- [ ] Error handling and loading states

### Phase 5: Review and Validation
- [ ] Manual diff review of all changes
- [ ] Verify spec compliance (trace FRs to code)
- [ ] Test user isolation (all endpoints)
- [ ] Verify data persistence
- [ ] Document lessons learned
- [ ] Update PHR with implementation notes

---

## Complexity Tracking

No constitution violations requiring justification. All decisions align with principles:
- Security-first: JWT auth enforced, user isolation at database level
- Clean architecture: Separation of models, schemas, API, deps
- Production-ready: Environment-based config, validation, error handling

---

## References

- **Specification**: [spec.md](./spec.md)
- **Constitution**: [.specify/memory/constitution.md](../../../../.specify/memory/constitution.md)
- **Phase I**: [phase-1/](../phase-1/README.md)
