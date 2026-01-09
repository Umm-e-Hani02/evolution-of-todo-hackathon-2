# Tasks: Full-Stack Multi-User Todo Web Application

**Input**: Design documents from `/specs/002-web-todo-auth/`
**Prerequisites**: plan.md (completed), spec.md (completed), data-model.md, contracts/openapi.yaml

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create phase-2/ directory structure per plan.md
- [ ] T002 [P] Initialize backend project with Python 3.13+ and FastAPI dependencies
- [ ] T003 [P] Initialize frontend project with Next.js 15+ and TypeScript
- [ ] T004 Create .env.example with JWT_SECRET, DATABASE_URL, and frontend API URL
- [ ] T005 Configure linting (ruff/black for Python, ESLint for TypeScript)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation

- [ ] T006 Create SQLModel User entity in `phase-2/backend/src/models/user.py` (FR-001)
- [ ] T007 Create SQLModel TodoTask entity in `phase-2/backend/src/models/todo.py` (FR-004, FR-007)
- [ ] T008 [P] Implement database connection module in `phase-2/backend/src/core/database.py` (FR-009)
- [ ] T009 Create database initialization script for schema creation

### Security Foundation

- [ ] T010 Implement password hashing functions (bcrypt) in `phase-2/backend/src/core/security.py` (FR-001)
- [ ] T011 Implement JWT encode/decode functions in `phase-2/backend/src/core/security.py` (FR-002)
- [ ] T012 [P] Create environment configuration in `phase-2/backend/src/core/config.py` (FR-012)

### API Foundation

- [ ] T013 Create FastAPI application entry point in `phase-2/backend/src/main.py`
- [ ] T014 [P] Create Pydantic request/response schemas in `phase-2/backend/src/schemas/user.py` and `todo.py`
- [ ] T015 Implement JWT authentication dependency in `phase-2/backend/src/deps.py` (FR-002, FR-003)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can register accounts and login to receive JWT tokens

**Independent Test**: Can be fully tested by registering a user, logging in, and using the token to access `/auth/me`

### Backend Implementation

- [ ] T016 [US1] Implement POST /auth/register endpoint in `phase-2/backend/src/api/auth.py` (FR-001)
- [ ] T017 [US1] Implement POST /auth/login endpoint in `phase-2/backend/src/api/auth.py` (FR-002)
- [ ] T018 [US1] Implement GET /auth/me endpoint in `phase-2/backend/src/api/auth.py` (FR-002)
- [ ] T019 [US1] Add email uniqueness validation on registration (FR-001)

### Backend Tests

- [ ] T020 [US1] Contract test for POST /auth/register in `phase-2/backend/tests/test_auth.py`
- [ ] T021 [US1] Contract test for POST /auth/login in `phase-2/backend/tests/test_auth.py`
- [ ] T022 [US1] Contract test for GET /auth/me in `phase-2/backend/tests/test_auth.py`
- [ ] T023 [US1] Test invalid credentials rejection in `phase-2/backend/tests/test_auth.py` (FR-002)

### Frontend Foundation

- [ ] T024 [US1] Setup Better Auth with JWT configuration in `phase-2/frontend/src/lib/auth.ts`
- [ ] T025 [US1] Create API client with JWT token handling in `phase-2/frontend/src/lib/api.ts`
- [ ] T026 [US1] Define TypeScript interfaces for auth responses in `phase-2/frontend/src/types/index.ts`

### Frontend Pages

- [ ] T027 [US1] Create registration page in `phase-2/frontend/src/app/register/page.tsx`
- [ ] T028 [US1] Create login page in `phase-2/frontend/src/app/login/page.tsx`
- [ ] T029 [US1] Add auth state management and token storage (FR-002)

**Checkpoint**: User Story 1 complete - users can register, login, and receive JWT tokens

---

## Phase 4: User Story 2 - Todo CRUD Operations (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create, read, update, and delete their own todo tasks

**Independent Test**: Can be fully tested by creating an account, obtaining a JWT token, and performing all CRUD operations on todo tasks

### Backend Implementation

- [ ] T030 [US2] Implement GET /todos endpoint in `phase-2/backend/src/api/todos.py` (FR-005)
- [ ] T031 [US2] Implement POST /todos endpoint in `phase-2/backend/src/api/todos.py` (FR-004)
- [ ] T032 [US2] Implement GET /todos/{id} endpoint in `phase-2/backend/src/api/todos.py` (FR-005)
- [ ] T033 [US2] Implement PUT /todos/{id} endpoint in `phase-2/backend/src/api/todos.py` (FR-006)
- [ ] T034 [US2] Implement PATCH /todos/{id} endpoint in `phase-2/backend/src/api/todos.py` (FR-006)
- [ ] T035 [US2] Implement DELETE /todos/{id} endpoint in `phase-2/backend/src/api/todos.py` (FR-007)

### Backend Tests

- [ ] T036 [US2] Contract test for GET /todos in `phase-2/backend/tests/test_todos.py`
- [ ] T037 [US2] Contract test for POST /todos in `phase-2/backend/tests/test_todos.py`
- [ ] T038 [US2] Contract test for GET /todos/{id} in `phase-2/backend/tests/test_todos.py`
- [ ] T039 [US2] Contract test for PUT /todos/{id} in `phase-2/backend/tests/test_todos.py`
- [ ] T040 [US2] Contract test for PATCH /todos/{id} in `phase-2/backend/tests/test_todos.py`
- [ ] T041 [US2] Contract test for DELETE /todos/{id} in `phase-2/backend/tests/test_todos.py`
- [ ] T042 [US2] Test input validation in `phase-2/backend/tests/test_todos.py` (FR-011)

### Frontend Implementation

- [ ] T043 [US2] Create todo TypeScript interfaces in `phase-2/frontend/src/types/index.ts`
- [ ] T044 [US2] Extend API client with todo operations in `phase-2/frontend/src/lib/api.ts`
- [ ] T045 [US2] Create task list component in `phase-2/frontend/src/components/todo/TaskList.tsx`
- [ ] T046 [US2] Create task item component in `phase-2/frontend/src/components/todo/TaskItem.tsx`
- [ ] T047 [US2] Create task form component in `phase-2/frontend/src/components/todo/TaskForm.tsx`

### Frontend Pages

- [ ] T048 [US2] Create dashboard layout with auth guard in `phase-2/frontend/src/app/dashboard/layout.tsx` (FR-003)
- [ ] T049 [US2] Create dashboard page with task list in `phase-2/frontend/src/app/dashboard/page.tsx`
- [ ] T050 [US2] Add task creation UI with form submission
- [ ] T051 [US2] Add task editing UI with inline or modal form
- [ ] T052 [US2] Add task deletion with confirmation

**Checkpoint**: User Story 2 complete - all CRUD operations work end-to-end with JWT auth

---

## Phase 5: User Story 3 - User Data Isolation (Priority: P1) 🎯 CRITICAL SECURITY

**Goal**: Users can only access their own data; cross-user access is impossible

**Independent Test**: Can be tested by creating two user accounts, creating tasks as User A, and verifying User B cannot access those tasks

### Backend Security Tests

- [ ] T053 [US3] Test user isolation on GET /todos in `phase-2/backend/tests/test_isolation.py` (SC-002)
- [ ] T054 [US3] Test user isolation on GET /todos/{id} in `phase-2/backend/tests/test_isolation.py` (SC-002)
- [ ] T055 [US3] Test user isolation on PUT /todos/{id} in `phase-2/backend/tests/test_isolation.py` (SC-002)
- [ ] T056 [US3] Test user isolation on DELETE /todos/{id} in `phase-2/backend/tests/test_isolation.py` (SC-002)
- [ ] T057 [US3] Test anonymous request rejection on all todo endpoints (SC-003)

### Frontend Security

- [ ] T058 [US3] Implement auth guard on dashboard routes (redirect to login if not authenticated)
- [ ] T059 [US3] Handle 401 errors globally and redirect to login

**Checkpoint**: User Story 3 complete - zero cross-user data access verified

---

## Phase 6: User Story 4 - Data Persistence (Priority: P1) 🎯 MVP

**Goal**: Todo data persists across server restarts

**Independent Test**: Can be tested by creating tasks, restarting the server, and verifying tasks are still accessible

### Database Verification

- [ ] T060 [US4] Verify database schema creation script matches data-model.md
- [ ] T061 [US4] Test data survives server restart (manual verification)
- [ ] T062 [US4] Test CASCADE delete removes user's tasks when user is deleted

### Integration Tests

- [ ] T063 [US4] Integration test for complete user flow: register → login → CRUD → logout

**Checkpoint**: User Story 4 complete - data persistence verified

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Documentation

- [ ] T064 Update quickstart.md with verified setup instructions
- [ ] T065 Create README.md for phase-2/ directory

### Error Handling

- [ ] T066 Implement consistent error response format across all endpoints (FR-011)
- [ ] T067 Add proper HTTP status codes (400, 401, 403, 404, 409, 422)
- [ ] T068 Add frontend error handling with user-friendly messages

### Validation

- [ ] T069 Add title length validation (max 500 characters)
- [ ] T070 Add email format validation
- [ ] T071 Add password strength validation (minimum 8 characters)

### CORS & Security Headers

- [ ] T072 Configure CORS for frontend origin
- [ ] T073 Add security headers (optional for Phase II)

### Final Verification

- [ ] T074 Run all backend tests and verify 100% pass rate
- [ ] T075 Run manual verification of all user stories
- [ ] T076 Verify spec compliance (all FRs traceable to code)

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|-----------|--------|
| Setup (1) | None | Foundational |
| Foundational (2) | Setup | All user stories |
| User Story 1 (3) | Foundational | - |
| User Story 2 (4) | Foundational | - |
| User Story 3 (5) | Foundational | Polish |
| User Story 4 (6) | Foundational | Polish |
| Polish (7) | All user stories | Release |

### User Story Dependencies

- **User Story 1 (Auth)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (CRUD)**: Can start after Foundational - Depends on US1 for JWT token handling
- **User Story 3 (Isolation)**: Can start after Foundational - Can test independently with multiple users
- **User Story 4 (Persistence)**: Can start after Foundational - Can test with single user

### Within Each User Story

- Tests (T020-T023, T036-T042, T053-T057) MUST be written and FAIL before implementation
- Models (T006-T007) before schemas (T014)
- Schemas before endpoints (T016-T018, T030-T035)
- Core implementation before integration (T063)
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup tasks (T001-T005)**: All can run in parallel
- **Foundational tasks (T006-T015)**: T006/T007 can parallelize with T008/T010/T011; T009/T012/T013/T014/T015 depend on earlier tasks
- **User Story 1 backend (T016-T019)**: Can parallelize with T020-T023 tests
- **User Story 2 backend (T030-T035)**: Can parallelize with T036-T042 tests
- **Frontend pages (T027-T029, T048-T052)**: Can work in parallel with backend tests

---

## Spec Traceability Map

| FR | Requirement | Tasks |
|----|-------------|-------|
| FR-001 | Register accounts | T006, T010, T016, T020, T027 |
| FR-002 | JWT authentication | T011, T015, T017, T021, T024, T025, T028 |
| FR-003 | Auth required on CRUD | T015, T048, T058 |
| FR-004 T007, T | Create tasks |014, T031, T037, T045, T047, T050 |
| FR-005 | List tasks | T007, T030, T036, T043, T044, T049 |
| FR-006 | Update tasks | T007, T014, T033, T034, T039, T040, T046, T051 |
| FR-007 | Delete tasks | T007, T035, T041, T046, T052 |
| FR-008 | User isolation | T006-T007 (FK), T053-T057 tests, T058 |
| FR-009 | PostgreSQL persistence | T008, T009, T060-T063 |
| FR-010 | REST API endpoints | T013, T016-T035 |
| FR-011 | Input validation | T014, T019, T042, T066-T071 |
| FR-012 | Environment config | T004, T012 |

---

## Implementation Order Recommendation

### Option A: Sequential (Recommended for single developer)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Auth)
4. Complete Phase 4: User Story 2 (CRUD)
5. Complete Phase 5: User Story 3 (Isolation) - CRITICAL SECURITY
6. Complete Phase 6: User Story 4 (Persistence)
7. Complete Phase 7: Polish
8. **VALIDATE**: Full system test

### Option B: Parallel (With multiple developers)

1. Team completes Phase 1 + Phase 2 together
2. Once Foundational is done:
   - Developer A: User Story 1 (Auth)
   - Developer B: User Story 2 (CRUD)
   - Developer C: User Story 3 (Isolation) + User Story 4 (Persistence)
3. Stories complete and integrate
4. Team completes Phase 7 together

---

## Notes

- **[P] tasks** = different files, no dependencies
- **[Story] label** maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Write tests FIRST, ensure they FAIL before implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **CRITICAL**: User Story 3 (Isolation) is a security requirement - do not skip
