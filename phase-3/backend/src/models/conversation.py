"""Conversation model for chat history persistence."""
from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4


class Conversation(SQLModel, table=True):
    """Conversation entity for storing chat sessions."""
    __tablename__ = "conversations"

    id: int = Field(
        default=None,
        primary_key=True,
        description="Unique identifier for the conversation",
    )
    user_id: str = Field(
        foreign_key="users.id",
        ondelete="CASCADE",
        index=True,
        description="Reference to owning user",
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
        cascade_delete="all",
    )
    user: "User" = Relationship(
        back_populates="conversations",
    )

    class Config:
        from_attributes = True
