# Quickstart: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot
**Date**: 2026-01-18
**Purpose**: Get started with Phase III AI chatbot development and testing

## Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed
- **PostgreSQL** access (Neon serverless recommended)
- **OpenAI API key** with access to GPT-4
- **Better Auth** configured (from Phase II)
- **Git** for version control
- **Phase II** backend running successfully

## Environment Setup

### 1. Install Dependencies

Add the following to `backend/requirements.txt`:

```txt
# Existing Phase II dependencies
fastapi>=0.104.0
sqlmodel>=0.0.14
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0

# New Phase III dependencies
openai>=1.10.0              # OpenAI Agents SDK
mcp>=0.1.0                  # Official MCP SDK for Python
pydantic>=2.5.0             # For MCP tool schemas
```

Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Add to `backend/.env`:

```env
# Existing Phase II variables
DATABASE_URL=postgresql://user:password@host/dbname
BETTER_AUTH_SECRET=your-secret-key

# New Phase III variables
OPENAI_API_KEY=sk-...your-openai-api-key
OPENAI_MODEL=gpt-4                    # or gpt-4-turbo
AGENT_TIMEOUT=30                      # seconds
CONVERSATION_HISTORY_LIMIT=50         # messages
```

**Security Note**: Never commit `.env` file to version control.

### 3. Database Migrations

Create and run migrations for new tables:

```bash
# Generate migration
alembic revision --autogenerate -m "Add Phase III tables: conversations, messages, tool_logs"

# Review the generated migration file in alembic/versions/
# Ensure it creates: conversations, messages, tool_logs tables

# Run migration
alembic upgrade head
```

**Expected Tables After Migration**:
- `conversations` (id, user_id, created_at, updated_at, deleted_at)
- `messages` (id, conversation_id, role, content, timestamp)
- `tool_logs` (id, conversation_id, tool_name, input, output, success, timestamp)
- `tasks` (existing, no changes)
- `users` (existing, managed by Better Auth)

## Project Structure

After implementation, your backend should look like:

```
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py      # NEW
│   │   ├── message.py           # NEW
│   │   ├── tool_log.py          # NEW
│   │   └── task.py              # EXISTING
│   ├── mcp/
│   │   ├── server.py            # NEW - MCP server setup
│   │   └── tools/               # NEW
│   │       ├── create_task.py
│   │       ├── list_tasks.py
│   │       ├── update_task.py
│   │       ├── complete_task.py
│   │       └── delete_task.py
│   ├── agent/
│   │   ├── runner.py            # NEW - OpenAI Agent runner
│   │   └── instructions.py      # NEW - Agent system prompt
│   ├── api/
│   │   ├── chat.py              # NEW - POST /api/chat
│   │   └── tasks.py             # EXISTING - Phase II REST endpoints
│   ├── services/
│   │   ├── conversation_service.py  # NEW
│   │   └── message_service.py       # NEW
│   └── database.py              # EXISTING
└── tests/
    ├── unit/
    │   ├── test_mcp_tools.py    # NEW
    │   └── test_models.py       # UPDATE
    ├── integration/
    │   └── test_agent_tools.py  # NEW
    └── contract/
        └── test_chat_api.py     # NEW
```

## Running the Application

### 1. Start the Backend Server

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2. Verify Phase II Endpoints Still Work

Test existing REST endpoints to ensure backward compatibility:

```bash
# Get auth token (Phase II)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Response: {"token": "eyJ..."}

# List tasks (Phase II REST endpoint)
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer eyJ..."

# Response: [{"id": "...", "title": "...", "completed": false}]
```

### 3. Test the Chat Endpoint

#### Start a New Conversation

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ..." \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": null
  }'
```

Expected response:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "I've created a task to buy groceries for you.",
  "tool_calls": [
    {
      "tool_name": "create_task",
      "input": {
        "title": "buy groceries",
        "user_id": "user-uuid"
      },
      "output": {
        "success": true,
        "data": {
          "task_id": "task-uuid",
          "title": "buy groceries"
        }
      },
      "success": true
    }
  ]
}
```

#### Continue the Conversation

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ..." \
  -d '{
    "message": "What are my tasks?",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

Expected response:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "You have 1 task:\n1. Buy groceries (incomplete)",
  "tool_calls": [
    {
      "tool_name": "list_tasks",
      "input": {
        "user_id": "user-uuid"
      },
      "output": {
        "success": true,
        "data": {
          "tasks": [
            {
              "task_id": "task-uuid",
              "title": "buy groceries",
              "completed": false
            }
          ]
        }
      },
      "success": true
    }
  ]
}
```

## Testing

### Unit Tests (MCP Tools)

Test each MCP tool in isolation:

```bash
cd backend
pytest tests/unit/test_mcp_tools.py -v
```

Expected tests:
- `test_create_task_success` - Valid task creation
- `test_create_task_empty_title` - Validation error
- `test_list_tasks_empty` - No tasks for user
- `test_list_tasks_with_filter` - Filter by completion status
- `test_update_task_success` - Update task title
- `test_update_task_not_found` - Task doesn't exist
- `test_complete_task_success` - Mark task complete
- `test_delete_task_success` - Delete task
- `test_authorization_check` - User can't access other user's tasks

### Integration Tests (Agent + Tools)

Test agent with real MCP tools:

```bash
pytest tests/integration/test_agent_tools.py -v
```

Expected tests:
- `test_agent_creates_task` - Agent correctly interprets "add task" intent
- `test_agent_lists_tasks` - Agent correctly interprets "show tasks" intent
- `test_agent_completes_task` - Agent correctly interprets "mark done" intent
- `test_multi_turn_conversation` - Agent maintains context across turns
- `test_ambiguous_command` - Agent asks for clarification

### Contract Tests (API Endpoint)

Test API contract compliance:

```bash
pytest tests/contract/test_chat_api.py -v
```

Expected tests:
- `test_chat_request_schema` - Request matches OpenAPI spec
- `test_chat_response_schema` - Response matches OpenAPI spec
- `test_authentication_required` - 401 without token
- `test_invalid_conversation_id` - 404 for nonexistent conversation
- `test_error_response_format` - Error responses match schema

### Manual Testing Scenarios

Test these conversational flows manually:

1. **Task Creation Variations**
   - "Add a task to buy groceries"
   - "Create a todo: finish report"
   - "Remind me to call dentist"
   - "New task: review pull request"

2. **Task Listing Variations**
   - "What are my tasks?"
   - "Show my todos"
   - "List incomplete tasks"
   - "What do I need to do?"

3. **Task Completion Variations**
   - "Mark 'buy groceries' as done"
   - "Complete the dentist task"
   - "I finished the report"

4. **Multi-Turn Conversations**
   - Create task → List tasks → Complete task → List tasks again
   - Verify agent maintains context

5. **Server Restart Resilience**
   - Start conversation
   - Restart server
   - Continue conversation
   - Verify history is preserved

## Verification Checklist

After implementation, verify:

- [ ] All Phase II REST endpoints still work (backward compatibility)
- [ ] `/api/chat` endpoint accepts POST requests with Bearer token
- [ ] New conversation created when `conversation_id` is null
- [ ] Existing conversation continued when `conversation_id` provided
- [ ] Agent correctly interprets task creation intent
- [ ] Agent correctly interprets task listing intent
- [ ] Agent correctly interprets task completion intent
- [ ] All tool calls logged to `tool_logs` table
- [ ] All messages persisted to `messages` table
- [ ] Conversation history reconstructed from database on each request
- [ ] Server restart doesn't lose conversation data
- [ ] Authentication required for all chat requests
- [ ] Users can only access their own tasks and conversations
- [ ] Error responses are user-friendly and match OpenAPI spec
- [ ] Tool call details included in response for transparency

## Common Issues and Troubleshooting

### Issue: "OpenAI API key not found"

**Solution**: Ensure `OPENAI_API_KEY` is set in `.env` file and loaded correctly.

```python
# In src/config.py
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment")
```

### Issue: "Agent doesn't call tools"

**Solution**: Verify agent instructions clearly describe when to use each tool.

```python
# In src/agent/instructions.py
INSTRUCTIONS = """
You are a helpful todo task assistant. You help users manage their tasks through conversation.

When the user wants to create a task, use the create_task tool.
When the user wants to see their tasks, use the list_tasks tool.
When the user wants to mark a task complete, use the complete_task tool.
When the user wants to update a task, use the update_task tool.
When the user wants to delete a task, use the delete_task tool.

Always confirm actions taken and provide friendly responses.
"""
```

### Issue: "Conversation history not loading"

**Solution**: Verify database query and message ordering.

```python
# In src/services/conversation_service.py
def load_conversation_history(conversation_id: str, limit: int = 50):
    messages = session.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.timestamp.desc())\
        .limit(limit)\
        .all()

    # Reverse to chronological order
    return list(reversed(messages))
```

### Issue: "Tool logs not persisted"

**Solution**: Ensure tool execution wrapper logs before returning.

```python
# In src/mcp/tools/base.py
def log_tool_execution(conversation_id, tool_name, input, output, success):
    tool_log = ToolLog(
        conversation_id=conversation_id,
        tool_name=tool_name,
        input=input,
        output=output,
        success=success,
        timestamp=datetime.utcnow()
    )
    session.add(tool_log)
    session.commit()
```

### Issue: "CORS errors from frontend"

**Solution**: Ensure FastAPI CORS middleware allows frontend origin.

```python
# In src/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://your-frontend.vercel.app"  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Next Steps

After completing Phase III implementation:

1. **Run `/sp.tasks`** to generate implementation tasks
2. **Implement tasks** following the task list
3. **Run tests** after each task completion
4. **Deploy to staging** for integration testing
5. **Update frontend** to add chat interface (separate feature)
6. **Deploy to production** after QA approval

## Resources

- **OpenAPI Spec**: `specs/001-ai-chatbot/contracts/chat-api.yaml`
- **Data Model**: `specs/001-ai-chatbot/data-model.md`
- **Research**: `specs/001-ai-chatbot/research.md`
- **Constitution**: `.specify/memory/constitution.md`
- **OpenAI Agents SDK Docs**: https://platform.openai.com/docs/agents
- **MCP SDK Docs**: https://modelcontextprotocol.io/docs
