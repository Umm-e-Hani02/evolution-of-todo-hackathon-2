"""Pydantic schemas for todo operations."""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class TodoCreate(BaseModel):
    """Schema for creating a new todo or replacing an existing todo."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Title of the task (1-500 characters)",
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional detailed description of the task",
    )
    completed: bool = Field(
        default=False,
        description="Whether the task has been completed",
    )


class TodoUpdate(BaseModel):
    """Schema for updating a todo (partial)."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Title of the task (1-500 characters)",
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional detailed description of the task",
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Whether the task has been completed",
    )


class TodoResponse(BaseModel):
    """Schema for todo data in responses."""

    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
