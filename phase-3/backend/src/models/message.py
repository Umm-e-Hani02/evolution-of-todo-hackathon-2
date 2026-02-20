"""Message model for chat message persistence."""
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Message(SQLModel, table=True):
    """Message entity for storing individual chat messages."""
    __tablename__ = "messages"

    id: int = Field(
        default=None,
        primary_key=True,
        description="Unique identifier for the message",
    )
    user_id: str = Field(
        foreign_key="users.id",
        ondelete="CASCADE",
        index=True,
        description="Reference to owning user",
    )
    conversation_id: int = Field(
        foreign_key="conversations.id",
        ondelete="CASCADE",
        index=True,
        description="Reference to parent conversation",
    )
    role: str = Field(
        max_length=20,
        description="Message role: 'user' or 'assistant'",
    )
    content: str = Field(
        description="Message content text",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the message was created",
    )

    # Relationships
    conversation: "Conversation" = Relationship(
        back_populates="messages",
    )
    user: "User" = Relationship(
        back_populates="messages",
    )

    class Config:
        from_attributes = True
