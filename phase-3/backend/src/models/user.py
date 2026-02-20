"""User model for SQLModel."""
from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4


class User(SQLModel, table=True):
    """User account entity for multi-user authentication."""
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        description="Unique identifier for the user account",
    )
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User's email address, used for authentication",
    )
    password_hash: str = Field(
        max_length=255,
        description="bcrypt hash of the user's password",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the account was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the account was last updated",
    )

    # Relationships
    tasks: List["TodoTask"] = Relationship(
        back_populates="user",
        cascade_delete="all",
    )
    conversations: List["Conversation"] = Relationship(
        back_populates="user",
        cascade_delete="all",
    )
    messages: List["Message"] = Relationship(
        back_populates="user",
        cascade_delete="all",
    )

    class Config:
        from_attributes = True
