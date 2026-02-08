# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `001-ai-chatbot` | **Date**: 2026-01-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a stateless AI-powered chatbot that enables natural language todo task management. Users interact with tasks (create, list, update, complete, delete) through conversational commands processed by an OpenAI agent. The agent uses MCP (Model Context Protocol) tools exclusively for all task operations, ensuring auditability and separation of concerns. Conversation history is persisted in PostgreSQL and reconstructed on every request, demonstrating stateless architecture principles. The system maintains backward compatibility with existing Phase II REST endpoints while adding a new `/api/chat` endpoint for conversational interactions.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK for Python, SQLModel, Better Auth
**Storage**: Neon PostgreSQL (serverless)
**Testing**: pytest (unit, integration, contract tests)
**Target Platform**: Linux server (Render or similar Python-supporting platform)
**Project Type**: web (backend API + React frontend)
**Performance Goals**: Chat endpoint responds within 5 seconds (excluding OpenAI API latency), 90% intent recognition accuracy
**Constraints**: Zero in-memory session state, 100% tool-driven task operations, backward compatibility with Phase II REST endpoints
**Scale/Scope**: Single-user conversational interface, 5 MCP tools (create/list/update/complete/delete tasks), conversation history limited to recent messages to avoid token limits

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Stateless Server Architecture ✅ COMPLIANT

- **Requirement**: Zero in-memory session state, database-backed persistence
- **Implementation**: Conversation history stored in PostgreSQL, reconstructed on every `/api/chat` request
- **Verification**: Server restart test - conversations must resume without data loss

### Principle II: Tool-Driven AI Behavior ✅ COMPLIANT

- **Requirement**: Agent uses only MCP tools, no direct database access
- **Implementation**: 5 MCP tools (create_task, list_tasks, update_task, complete_task, delete_task) encapsulate all task operations
- **Verification**: Agent code must not import SQLModel models or database modules

### Principle III: Deterministic and Auditable Actions ✅ COMPLIANT

- **Requirement**: All tool calls logged with inputs, outputs, timestamps
- **Implementation**: ToolLog entity persists every MCP tool invocation to database
- **Verification**: Tool call logs queryable for audit, conversational responses confirm actions

### Principle IV: Clear Separation of Concerns ✅ COMPLIANT

- **Requirement**: Strict layer boundaries (UI, API, Agent, MCP, Database)
- **Implementation**:
  - Frontend → FastAPI `/api/chat` endpoint only
  - FastAPI → Orchestrates OpenAI Agent, does not implement AI logic
  - Agent → Uses MCP tools only
  - MCP Server → Encapsulates task business logic, uses SQLModel for DB access
- **Verification**: No cross-layer imports, each layer independently testable

### Principle V: Conversation Context Reconstruction ✅ COMPLIANT

- **Requirement**: Conversation history from database, not in-memory
- **Implementation**: Messages table stores all user/assistant messages, loaded on each request
- **Verification**: Multi-device access test, conversation history available across sessions

### Summary

**Status**: ✅ ALL PRINCIPLES COMPLIANT

No constitutional violations. Architecture fully aligns with stateless, tool-driven, auditable design principles.

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── chat-api.yaml    # OpenAPI spec for /api/chat endpoint
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py      # Conversation SQLModel
│   │   ├── message.py           # Message SQLModel
│   │   ├── tool_log.py          # ToolLog SQLModel
│   │   └── task.py              # Task SQLModel (existing from Phase II)
│   ├── mcp/
│   │   ├── server.py            # MCP server initialization
│   │   └── tools/
│   │       ├── create_task.py   # MCP tool: create task
│   │       ├── list_tasks.py    # MCP tool: list tasks
│   │       ├── update_task.py   # MCP tool: update task
│   │       ├── complete_task.py # MCP tool: complete task
│   │       └── delete_task.py   # MCP tool: delete task
│   ├── agent/
│   │   ├── runner.py            # OpenAI Agent runner
│   │   └── instructions.py      # Agent system instructions
│   ├── api/
│   │   ├── chat.py              # POST /api/chat endpoint
│   │   └── tasks.py             # Existing Phase II REST endpoints
│   ├── services/
│   │   ├── conversation_service.py  # Conversation CRUD operations
│   │   └── message_service.py       # Message persistence
│   └── database.py              # Database connection and session management
└── tests/
    ├── unit/
    │   ├── test_mcp_tools.py    # Unit tests for each MCP tool
    │   └── test_models.py       # Unit tests for SQLModel entities
    ├── integration/
    │   └── test_agent_tools.py  # Integration tests: agent + MCP tools
    └── contract/
        └── test_chat_api.py     # Contract tests for /api/chat endpoint

frontend/
├── src/
│   ├── components/
│   │   └── ChatInterface.tsx    # New chat UI component (out of scope for backend)
│   ├── pages/
│   │   └── Chat.tsx             # Chat page (out of scope for backend)
│   └── services/
│       └── chatApi.ts           # API client for /api/chat (out of scope for backend)
└── tests/
```

**Structure Decision**: Web application structure selected. Backend contains all Phase III logic (MCP tools, agent, chat endpoint) while maintaining Phase II REST endpoints. Frontend structure shown for completeness but frontend implementation is out of scope for this feature. The `backend/src/mcp/` directory encapsulates all MCP tool implementations, ensuring clear separation from agent and API layers.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
