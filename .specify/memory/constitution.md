<!--
Sync Impact Report:
- Version: Initial → 1.0.0 (MAJOR: First ratification)
- Principles Added: 5 core principles established
- Sections Added: Technical Standards, Development Workflow, Governance
- Templates Status:
  ✅ plan-template.md: Constitution Check section aligns with principles
  ✅ spec-template.md: User story prioritization aligns with MVP-first approach
  ✅ tasks-template.md: Phase structure supports stateless architecture validation
- Follow-up: None - all placeholders resolved
-->

# Evolution of Todo — Phase III Constitution

## Core Principles

### I. Stateless Server Architecture

The server MUST maintain zero in-memory session state. All application state MUST be persisted in the database. Conversation context MUST be reconstructed from the database on every request.

**Rationale**: Stateless design ensures horizontal scalability, eliminates session affinity requirements, enables zero-downtime deployments, and simplifies debugging by making all state explicit and auditable.

**Non-negotiable rules**:
- No in-memory caches for user sessions or conversation history
- Server restart MUST NOT lose any user data or conversation state
- Each request MUST be independently processable using only database state
- No sticky sessions or session affinity in load balancing

### II. Tool-Driven AI Behavior

The AI agent MUST interact with the application exclusively through MCP (Model Context Protocol) tools. The agent MUST NOT have direct database access. All task operations (create, read, update, delete) MUST go through well-defined MCP tools.

**Rationale**: Tool-driven architecture creates a clear contract between AI and application logic, enables comprehensive auditing of AI actions, allows independent testing of tools, and prevents uncontrolled database access.

**Non-negotiable rules**:
- Agent code MUST NOT import database models or ORM libraries
- Every task operation MUST have a corresponding MCP tool
- Tools MUST validate inputs and return structured outputs
- Tool execution MUST be logged for audit trails

### III. Deterministic and Auditable Actions

Every AI action MUST be deterministic, traceable, and auditable. Tool calls MUST be logged with inputs, outputs, and timestamps. Users MUST be able to understand what the AI did and why.

**Rationale**: Auditability builds user trust, enables debugging of AI behavior, supports compliance requirements, and allows rollback of unintended actions.

**Non-negotiable rules**:
- All tool invocations MUST be persisted to database
- Tool logs MUST include: timestamp, tool name, input parameters, output, success/failure
- Conversational responses MUST confirm actions taken
- Failed tool calls MUST be surfaced to users with clear error messages

### IV. Clear Separation of Concerns

The system MUST maintain strict boundaries between layers: UI (frontend), API (FastAPI), Agent (OpenAI SDK), MCP Server (tool provider), and Database (PostgreSQL). Each layer MUST have a single, well-defined responsibility.

**Rationale**: Separation of concerns enables independent testing, simplifies maintenance, allows technology substitution, and prevents tight coupling that hinders evolution.

**Non-negotiable rules**:
- Frontend MUST communicate only with API endpoints (no direct DB or agent access)
- API MUST orchestrate agent calls but not implement AI logic
- Agent MUST use only MCP tools (no direct API or DB calls)
- MCP Server MUST encapsulate all business logic for task operations
- Database MUST be accessed only through SQLModel ORM

### V. Conversation Context Reconstruction

Conversation history MUST be stored in the database and reconstructed on every request. The agent MUST receive full conversation context from the database, not from in-memory state.

**Rationale**: Database-backed conversation history ensures consistency across server restarts, enables conversation replay for debugging, supports multi-device access, and aligns with stateless architecture.

**Non-negotiable rules**:
- Every user message and agent response MUST be persisted immediately
- Agent initialization MUST load conversation history from database
- Conversation retrieval MUST be scoped to authenticated user
- Message ordering MUST be preserved via timestamps or sequence numbers

## Technical Standards

### Technology Stack (Non-Negotiable)

- **Backend Framework**: FastAPI (Python 3.11+)
- **Database**: Neon PostgreSQL with SQLModel ORM
- **Authentication**: Better Auth
- **AI Framework**: OpenAI Agents SDK
- **Tool Protocol**: Official MCP SDK for Python
- **Frontend**: React (existing Phase II implementation)

### API Design

- **Single Chat Endpoint**: One stateless POST endpoint (`/api/chat`) handles all conversational interactions
- **Request Format**: JSON with `{ user_id, message, conversation_id? }`
- **Response Format**: JSON with `{ response, tool_calls?, conversation_id }`
- **Authentication**: Bearer token via Better Auth, validated on every request
- **Error Handling**: Structured error responses with codes and user-friendly messages

### MCP Tool Requirements

Every MCP tool MUST:
- Accept structured input (JSON schema validated)
- Return structured output (success/failure + data)
- Be independently testable without agent
- Include docstrings describing purpose, inputs, outputs
- Handle errors gracefully and return actionable error messages

### Database Schema Requirements

- **Users**: Managed by Better Auth
- **Conversations**: `id`, `user_id`, `created_at`, `updated_at`
- **Messages**: `id`, `conversation_id`, `role` (user/assistant), `content`, `timestamp`
- **Tasks**: `id`, `user_id`, `title`, `completed`, `created_at`, `updated_at`
- **Tool Logs**: `id`, `conversation_id`, `tool_name`, `input`, `output`, `timestamp`, `success`

All tables MUST use UUIDs for primary keys. All timestamps MUST be UTC. Soft deletes MUST be used for user-facing entities (tasks, conversations).

## Development Workflow

### Phase Isolation

This project follows a phased evolution approach:
- **Phase I**: Basic todo CRUD (completed)
- **Phase II**: Full-stack improvements (completed)
- **Phase III**: AI-powered chatbot (current)

Phase III MUST NOT break Phase I or Phase II functionality. Backend MUST support both traditional REST endpoints (Phase II) and conversational endpoint (Phase III) simultaneously.

### Testing Requirements

- **Unit Tests**: Required for MCP tools, database models, API endpoints
- **Integration Tests**: Required for agent + MCP tool interactions
- **Contract Tests**: Required for API endpoint contracts
- **Manual Testing**: Required for conversational flows before deployment

Tests MUST be written before implementation (TDD) when explicitly requested in feature specifications. Otherwise, tests are optional but encouraged.

### Deployment Constraints

- **Backend**: Deployed to Render or similar platform supporting Python
- **Database**: Neon PostgreSQL (serverless)
- **Frontend**: Vercel (existing Phase II deployment)
- **Environment Variables**: All secrets MUST be in `.env` (never committed)
- **CORS**: Backend MUST allow frontend origin (production and development)

### Code Quality Standards

- **Type Hints**: Required for all Python functions
- **Docstrings**: Required for public APIs and MCP tools
- **Linting**: Ruff or Black for formatting
- **Error Handling**: All external calls (DB, OpenAI API) MUST have try-catch with logging
- **Logging**: Structured logging (JSON) for production, human-readable for development

## Governance

### Amendment Process

This constitution supersedes all other development practices. Amendments require:
1. Documented rationale for the change
2. Impact analysis on existing code and templates
3. Update to constitution version following semantic versioning
4. Propagation of changes to dependent templates (plan, spec, tasks)
5. Commit message: `docs: amend constitution to vX.Y.Z (brief description)`

### Versioning Policy

- **MAJOR**: Backward-incompatible principle removals or redefinitions
- **MINOR**: New principles added or materially expanded guidance
- **PATCH**: Clarifications, wording fixes, non-semantic refinements

### Compliance Review

All pull requests MUST verify compliance with this constitution. Violations MUST be justified in the "Complexity Tracking" section of `plan.md` with:
- What principle is violated
- Why the violation is necessary
- What simpler alternative was rejected and why

Unjustified violations MUST be rejected in code review.

### Runtime Guidance

For agent-specific development guidance, see `CLAUDE.md` in the repository root. That file provides execution workflows, PHR creation rules, and ADR suggestion protocols that complement these constitutional principles.

**Version**: 1.0.0 | **Ratified**: 2026-01-18 | **Last Amended**: 2026-01-18
