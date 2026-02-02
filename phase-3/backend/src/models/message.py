"""Message model for Phase-3 AI Chatbot."""
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4


class MessageRole(str, Enum):
    """Enum for message roles in conversation."""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """Message entity representing a single message in a conversation."""

    __tablename__ = "messages"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        description="Unique identifier for the message",
    )
    conversation_id: str = Field(
        foreign_key="conversations.id",
        ondelete="CASCADE",
        description="Reference to the parent conversation",
    )
    role: MessageRole = Field(
        description="The role of the message sender (user or assistant)"
    )
    content: str = Field(
        max_length=5000,
        description="The content of the message",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the message was created",
    )

    # Relationships
    conversation: "Conversation" = Relationship(
        back_populates="messages",
    )

    class Config:
        from_attributes = True