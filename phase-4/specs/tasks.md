---

description: "Task list for AI-Powered Todo Chatbot implementation"
---

# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/001-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT included in this task list as they were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below use web app structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Add Phase III dependencies to backend/requirements.txt (openai>=1.10.0, mcp>=0.1.0, pydantic>=2.5.0)
- [ ] T002 Install dependencies with pip install -r backend/requirements.txt
- [ ] T003 [P] Create backend/src/models/ directory structure
- [ ] T004 [P] Create backend/src/mcp/tools/ directory structure
- [ ] T005 [P] Create backend/src/agent/ directory structure
- [ ] T006 [P] Create backend/src/services/ directory structure
- [ ] T007 Add OPENAI_API_KEY, OPENAI_MODEL, AGENT_TIMEOUT, CONVERSATION_HISTORY_LIMIT to backend/.env

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create Conversation SQLModel in backend/src/models/conversation.py with fields: id, user_id, created_at, updated_at, deleted_at
- [ ] T009 [P] Create Message SQLModel in backend/src/models/message.py with fields: id, conversation_id, role, content, timestamp
- [ ] T010 [P] Create ToolLog SQLModel in backend/src/models/tool_log.py with fields: id, conversation_id, tool_name, input, output, success, timestamp
- [ ] T011 Generate Alembic migration for Phase III tables (conversations, messages, tool_logs) with alembic revision --autogenerate -m "Add Phase III tables"
- [ ] T012 Review generated migration file in backend/alembic/versions/ and verify table creation
- [ ] T013 Run database migration with alembic upgrade head
- [ ] T014 Create MCP server initialization in backend/src/mcp/server.py using Official MCP SDK
- [ ] T015 Create agent system instructions in backend/src/agent/instructions.py defining when to use each MCP tool
- [ ] T016 Create agent runner in backend/src/agent/runner.py using OpenAI Agents SDK with Agent and Runner classes
- [ ] T017 Create ConversationService in backend/src/services/conversation_service.py with methods: create_conversation, get_conversation, load_conversation_history (last 50 messages)
- [ ] T018 [P] Create MessageService in backend/src/services/message_service.py with methods: save_message, get_messages_by_conversation
- [ ] T019 Verify Better Auth integration works by testing existing Phase II authentication endpoints

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Tasks via Chat (Priority: P1) 🎯 MVP

**Goal**: Users can create todo tasks by typing natural language requests. AI agent interprets intent and creates tasks using MCP tools.

**Independent Test**: Send chat message "Add a task to buy groceries" and verify task is created in database and confirmed conversationally.

### Implementation for User Story 1

- [ ] T020 [US1] Create create_task MCP tool in backend/src/mcp/tools/create_task.py with input schema (title: str, user_id: str) and structured output
- [ ] T021 [US1] Register create_task tool with MCP server in backend/src/mcp/server.py
- [ ] T022 [US1] Add create_task tool to agent configuration in backend/src/agent/runner.py
- [ ] T023 [US1] Create POST /api/chat endpoint in backend/src/api/chat.py that accepts message and optional conversation_id
- [ ] T024 [US1] Implement authentication middleware for /api/chat endpoint using Better Auth Bearer token validation
- [ ] T025 [US1] Implement chat request handler in backend/src/api/chat.py: load conversation history, call agent runner, save messages
- [ ] T026 [US1] Implement tool execution logging in backend/src/api/chat.py: persist ToolLog entries for each tool call
- [ ] T027 [US1] Implement response formatting in backend/src/api/chat.py: return conversation_id, agent message, tool_calls array
- [ ] T028 [US1] Add error handling for authentication failures (401), validation errors (400), and internal errors (500) in backend/src/api/chat.py
- [ ] T029 [US1] Update agent instructions in backend/src/agent/instructions.py to describe when to use create_task tool

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can create tasks via chat.

---

## Phase 4: User Story 2 - List and View Tasks (Priority: P2)

**Goal**: Users can ask the AI to show their current tasks. Agent retrieves tasks using MCP tools and presents them conversationally.

**Independent Test**: Create several tasks, then ask "What are my tasks?" and verify all tasks are listed in the response.

### Implementation for User Story 2

- [ ] T030 [US2] Create list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py with input schema (user_id: str, filter: Optional[str]) and structured output
- [ ] T031 [US2] Implement filter logic in list_tasks tool: support "all", "completed", "incomplete" filters
- [ ] T032 [US2] Register list_tasks tool with MCP server in backend/src/mcp/server.py
- [ ] T033 [US2] Add list_tasks tool to agent configuration in backend/src/agent/runner.py
- [ ] T034 [US2] Update agent instructions in backend/src/agent/instructions.py to describe when to use list_tasks tool and how to format task lists conversationally

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can create and list tasks.

---

## Phase 5: User Story 3 - Update and Complete Tasks (Priority: P3)

**Goal**: Users can mark tasks as complete, update task titles, or delete tasks through natural language commands.

**Independent Test**: Create a task, then say "Mark 'buy milk' as done" and verify the task is marked complete in the database.

### Implementation for User Story 3

- [ ] T035 [P] [US3] Create update_task MCP tool in backend/src/mcp/tools/update_task.py with input schema (task_id: str, title: str, user_id: str)
- [ ] T036 [P] [US3] Create complete_task MCP tool in backend/src/mcp/tools/complete_task.py with input schema (task_id: str, user_id: str)
- [ ] T037 [P] [US3] Create delete_task MCP tool in backend/src/mcp/tools/delete_task.py with input schema (task_id: str, user_id: str) implementing soft delete
- [ ] T038 [US3] Register update_task, complete_task, delete_task tools with MCP server in backend/src/mcp/server.py
- [ ] T039 [US3] Add update_task, complete_task, delete_task tools to agent configuration in backend/src/agent/runner.py
- [ ] T040 [US3] Update agent instructions in backend/src/agent/instructions.py to describe when to use update_task, complete_task, and delete_task tools
- [ ] T041 [US3] Implement task matching logic in agent instructions: guide agent to identify tasks by title when user references them

**Checkpoint**: All CRUD operations should now be functional via chat. Users can create, list, update, complete, and delete tasks.

---

## Phase 6: User Story 4 - Conversation Persistence (Priority: P4)

**Goal**: Users can resume conversations after server restarts or from different devices. System reconstructs conversation context from database.

**Independent Test**: Have a conversation, restart the server, then send another message and verify the agent has context from previous messages.

### Implementation for User Story 4

- [ ] T042 [US4] Verify conversation history loading in backend/src/services/conversation_service.py loads last 50 messages in chronological order
- [ ] T043 [US4] Verify message persistence in backend/src/api/chat.py saves both user message and agent response immediately after agent execution
- [ ] T044 [US4] Verify conversation_id is returned in response and can be used to continue conversations in backend/src/api/chat.py
- [ ] T045 [US4] Add conversation_id validation in backend/src/api/chat.py: return 404 if conversation doesn't exist or doesn't belong to authenticated user

**Checkpoint**: Conversation persistence should be fully functional. Server restarts don't lose conversation data.

---

## Phase 7: User Story 5 - Tool Call Visibility (Priority: P5)

**Goal**: Users and developers can see which MCP tools were invoked, with what parameters, and what results were returned.

**Independent Test**: Create a task and verify that tool call logs show the "create_task" tool was invoked with the correct parameters.

### Implementation for User Story 5

- [ ] T046 [US5] Verify tool_calls array is included in chat response in backend/src/api/chat.py with tool_name, input, output, success fields
- [ ] T047 [US5] Verify ToolLog entries are persisted to database for every tool invocation in backend/src/api/chat.py
- [ ] T048 [US5] Add endpoint GET /api/conversations/{conversation_id}/tool-logs in backend/src/api/chat.py to retrieve tool logs for a conversation
- [ ] T049 [US5] Implement authorization check in tool logs endpoint: users can only access their own conversation logs

**Checkpoint**: Tool call visibility is complete. Developers can inspect tool invocations for debugging and evaluation.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T050 [P] Add structured logging (JSON format) for production in backend/src/api/chat.py and backend/src/mcp/tools/
- [ ] T051 [P] Add error handling for OpenAI API failures (503 Service Unavailable) in backend/src/agent/runner.py
- [ ] T052 [P] Add error handling for database connection failures in backend/src/api/chat.py
- [ ] T053 [P] Add request timeout (5 seconds) to /api/chat endpoint in backend/src/api/chat.py
- [ ] T054 [P] Verify CORS configuration in backend/src/main.py allows frontend origin (development and production)
- [ ] T055 [P] Add input validation for message length (max 10000 characters) in backend/src/api/chat.py
- [ ] T056 [P] Add type hints to all functions in backend/src/
- [ ] T057 [P] Add docstrings to all MCP tools in backend/src/mcp/tools/
- [ ] T058 Verify backward compatibility: test existing Phase II REST endpoints (/api/tasks) still work
- [ ] T059 Create deployment documentation in specs/001-ai-chatbot/deployment.md with environment variables, migration steps, and verification checklist
- [ ] T060 Update specs/001-ai-chatbot/quickstart.md with actual implementation details and curl examples for testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Verifies existing conversation persistence logic
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Adds visibility to existing tool logging

### Within Each User Story

- Models before services (already in Foundational phase)
- MCP tools before agent configuration
- Agent configuration before chat endpoint
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T006)
- All Foundational tasks marked [P] can run in parallel within their dependencies (T009-T010, T018)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All US3 MCP tools marked [P] can be created in parallel (T035-T037)
- All Polish tasks marked [P] can run in parallel (T050-T057)

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch User Story 1 tasks:
# T020-T022 can run in parallel (create and register create_task tool)
# T023-T029 must run sequentially (chat endpoint depends on tool being ready)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T020-T029)
   - Developer B: User Story 2 (T030-T034)
   - Developer C: User Story 3 (T035-T041)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included as they were not requested in the specification
- Frontend implementation is OUT OF SCOPE per specification
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
