# Data Model: Full-Stack Multi-User Todo Web Application

**Date**: 2026-01-06
**Branch**: `002-web-todo-auth`
**Based On**: [spec.md](./spec.md) and [plan.md](./plan.md)

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Entity                               │
├─────────────────────────────────────────────────────────────────┤
│  id: UUID (PK)                                                  │
│  email: VARCHAR(255) UNIQUE NOT NULL                            │
│  password_hash: VARCHAR(255) NOT NULL                           │
│  created_at: TIMESTAMP WITH TIME ZONE                           │
│  updated_at: TIMESTAMP WITH TIME ZONE                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │ 1-to-many
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TodoTask Entity                             │
├─────────────────────────────────────────────────────────────────┤
│  id: UUID (PK)                                                  │
│  user_id: UUID (FK → users.id) ON DELETE CASCADE                │
│  title: VARCHAR(500) NOT NULL                                   │
│  description: TEXT                                              │
│  completed: BOOLEAN DEFAULT FALSE                               │
│  created_at: TIMESTAMP WITH TIME ZONE                           │
│  updated_at: TIMESTAMP WITH TIME ZONE                           │
└─────────────────────────────────────────────────────────────────┘
```

## SQLModel Entities

### User Entity

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional
from uuid import UUID

class User(SQLModel, table=True):
    """User account entity for multi-user authentication."""
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique identifier for the user account"
    )
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        description="User's email address, used for authentication"
    )
    password_hash: str = Field(
        max_length=255,
        description="bcrypt hash of the user's password"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the account was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the account was last updated"
    )

    # Relationships
    tasks: List["TodoTask"] = Relationship(
        back_populates="user",
        cascade_delete="all",
        description="All todo tasks owned by this user"
    )
```

### TodoTask Entity

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID

class TodoTask(SQLModel, table=True):
    """Todo task entity owned by a single user."""
    __tablename__ = "todo_tasks"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique identifier for the task"
    )
    user_id: UUID = Field(
        foreign_key="users.id",
        on_delete="CASCADE",
        description="Reference to owning user"
    )
    title: str = Field(
        max_length=500,
        description="Title of the task (required)"
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional detailed description of the task"
    )
    completed: bool = Field(
        default=False,
        description="Whether the task has been completed"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the task was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the task was last updated"
    )

    # Relationships
    user: User = Relationship(
        back_populates="tasks",
        description="The user who owns this task"
    )
```

## Pydantic Schemas (API Request/Response)

### User Schemas

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    """Schema for user registration request."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    """Schema for login request."""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for user data in responses (no password)."""
    id: UUID
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Schema for authentication response."""
    token: str
    user: UserResponse
```

### Todo Schemas

```python
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class TodoCreate(BaseModel):
    """Schema for creating a new todo."""
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    """Schema for updating a todo (partial)."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    """Schema for todo data in responses."""
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

## Database Migration

### Initial Schema (PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Todo tasks table
CREATE TABLE todo_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for query performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_todos_user_id ON todo_tasks(user_id);
CREATE INDEX idx_todos_user_completed ON todo_tasks(user_id, completed);
```

## Schema Mappings

| FR Reference | Entity/Field | Requirement |
|--------------|--------------|-------------|
| FR-001 | User.email, User.password_hash | User registration |
| FR-002 | JWT generation | JWT authentication |
| FR-003 | Middleware checks | Auth required on CRUD |
| FR-004 | TodoTask.title, description | Create tasks |
| FR-005 | SELECT WHERE user_id | List own tasks |
| FR-006 | UPDATE WHERE user_id | Update own tasks |
| FR-007 | DELETE WHERE user_id | Delete own tasks |
| FR-008 | CASCADE + WHERE user_id | User isolation |
| FR-009 | PostgreSQL persistence | Data persistence |
