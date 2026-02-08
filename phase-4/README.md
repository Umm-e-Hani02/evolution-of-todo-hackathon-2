# Phase III - AI-Powered Todo Chatbot

A stateless AI-powered chatbot for natural language todo task management, built with FastAPI, OpenAI Agents SDK, and MCP (Model Context Protocol) tools.

## Architecture Overview

Phase III demonstrates a **stateless, tool-driven AI architecture** with the following key components:

- **FastAPI Backend**: Stateless REST API with a single `/api/chat` endpoint
- **OpenAI Agents SDK**: Processes natural language and determines intent
- **MCP Tools**: 5 tools for task operations (create, list, update, complete, delete)
- **PostgreSQL Database**: Persists all state (conversations, messages, tasks, tool logs)
- **Stateless Design**: Conversation history reconstructed from database on every request

## Key Features

✅ **Natural Language Task Management**: Create, list, update, complete, and delete tasks via chat
✅ **Stateless Architecture**: Zero in-memory session state, horizontal scalability
✅ **Tool-Driven AI**: Agent uses only MCP tools, no direct database access
✅ **Auditable Actions**: All tool calls logged with inputs, outputs, and timestamps
✅ **Conversation Persistence**: Resume conversations after server restarts
✅ **Tool Call Visibility**: Inspect tool invocations for debugging and evaluation

## Project Structure

```
phase-3/
├── backend/
│   ├── src/
│   │   ├── models/          # SQLModel entities
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   ├── task.py
│   │   │   └── tool_log.py
│   │   ├── mcp/             # MCP tools
│   │   │   ├── server.py
│   │   │   └── tools/
│   │   │       ├── create_task.py
│   │   │       ├── list_tasks.py
│   │   │       ├── update_task.py
│   │   │       ├── complete_task.py
│   │   │       └── delete_task.py
│   │   ├── agent/           # OpenAI Agent
│   │   │   ├── runner.py
│   │   │   └── instructions.py
│   │   ├── services/        # Business logic
│   │   │   ├── conversation_service.py
│   │   │   └── message_service.py
│   │   ├── api/             # API endpoints
│   │   │   └── chat.py
│   │   ├── database.py      # Database config
│   │   └── main.py          # FastAPI app
│   ├── alembic/             # Database migrations
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # React frontend (to be implemented)
└── specs/                   # Documentation

```

## Prerequisites

- Python 3.11+
- PostgreSQL (Neon serverless recommended)
- OpenAI API key with GPT-4 access
- Node.js 18+ (for frontend)

## Setup Instructions

### 1. Backend Setup

```bash
cd phase-3/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your:
# - DATABASE_URL (PostgreSQL connection string)
# - OPENAI_API_KEY (your OpenAI API key)
# - BETTER_AUTH_SECRET (from Phase II, or generate new)
```

### 2. Database Setup

```bash
# Run migrations
alembic upgrade head

# Verify tables created:
# - conversations
# - messages
# - tool_logs
# - tasks (should already exist from Phase II)
```

### 3. Run Backend Server

```bash
# Development mode
uvicorn src.main:app --reload --port 8000

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Server will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

### 4. Test the Chat Endpoint

```bash
# Start a new conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": null
  }'

# Response:
# {
#   "conversation_id": "uuid-here",
#   "message": "I've created a task to buy groceries for you.",
#   "tool_calls": [
#     {
#       "tool_name": "create_task",
#       "input": {"title": "buy groceries", "user_id": "..."},
#       "output": {"success": true, "data": {...}},
#       "success": true
#     }
#   ]
# }

# Continue the conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are my tasks?",
    "conversation_id": "uuid-from-previous-response"
  }'
```

## API Endpoints

### POST /api/chat

Send a chat message to the AI agent.

**Request:**
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": null  // Optional: omit for new conversation
}
```

**Response:**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "I've created a task to buy groceries for you.",
  "tool_calls": [
    {
      "tool_name": "create_task",
      "input": {"title": "buy groceries", "user_id": "..."},
      "output": {"success": true, "data": {"task_id": "...", "title": "buy groceries"}},
      "success": true
    }
  ]
}
```

### GET /api/conversations/{conversation_id}/tool-logs

Get tool execution logs for a conversation (for debugging and evaluation).

**Response:**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "tool_logs": [
    {
      "id": "...",
      "tool_name": "create_task",
      "input": {...},
      "output": {...},
      "success": true,
      "timestamp": "2026-01-18T10:30:00Z"
    }
  ]
}
```

## MCP Tools

Phase III implements 5 MCP tools for task management:

1. **create_task**: Create a new task
   - Input: `title` (string), `user_id` (string)
   - Output: Task data with `task_id`, `title`, `completed`, `created_at`

2. **list_tasks**: List user's tasks with optional filtering
   - Input: `user_id` (string), `filter` (optional: "all", "completed", "incomplete")
   - Output: Array of tasks with count

3. **update_task**: Update a task's title
   - Input: `task_id` (string), `title` (string), `user_id` (string)
   - Output: Updated task data

4. **complete_task**: Mark a task as complete
   - Input: `task_id` (string), `user_id` (string)
   - Output: Updated task data with `completed: true`

5. **delete_task**: Soft delete a task
   - Input: `task_id` (string), `user_id` (string)
   - Output: Confirmation with `deleted: true`

## Stateless Architecture

Phase III demonstrates a **stateless server architecture**:

- ✅ **No in-memory session state**: All state persisted in PostgreSQL
- ✅ **Conversation reconstruction**: History loaded from database on every request
- ✅ **Horizontal scalability**: Any server instance can handle any request
- ✅ **Zero-downtime deployments**: Server restarts don't lose data
- ✅ **Multi-device support**: Access conversations from any device

## Testing Scenarios

### Scenario 1: Create and List Tasks

```bash
# 1. Create a task
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'

# 2. Create another task
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a task to finish the report", "conversation_id": "uuid-from-step-1"}'

# 3. List all tasks
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are my tasks?", "conversation_id": "uuid-from-step-1"}'
```

### Scenario 2: Complete and Delete Tasks

```bash
# 1. Complete a task
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Mark buy groceries as done", "conversation_id": "uuid"}'

# 2. Delete a task
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Delete the report task", "conversation_id": "uuid"}'
```

### Scenario 3: Server Restart Resilience

```bash
# 1. Start a conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk"}'
# Save the conversation_id

# 2. Restart the server
# Ctrl+C to stop, then restart with: uvicorn src.main:app --reload

# 3. Continue the conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What tasks do I have?", "conversation_id": "saved-uuid"}'

# ✅ Conversation history is preserved!
```

## Environment Variables

Required environment variables in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@host/dbname

# OpenAI
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4
AGENT_TIMEOUT=30
CONVERSATION_HISTORY_LIMIT=50

# Auth (from Phase II)
BETTER_AUTH_SECRET=your-secret-key

# CORS
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

## Deployment

### Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `cd phase-3/backend && pip install -r requirements.txt`
   - **Start Command**: `cd phase-3/backend && uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env`
5. Deploy!

### Database Migration on Deploy

Add to your deploy script:

```bash
cd phase-3/backend
alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

## Troubleshooting

### Issue: "OpenAI API key not found"

**Solution**: Ensure `OPENAI_API_KEY` is set in `.env` file.

### Issue: "Agent doesn't call tools"

**Solution**: Verify agent instructions in `src/agent/instructions.py` clearly describe when to use each tool.

### Issue: "Conversation history not loading"

**Solution**: Check database connection and verify `messages` table has data.

### Issue: "CORS errors from frontend"

**Solution**: Add your frontend URL to `CORS_ORIGINS` in `.env`.

## Architecture Principles

Phase III follows these constitutional principles:

1. **Stateless Server Architecture**: Zero in-memory session state
2. **Tool-Driven AI Behavior**: Agent uses only MCP tools
3. **Deterministic and Auditable Actions**: All tool calls logged
4. **Clear Separation of Concerns**: Strict layer boundaries
5. **Conversation Context Reconstruction**: Database-backed history

## Next Steps

- [ ] Implement frontend with React and ChatKit
- [ ] Add Better Auth integration (currently using mock auth)
- [ ] Add rate limiting for production
- [ ] Implement conversation summarization for long conversations
- [ ] Add support for task due dates and priorities
- [ ] Deploy to production

## License

MIT

## Support

For issues or questions, please refer to the specification documents in `specs/001-ai-chatbot/`.
