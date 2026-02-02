"""TodoTask model for SQLModel."""
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4


class TodoTask(SQLModel, table=True):
    """Todo task entity owned by a single user."""

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        description="Unique identifier for the task",
    )
    user_id: str = Field(
        foreign_key="users.id",
        ondelete="CASCADE",
        description="Reference to owning user",
    )
    title: str = Field(
        max_length=500,
        description="Title of the task (required)",
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional detailed description of the task",
    )
    completed: bool = Field(
        default=False,
        description="Whether the task has been completed",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the task was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the task was last updated",
    )

    # Relationships
    user: "User" = Relationship(
        back_populates="tasks",
    )

    class Config:
        from_attributes = True
