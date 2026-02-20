# Phase 3: AI-Powered Todo Application

**Version**: 1.0.0
**Status**: Production Ready
**Last Updated**: 2026-02-20

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Setup & Installation](#setup--installation)
5. [Authentication](#authentication)
6. [Task Management](#task-management)
7. [Chatbot Integration](#chatbot-integration)
8. [Security](#security)
9. [API Documentation](#api-documentation)
10. [Testing](#testing)
11. [Known Limitations](#known-limitations)
12. [Troubleshooting](#troubleshooting)

---

## Project Overview

Phase 3 is a full-stack, multi-user todo application with an AI-powered chatbot assistant. Users can manage tasks through a modern web interface or by conversing naturally with an AI assistant that executes task operations via MCP (Model Context Protocol) tools.

### Key Capabilities

- **Multi-user authentication** with JWT tokens
- **CRUD operations** for task management
- **AI chatbot** for natural language task management
- **Stateless architecture** for horizontal scalability
- **Real-time UI updates** with optimistic rendering
- **Session-only chat** (resets on logout)

### Technology Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- React Context API
- Axios for HTTP requests

**Backend:**
- FastAPI (Python)
- SQLModel ORM
- PostgreSQL / SQLite
- OpenAI API (optional)
- JWT authentication with bcrypt

**AI Integration:**
- OpenAI function calling
- MCP (Model Context Protocol) tools
- Fallback intent detection (regex-based)

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Dashboard   │  │   Chatbot    │  │  Auth Pages  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                            │                                │
│                    Axios API Client                         │
└────────────────────────────┼────────────────────────────────┘
                             │ HTTP/REST
┌────────────────────────────┼────────────────────────────────┐
│                         Backend                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Auth API    │  │  Todos API   │  │   Chat API   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                            │                                │
│  ┌─────────────────────────┴─────────────────────────┐     │
│  │              Stateless Chatbot Service            │     │
│  │  ┌──────────────────────────────────────────┐    │     │
│  │  │         MCP Server (5 Tools)             │    │     │
│  │  │  • create_task  • list_tasks             │    │     │
│  │  │  • update_task  • complete_task          │    │     │
│  │  │  • delete_task                           │    │     │
│  │  └──────────────────────────────────────────┘    │     │
│  └────────────────────────────────────────────────────┘     │
│                            │                                │
│                    Database (SQLModel)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Users     │  │  TodoTasks   │  │Conversations │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- TodoTask table
CREATE TABLE todotask (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- Conversation table
CREATE TABLE conversation (
    id INTEGER PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- Message table
CREATE TABLE message (
    id INTEGER PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    conversation_id INTEGER REFERENCES conversation(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);
```

---

## Features

### 1. User Authentication

- **Registration**: Email + password with validation
- **Login**: JWT token generation (24-hour expiry)
- **Session Management**: Token stored in localStorage
- **Auto-redirect**: Unauthorized access redirects to login
- **Rate Limiting**: 5 login attempts per minute per IP

### 2. Task Management (UI)

**Create Task:**
- Click "Add New Task" button
- Enter title (required) and description (optional)
- Task appears immediately in dashboard

**Update Task:**
- Click edit icon on task card
- Modify title or description
- Changes saved with optimistic UI update

**Complete Task:**
- Click checkbox on task card
- Status toggles immediately
- Backend syncs in background

**Delete Task:**
- Click delete icon
- Confirmation dialog appears
- Task removed with optimistic UI update

**Filter Tasks:**
- All Tasks - Show everything
- Completed - Show only completed tasks
- Pending - Show only incomplete tasks

### 3. Task Management (Chatbot)

**Natural Language Commands:**

```
Create:
- "add task buy milk"
- "create a task to call mom"
- "remind me to buy groceries"

List:
- "show my tasks"
- "what do I need to do?"
- "list all tasks"

Complete:
- "complete task 1"
- "mark the first task as done"
- "finish the milk task"

Update:
- "update task 1 to say buy bread"
- "change the first task"

Delete:
- "delete task 1"
- "remove the milk task"
- "delete the first task"
```

### 4. Session-Only Chat

**Behavior:**
- Chat history persists during active session
- Close/reopen chatbot → history preserved
- Logout → chat history cleared
- Re-login → fresh chat starts

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd phase-3/backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and configure:
# - JWT_SECRET (generate with: openssl rand -base64 32)
# - DATABASE_URL (default: sqlite:///./local.db)
# - OPENAI_API_KEY (optional, for chatbot)
# - CORS_ORIGINS (comma-separated list)

# Run the server
uvicorn src.main:app --reload --port 8000
```

**Backend will start at**: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### Frontend Setup

```bash
# Navigate to frontend directory
cd phase-3/frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run the development server
npm run dev
```

**Frontend will start at**: `http://localhost:3000`

### Environment Variables

**Backend (.env):**
```bash
# Database
DATABASE_URL=sqlite:///./local.db

# JWT Authentication
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Debug
DEBUG=true

# OpenAI (optional)
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Authentication

### JWT Token Flow

```
1. User submits email + password
   ↓
2. Backend verifies credentials
   ↓
3. Backend generates JWT token
   {
     "sub": "user-uuid",
     "email": "user@example.com",
     "exp": 1234567890
   }
   ↓
4. Frontend stores token in localStorage
   ↓
5. All API requests include: Authorization: Bearer <token>
   ↓
6. Backend validates token on each request
   ↓
7. Backend extracts user_id from token
   ↓
8. Backend filters data by user_id
```

### Password Security

- **Hashing**: bcrypt with automatic salt generation
- **Storage**: Only hash stored in database (never plaintext)
- **Verification**: Constant-time comparison to prevent timing attacks

---

## Task Management

### CRUD Operations

**Create:**
```http
POST /todos
Body: { title: string, description?: string }
Response: TodoTask object
```

**Read:**
```http
GET /todos
Response: TodoTask[]

GET /todos/{id}
Response: TodoTask
```

**Update:**
```http
PATCH /todos/{id}
Body: { title?: string, description?: string, completed?: boolean }
Response: TodoTask
```

**Delete:**
```http
DELETE /todos/{id}
Response: 204 No Content
```

### User Isolation

**Enforcement:**
- All endpoints require JWT authentication
- All queries filter by `current_user.id`
- Cross-user access returns 404 (not 403 to prevent enumeration)
- Foreign key constraints with CASCADE delete

---

## Chatbot Integration

### Dual Mode Operation

**Mode 1: OpenAI Powered (Recommended)**
- Requires: Valid OPENAI_API_KEY
- Uses: GPT-4 with function calling
- Capabilities: Natural language understanding, multi-step reasoning
- Example: "Can you help me remember to buy milk?" → Creates task

**Mode 2: Intent Detection (Fallback)**
- Requires: No API key
- Uses: Regex-based pattern matching
- Capabilities: Basic command recognition
- Example: "add task buy milk" → Creates task

### Function Calling Loop

The chatbot implements a multi-turn function calling loop:

```python
for iteration in range(5):  # Max 5 iterations
    # 1. Send messages to AI
    response = openai.chat.completions.create(...)

    # 2. Check if AI wants to call tools
    if not response.tool_calls:
        return response.content  # AI is done

    # 3. Execute all tool calls
    for tool_call in response.tool_calls:
        result = mcp_server.call_tool(...)
        conversation.append(tool_result)

    # 4. Loop back - AI sees results and decides next action
```

This enables complex operations like:
- "delete task 1" → list_tasks → delete_task
- "complete the first task" → list_tasks → complete_task

### MCP Tools

1. **create_task** - Create new task
2. **list_tasks** - List all user's tasks
3. **update_task** - Update task properties
4. **complete_task** - Mark task as completed
5. **delete_task** - Delete task

---

## Security

### Authentication Security

✅ **Password Protection**
- Bcrypt hashing with automatic salt
- No plaintext passwords stored
- Constant-time comparison

✅ **Token Security**
- JWT with expiration (24 hours)
- Signed with secret key (HS256)
- Validated on every request

✅ **Rate Limiting**
- Login: 5 attempts per minute per IP
- Task creation: 30 tasks per minute per IP

### Authorization Security

✅ **User Isolation**
- All endpoints verify user ownership
- Database queries filter by user_id
- Cross-user access returns 404

✅ **ID Security**
- UUID-based IDs (prevents enumeration)
- No sequential IDs exposed

### API Security

✅ **CORS Protection**
- Restricted to localhost in development
- Configurable for production domains

✅ **SQL Injection Protection**
- SQLModel ORM (parameterized queries)
- No raw SQL execution

✅ **XSS Protection**
- React auto-escaping
- JSON API (not HTML)

---

## API Documentation

### Authentication Endpoints

**Register User**
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response 201:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "created_at": "2026-02-20T00:00:00Z"
  }
}
```

**Login**
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response 200:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "created_at": "2026-02-20T00:00:00Z"
  }
}
```

### Task Endpoints

**List Tasks**
```http
GET /todos
Authorization: Bearer <token>

Response 200:
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Buy milk",
    "description": "Get 2% milk from store",
    "completed": false,
    "created_at": "2026-02-20T00:00:00Z",
    "updated_at": "2026-02-20T00:00:00Z"
  }
]
```

**Create Task**
```http
POST /todos
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy milk",
  "description": "Get 2% milk from store"
}

Response 201:
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Buy milk",
  "description": "Get 2% milk from store",
  "completed": false,
  "created_at": "2026-02-20T00:00:00Z",
  "updated_at": "2026-02-20T00:00:00Z"
}
```

### Chat Endpoints

**Send Message**
```http
POST /api/chat
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "add task buy milk",
  "conversation_id": 1
}

Response 200:
{
  "conversation_id": 1,
  "response": "✓ Got it! I've added 'buy milk' to your task list.",
  "tool_calls": [
    {
      "tool": "create_task",
      "arguments": {"title": "buy milk"},
      "result": {"success": true, "task_id": "uuid", "title": "buy milk"}
    }
  ]
}
```

---

## Testing

### Manual Testing Checklist

**Authentication:**
- [ ] Register new user with valid email/password
- [ ] Register with duplicate email → 409 error
- [ ] Login with correct credentials → Success
- [ ] Login with wrong password → 401 error
- [ ] Access /dashboard without token → Redirect to login
- [ ] Logout → Token cleared, redirect to login

**Task Management (UI):**
- [ ] Create task with title only → Appears in list
- [ ] Update task title → Changes persist
- [ ] Toggle task completion → Status changes immediately
- [ ] Delete task → Removed from list with confirmation
- [ ] Filter by "All" → Shows all tasks
- [ ] Filter by "Completed" → Shows only completed
- [ ] Filter by "Pending" → Shows only incomplete

**Task Management (Chatbot):**
- [ ] "add task buy milk" → Task created
- [ ] "show my tasks" → Lists all tasks
- [ ] "complete task 1" → First task marked complete
- [ ] "delete task 1" → First task deleted

**Session Management:**
- [ ] Chat during session → History preserved
- [ ] Close/reopen chatbot → History still there
- [ ] Logout → Chat cleared
- [ ] Login again → Fresh chat starts

**User Isolation:**
- [ ] Create task as User A
- [ ] Login as User B
- [ ] User B cannot see User A's tasks

---

## Known Limitations

### 1. Chatbot Conversation Persistence

**Limitation**: Conversations are stored in database but become orphaned after logout.

**Impact**: Database accumulates unused conversation records over time.

**Mitigation**: Implement periodic cleanup job to delete old conversations.

### 2. Rate Limiting Scope

**Limitation**: Rate limiting only applied to login and task creation endpoints.

**Impact**: Other endpoints (update, delete) could be spammed.

**Mitigation**: Add rate limiting to all write operations in production.

### 3. OpenAI Dependency

**Limitation**: Advanced chatbot features require OpenAI API key (costs money).

**Impact**: Without API key, chatbot uses basic intent detection (less flexible).

**Mitigation**: Intent detection fallback provides core functionality for free.

### 4. Single Database Connection

**Limitation**: SQLite default configuration doesn't support high concurrency.

**Impact**: Performance degrades under heavy load.

**Mitigation**: Use PostgreSQL in production (configured via DATABASE_URL).

### 5. Client-Side Token Storage

**Limitation**: JWT tokens stored in localStorage (vulnerable to XSS).

**Impact**: If XSS vulnerability exists, tokens could be stolen.

**Mitigation**: React auto-escaping prevents XSS; consider httpOnly cookies for enhanced security.

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'src'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem**: `Database connection error`
```bash
# Solution: Check DATABASE_URL in .env
# For SQLite: sqlite:///./local.db
# For PostgreSQL: postgresql://user:pass@host:5432/dbname
```

**Problem**: `Invalid JWT secret`
```bash
# Solution: Generate new secret
openssl rand -base64 32
# Add to .env: JWT_SECRET=<generated-secret>
```

### Frontend Issues

**Problem**: `Cannot find module '@/lib/api'`
```bash
# Solution: Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Problem**: `CORS error`
```bash
# Solution: Check CORS_ORIGINS in backend .env
# Must include: http://localhost:3000
```

### Chatbot Issues

**Problem**: Chatbot shows "Sorry, I encountered an error"
```bash
# Solution: Check backend logs for details
# Common causes:
# - Invalid OPENAI_API_KEY
# - Network timeout
# - Database connection issue
```

**Problem**: Delete command doesn't work
```bash
# Solution: Ensure function calling loop is implemented
# Check backend logs for:
# [DEBUG] Function calling iteration 1
# [DEBUG] Function calling iteration 2
```

---

## Production Deployment

**Backend:**
```bash
# Use production WSGI server
pip install gunicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
npm run build
npm start
```

**Environment Configuration:**
- Set `DEBUG=false` in production
- Use PostgreSQL instead of SQLite
- Configure proper CORS_ORIGINS
- Use strong JWT_SECRET (32+ characters)
- Enable HTTPS
- Set up monitoring and logging

---

## License

MIT

---

## Support

For issues, questions, or contributions:
- API Docs: http://localhost:8000/docs (when running)
- GitHub Issues: [Your Repo URL]

---

**Phase 3 - Production Ready** ✅
