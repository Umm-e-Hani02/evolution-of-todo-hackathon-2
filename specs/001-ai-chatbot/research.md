# Research: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot
**Date**: 2026-01-18
**Purpose**: Document architectural decisions and research findings for Phase III implementation

## Architectural Decisions

### Decision 1: MCP Tools vs Direct Function Calls

**Decision**: Use MCP (Model Context Protocol) tools exclusively for all task operations

**Rationale**:
- **Auditability**: MCP tools create a clear audit trail. Every tool invocation is logged with inputs, outputs, and timestamps, enabling full traceability of AI actions.
- **Separation of Concerns**: MCP tools enforce a strict boundary between AI logic (agent) and business logic (task operations). The agent cannot directly access the database or application internals.
- **Independent Testing**: MCP tools can be tested independently without running the AI agent, enabling faster test cycles and better test coverage.
- **Standardization**: MCP is an emerging standard for AI-application integration. Using it positions the codebase for future interoperability with other AI frameworks.
- **Security**: Tool-based architecture prevents the agent from executing arbitrary code or accessing unauthorized data. All operations go through validated, controlled interfaces.

**Alternatives Considered**:
- **Direct Function Calls**: Agent directly calls Python functions for task operations
  - Rejected because: No audit trail, tight coupling between agent and business logic, harder to test, security concerns with unrestricted function access
- **REST API Calls**: Agent makes HTTP requests to internal REST endpoints
  - Rejected because: Unnecessary network overhead for in-process communication, more complex error handling, doesn't provide the structured tool interface that MCP offers

**Implementation Notes**:
- Each MCP tool will have JSON schema validation for inputs
- Tools return structured responses: `{"success": bool, "data": dict, "error": str?}`
- Tool execution logged to `tool_logs` table before returning to agent

---

### Decision 2: Stateless vs Session-Based Chat

**Decision**: Implement stateless chat architecture with database-backed conversation history

**Rationale**:
- **Horizontal Scalability**: Stateless design allows any server instance to handle any request. No session affinity required, enabling simple load balancing.
- **Zero-Downtime Deployments**: Server restarts don't lose conversation state. Users can continue conversations seamlessly across deployments.
- **Multi-Device Support**: Conversation history stored in database is accessible from any device. Users can start a conversation on mobile and continue on desktop.
- **Simplified Debugging**: All state is explicit in the database. No hidden in-memory state to track down during debugging.
- **Constitutional Compliance**: Aligns with Principle I (Stateless Server Architecture) and Principle V (Conversation Context Reconstruction).

**Alternatives Considered**:
- **Session-Based Chat with In-Memory State**: Store conversation history in server memory (e.g., Redis, in-process cache)
  - Rejected because: Violates constitutional principles, requires session affinity, loses state on restart, complicates horizontal scaling
- **Hybrid Approach**: Cache recent messages in memory, fall back to database for older messages
  - Rejected because: Adds complexity, still requires cache invalidation logic, doesn't fully solve the statelessness requirement

**Implementation Notes**:
- Every `/api/chat` request loads conversation history from `messages` table
- Conversation history limited to last 50 messages to avoid token limit issues
- Message ordering preserved via `timestamp` field (UTC)
- New messages persisted immediately after agent response

---

### Decision 3: Tool Granularity and Composition

**Decision**: Implement 5 fine-grained MCP tools (create_task, list_tasks, update_task, complete_task, delete_task) rather than a single generic tool

**Rationale**:
- **Clear Intent**: Each tool has a single, well-defined purpose. The agent's intent is explicit in the tool selection.
- **Simplified Validation**: Each tool validates only the inputs it needs. `create_task` validates title, `complete_task` validates task_id, etc.
- **Better Auditability**: Tool logs clearly show what action was taken. "create_task" is more informative than "execute_task_operation with action=create".
- **Easier Testing**: Each tool can be tested independently with focused test cases.
- **Agent Clarity**: Fine-grained tools make it easier for the agent to select the correct operation. Less ambiguity in tool selection.

**Alternatives Considered**:
- **Single Generic Tool**: One `manage_task` tool with an `action` parameter (create/list/update/complete/delete)
  - Rejected because: Less clear intent, complex validation logic, harder to audit, agent more likely to make mistakes in parameter construction
- **Coarse-Grained Composition**: Combine related operations (e.g., `modify_task` for update/complete/delete)
  - Rejected because: Still introduces ambiguity, doesn't provide enough granularity for clear audit trails

**Tool Specifications**:
- `create_task(title: str, user_id: str)` → Creates new task
- `list_tasks(user_id: str, filter: str?)` → Lists tasks (all, completed, incomplete)
- `update_task(task_id: str, title: str, user_id: str)` → Updates task title
- `complete_task(task_id: str, user_id: str)` → Marks task as complete
- `delete_task(task_id: str, user_id: str)` → Deletes task

All tools include `user_id` for authorization scoping.

---

### Decision 4: Conversation Reconstruction Strategy

**Decision**: Load full conversation history from database on every request, limited to last 50 messages

**Rationale**:
- **Simplicity**: No complex caching or synchronization logic. Database is the single source of truth.
- **Consistency**: Every request sees the same conversation state. No cache invalidation issues.
- **Token Limit Management**: Limiting to 50 messages prevents exceeding OpenAI token limits while providing sufficient context for most conversations.
- **Performance**: PostgreSQL query for 50 messages is fast (<10ms). Not a bottleneck compared to OpenAI API latency (1-3 seconds).

**Alternatives Considered**:
- **Load All Messages**: No limit on conversation history
  - Rejected because: Risk of exceeding token limits on long conversations, unnecessary data transfer for old messages
- **Sliding Window with Summarization**: Summarize old messages, keep recent messages verbatim
  - Rejected because: Adds complexity, requires additional OpenAI API calls for summarization, may lose important context
- **Conversation Branching**: Allow users to create new conversation branches
  - Rejected because: Out of scope for MVP, adds UI complexity, not required by spec

**Implementation Notes**:
- Query: `SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp DESC LIMIT 50`
- Messages reversed to chronological order before sending to agent
- If conversation exceeds 50 messages, oldest messages are not loaded (but remain in database for audit)
- Future enhancement: Add conversation summarization for very long conversations

---

## Technology Research

### OpenAI Agents SDK Integration

**Key Findings**:
- OpenAI Agents SDK provides `Agent` and `Runner` classes for managing agent lifecycle
- Agents are configured with system instructions, tools, and model selection
- Runner handles the request-response cycle and tool execution loop
- Tools are registered as Python functions with type hints and docstrings

**Best Practices**:
- Define agent instructions in separate file (`agent/instructions.py`) for maintainability
- Use type hints for all tool parameters to enable automatic schema generation
- Implement tool error handling to return structured error responses
- Set reasonable timeout limits for agent execution (30 seconds recommended)

**Integration Pattern**:
```python
# Pseudocode
agent = Agent(
    name="TodoAssistant",
    instructions=load_instructions(),
    tools=[create_task, list_tasks, update_task, complete_task, delete_task],
    model="gpt-4"
)

runner = Runner(agent=agent)
response = runner.run(messages=conversation_history)
```

---

### MCP SDK for Python

**Key Findings**:
- Official MCP SDK provides `MCPServer` class for tool registration
- Tools defined as Python functions with JSON schema annotations
- SDK handles input validation, error handling, and response formatting
- Supports both synchronous and asynchronous tool execution

**Best Practices**:
- Use Pydantic models for tool input/output schemas
- Implement comprehensive error handling in each tool
- Log all tool executions for audit trail
- Return structured responses with success/failure status

**Integration Pattern**:
```python
# Pseudocode
mcp_server = MCPServer()

@mcp_server.tool()
def create_task(title: str, user_id: str) -> dict:
    """Create a new task for the user."""
    # Implementation
    return {"success": True, "data": {"task_id": "...", "title": title}}
```

---

### Error Handling Patterns

**Strategy**: Implement layered error handling at each architectural boundary

**Layers**:
1. **MCP Tool Layer**: Catch database errors, validation errors, return structured error responses
2. **Agent Layer**: Handle tool execution failures, retry logic for transient errors
3. **API Layer**: Catch agent errors, return user-friendly HTTP error responses
4. **Frontend Layer**: Display error messages to user (out of scope for backend)

**Error Categories**:
- **Validation Errors**: Invalid input parameters (400 Bad Request)
- **Authentication Errors**: Missing or invalid auth token (401 Unauthorized)
- **Authorization Errors**: User attempting to access another user's tasks (403 Forbidden)
- **Not Found Errors**: Task or conversation not found (404 Not Found)
- **External Service Errors**: OpenAI API failures (503 Service Unavailable)
- **Database Errors**: Connection failures, constraint violations (500 Internal Server Error)

**Implementation Notes**:
- All errors logged with structured logging (timestamp, error type, context)
- User-facing error messages are friendly and actionable
- Internal error details (stack traces) not exposed to users
- Failed tool calls logged to `tool_logs` table with `success=false`

---

## Performance Considerations

**Expected Latency Breakdown**:
- Database query (load conversation): ~10ms
- OpenAI API call (agent processing): 1-3 seconds
- Database write (save messages + tool logs): ~20ms
- **Total**: ~1-3 seconds (dominated by OpenAI API)

**Optimization Opportunities**:
- Use database connection pooling to reduce connection overhead
- Implement request timeout (5 seconds) to prevent hanging requests
- Consider caching user authentication results (if Better Auth supports it)
- Monitor OpenAI API latency and implement fallback strategies for slow responses

**Scalability**:
- Stateless architecture enables horizontal scaling
- Database is the bottleneck (Neon PostgreSQL serverless handles this)
- Each request is independent, no coordination required between servers

---

## Security Considerations

**Authentication**:
- All `/api/chat` requests require Bearer token from Better Auth
- Token validated on every request (no session state)
- User ID extracted from validated token

**Authorization**:
- All MCP tools include `user_id` parameter
- Tools verify that `user_id` matches authenticated user
- Database queries scoped to authenticated user (prevents data leakage)

**Input Validation**:
- MCP tools validate all inputs using JSON schema
- SQL injection prevented by using SQLModel ORM (parameterized queries)
- XSS prevention handled by frontend (out of scope for backend)

**Audit Trail**:
- All tool invocations logged to `tool_logs` table
- Logs include: timestamp, tool name, input, output, success status, conversation_id
- Logs queryable for security audits and debugging

---

## Testing Strategy

### Unit Tests (MCP Tools)
- Test each tool in isolation with mocked database
- Verify input validation (valid inputs, invalid inputs, edge cases)
- Verify authorization (user can only access own tasks)
- Verify error handling (database errors, not found errors)

### Integration Tests (Agent + Tools)
- Test agent with real MCP tools and test database
- Verify agent selects correct tool for user intent
- Verify multi-turn conversations maintain context
- Verify tool execution results in correct database state

### Contract Tests (API Endpoint)
- Test `/api/chat` endpoint with OpenAPI schema validation
- Verify request/response format matches contract
- Verify authentication and authorization
- Verify error responses match expected format

### Manual Tests (Conversational Flows)
- Test natural language variations ("add task", "create todo", "new task")
- Test ambiguous commands (agent should ask for clarification)
- Test multi-turn conversations (context maintained)
- Test server restart resilience (conversation resumes)

---

## Open Questions

None. All architectural decisions resolved through research and constitutional alignment.
