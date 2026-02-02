"""Conversation model for Phase-3 AI Chatbot."""
from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4


class Conversation(SQLModel, table=True):
    """Conversation entity representing a chat session between user and AI."""

    __tablename__ = "conversations"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        description="Unique identifier for the conversation",
    )
    user_id: str = Field(
        foreign_key="users.id",  # Reference Phase-2 user table
        ondelete="CASCADE",
        description="Reference to the user who owns this conversation",
    )
    title: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Optional title for the conversation",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the conversation was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the conversation was last updated",
    )

    # Relationships
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        cascade_delete=True,
    )

    class Config:
        from_attributes = True