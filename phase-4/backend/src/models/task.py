"""
Task SQLModel for Phase III AI Chatbot.

This is the existing Task model from Phase II, included here for reference.
The actual Task model should be imported from the Phase II backend.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.

    Attributes:
        id: Unique task identifier (UUID)
        user_id: Owner of the task (foreign key to users table, string to match Phase II)
        title: Task description (max 500 characters)
        completed: Completion status (default: false)
        created_at: When task was created (UTC)
        updated_at: Last modification timestamp (UTC)
        deleted_at: Soft delete timestamp (UTC, nullable)
    """
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(nullable=False, index=True, max_length=36)  # Don't reference users table since it's external
    title: str = Field(nullable=False, max_length=500)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    deleted_at: Optional[datetime] = Field(default=None)
