# Data Model: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot
**Date**: 2026-01-18
**Purpose**: Define database entities, relationships, and validation rules for Phase III

## Entity Overview

```
User (existing, managed by Better Auth)
  ├── has many → Conversations
  └── has many → Tasks (existing from Phase II)

Conversation
  ├── belongs to → User
  └── has many → Messages
  └── has many → ToolLogs

Message
  └── belongs to → Conversation

Task (existing from Phase II)
  └── belongs to → User

ToolLog
  └── belongs to → Conversation
```

---

## Entities

### User (Existing Entity)

**Purpose**: Represents authenticated users of the system

**Managed By**: Better Auth (existing Phase II authentication system)

**Relationships**:
- Has many Conversations (new in Phase III)
- Has many Tasks (existing from Phase II)

**Notes**:
- User entity is not modified in Phase III
- Better Auth handles user authentication, registration, and session management
- User ID is extracted from Bearer token on each request

---

### Conversation (New Entity)

**Purpose**: Represents a chat session between a user and the AI agent

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Auto-generated | Unique conversation identifier |
| user_id | UUID | Foreign Key (User), NOT NULL, Indexed | Owner of the conversation |
| created_at | DateTime | NOT NULL, Default: UTC now | When conversation was created |
| updated_at | DateTime | NOT NULL, Default: UTC now, Auto-update | Last message timestamp |

**Relationships**:
- Belongs to User (user_id → users.id)
- Has many Messages (conversation_id ← messages.conversation_id)
- Has many ToolLogs (conversation_id ← tool_logs.conversation_id)

**Validation Rules**:
- `user_id` must reference existing user
- `created_at` must be <= `updated_at`
- Timestamps must be in UTC

**Indexes**:
- Primary: `id`
- Foreign Key: `user_id` (for efficient user conversation queries)
- Composite: `(user_id, updated_at DESC)` (for listing user's recent conversations)

**Soft Delete**: Yes (add `deleted_at` field for soft deletes)

**State Transitions**: None (conversations don't have explicit states)

---

### Message (New Entity)

**Purpose**: Represents a single message in a conversation (user or assistant)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Auto-generated | Unique message identifier |
| conversation_id | UUID | Foreign Key (Conversation), NOT NULL, Indexed | Parent conversation |
| role | Enum | NOT NULL, Values: 'user', 'assistant' | Who sent the message |
| content | Text | NOT NULL, Max length: 10000 chars | Message content |
| timestamp | DateTime | NOT NULL, Default: UTC now, Indexed | When message was sent |

**Relationships**:
- Belongs to Conversation (conversation_id → conversations.id)

**Validation Rules**:
- `conversation_id` must reference existing conversation
- `role` must be either 'user' or 'assistant'
- `content` must not be empty (min length: 1 char)
- `content` max length: 10000 characters (prevents abuse)
- `timestamp` must be in UTC

**Indexes**:
- Primary: `id`
- Foreign Key: `conversation_id` (for efficient conversation message queries)
- Composite: `(conversation_id, timestamp ASC)` (for chronological message ordering)

**Soft Delete**: No (messages are permanent for audit trail)

**Ordering**: Messages ordered by `timestamp` ASC within a conversation

**State Transitions**: None (messages are immutable once created)

---

### Task (Existing Entity - Modified)

**Purpose**: Represents a todo item

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Auto-generated | Unique task identifier |
| user_id | UUID | Foreign Key (User), NOT NULL, Indexed | Owner of the task |
| title | String | NOT NULL, Max length: 500 chars | Task description |
| completed | Boolean | NOT NULL, Default: false | Completion status |
| created_at | DateTime | NOT NULL, Default: UTC now | When task was created |
| updated_at | DateTime | NOT NULL, Default: UTC now, Auto-update | Last modification timestamp |

**Relationships**:
- Belongs to User (user_id → users.id)

**Validation Rules**:
- `user_id` must reference existing user
- `title` must not be empty (min length: 1 char)
- `title` max length: 500 characters
- `completed` defaults to false
- Timestamps must be in UTC

**Indexes**:
- Primary: `id`
- Foreign Key: `user_id` (for efficient user task queries)
- Composite: `(user_id, completed, created_at DESC)` (for filtering and sorting)

**Soft Delete**: Yes (add `deleted_at` field if not already present)

**State Transitions**:
- `completed: false` → `completed: true` (via complete_task tool)
- `completed: true` → `completed: false` (not supported in Phase III, but possible in future)

**Notes**:
- Task entity exists from Phase II
- No schema changes required for Phase III
- Accessed via MCP tools only (not directly by agent)

---

### ToolLog (New Entity)

**Purpose**: Audit trail for all MCP tool invocations

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Auto-generated | Unique log entry identifier |
| conversation_id | UUID | Foreign Key (Conversation), NOT NULL, Indexed | Associated conversation |
| tool_name | String | NOT NULL, Max length: 100 chars | Name of the tool invoked |
| input | JSON | NOT NULL | Tool input parameters |
| output | JSON | NOT NULL | Tool output/result |
| success | Boolean | NOT NULL | Whether tool execution succeeded |
| timestamp | DateTime | NOT NULL, Default: UTC now, Indexed | When tool was invoked |

**Relationships**:
- Belongs to Conversation (conversation_id → conversations.id)

**Validation Rules**:
- `conversation_id` must reference existing conversation
- `tool_name` must not be empty
- `tool_name` must match one of: create_task, list_tasks, update_task, complete_task, delete_task
- `input` must be valid JSON
- `output` must be valid JSON
- `timestamp` must be in UTC

**Indexes**:
- Primary: `id`
- Foreign Key: `conversation_id` (for conversation audit trail)
- Composite: `(conversation_id, timestamp ASC)` (for chronological tool log ordering)
- Single: `tool_name` (for tool usage analytics)
- Single: `success` (for error rate monitoring)

**Soft Delete**: No (audit logs are permanent)

**Ordering**: Tool logs ordered by `timestamp` ASC within a conversation

**State Transitions**: None (tool logs are immutable once created)

**Example Records**:

```json
// Successful create_task
{
  "id": "uuid-1",
  "conversation_id": "conv-uuid",
  "tool_name": "create_task",
  "input": {"title": "Buy groceries", "user_id": "user-uuid"},
  "output": {"success": true, "data": {"task_id": "task-uuid", "title": "Buy groceries"}},
  "success": true,
  "timestamp": "2026-01-18T10:30:00Z"
}

// Failed complete_task (task not found)
{
  "id": "uuid-2",
  "conversation_id": "conv-uuid",
  "tool_name": "complete_task",
  "input": {"task_id": "nonexistent-uuid", "user_id": "user-uuid"},
  "output": {"success": false, "error": "Task not found"},
  "success": false,
  "timestamp": "2026-01-18T10:31:00Z"
}
```

---

## Database Schema Migrations

### New Tables (Phase III)

1. **conversations**
   - Add table with fields: id, user_id, created_at, updated_at, deleted_at
   - Add foreign key: user_id → users.id
   - Add indexes: user_id, (user_id, updated_at DESC)

2. **messages**
   - Add table with fields: id, conversation_id, role, content, timestamp
   - Add foreign key: conversation_id → conversations.id
   - Add indexes: conversation_id, (conversation_id, timestamp ASC)
   - Add check constraint: role IN ('user', 'assistant')

3. **tool_logs**
   - Add table with fields: id, conversation_id, tool_name, input, output, success, timestamp
   - Add foreign key: conversation_id → conversations.id
   - Add indexes: conversation_id, (conversation_id, timestamp ASC), tool_name, success

### Modified Tables (Phase III)

**tasks** (if soft delete not already implemented):
- Add field: deleted_at (DateTime, NULL, Default: NULL)
- Add index: (user_id, deleted_at, completed, created_at DESC)

---

## Data Access Patterns

### Conversation Loading (Most Frequent)
```sql
-- Load conversation with last 50 messages
SELECT * FROM messages
WHERE conversation_id = ?
ORDER BY timestamp DESC
LIMIT 50;
```

### User's Recent Conversations
```sql
-- List user's conversations, most recent first
SELECT * FROM conversations
WHERE user_id = ? AND deleted_at IS NULL
ORDER BY updated_at DESC
LIMIT 20;
```

### Task Operations (via MCP Tools)
```sql
-- Create task
INSERT INTO tasks (id, user_id, title, completed, created_at, updated_at)
VALUES (?, ?, ?, false, NOW(), NOW());

-- List user's tasks
SELECT * FROM tasks
WHERE user_id = ? AND deleted_at IS NULL
ORDER BY created_at DESC;

-- Complete task
UPDATE tasks
SET completed = true, updated_at = NOW()
WHERE id = ? AND user_id = ?;
```

### Audit Trail Query
```sql
-- Get all tool calls for a conversation
SELECT * FROM tool_logs
WHERE conversation_id = ?
ORDER BY timestamp ASC;
```

---

## Data Retention Policy

- **Conversations**: Soft delete, retained indefinitely (can be purged manually if needed)
- **Messages**: Hard delete not supported, retained indefinitely for audit trail
- **Tasks**: Soft delete, retained indefinitely (existing Phase II behavior)
- **ToolLogs**: Hard delete not supported, retained indefinitely for audit trail

**Future Considerations**:
- Implement automatic archival of conversations older than 1 year
- Implement conversation export feature for users
- Add GDPR-compliant data deletion workflow

---

## Performance Considerations

**Expected Query Performance**:
- Load 50 messages: <10ms (indexed by conversation_id + timestamp)
- List user conversations: <10ms (indexed by user_id + updated_at)
- Task CRUD operations: <5ms (indexed by user_id)
- Tool log insertion: <5ms (simple insert)

**Optimization Strategies**:
- Use connection pooling (SQLModel/SQLAlchemy default)
- Limit conversation history to 50 messages (prevents large result sets)
- Use composite indexes for common query patterns
- Consider read replicas if read load becomes high (future)

---

## Security Considerations

**Authorization**:
- All queries scoped to authenticated user_id
- No cross-user data access possible
- Foreign key constraints enforce referential integrity

**Data Validation**:
- SQLModel validates field types and constraints
- Application layer validates business rules
- Database constraints enforce data integrity

**Audit Trail**:
- ToolLogs provide complete audit trail of all AI actions
- Messages provide complete conversation history
- Timestamps enable temporal analysis

---

## Testing Strategy

**Unit Tests (Models)**:
- Test field validation (required fields, max lengths, enums)
- Test relationship definitions (foreign keys, cascades)
- Test default values and auto-generated fields

**Integration Tests (Database)**:
- Test CRUD operations for each entity
- Test relationship queries (join queries)
- Test soft delete behavior
- Test constraint violations (foreign key, unique, check)

**Performance Tests**:
- Benchmark conversation loading with 50 messages
- Benchmark task list queries with 1000+ tasks
- Verify index usage with EXPLAIN ANALYZE
