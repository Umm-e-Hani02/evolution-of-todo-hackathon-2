"""
ToolLog SQLModel for Phase III AI Chatbot.

Represents an MCP tool invocation for audit trail.
"""
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import JSON, Column


class ToolLog(SQLModel, table=True):
    """
    ToolLog entity representing an MCP tool invocation.

    Attributes:
        id: Unique log entry identifier (UUID)
        conversation_id: Associated conversation (foreign key)
        tool_name: Name of the tool invoked
        input: Tool input parameters (JSON)
        output: Tool output/result (JSON)
        success: Whether tool execution succeeded
        timestamp: When tool was invoked (UTC)
    """
    __tablename__ = "tool_logs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False, index=True)
    tool_name: str = Field(nullable=False, max_length=100, index=True)
    input: Dict[str, Any] = Field(sa_column=Column(JSON, nullable=False))
    output: Dict[str, Any] = Field(sa_column=Column(JSON, nullable=False))
    success: bool = Field(nullable=False, index=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="tool_logs")
