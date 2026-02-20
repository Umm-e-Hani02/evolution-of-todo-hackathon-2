"""SQLModel models for Phase-3 AI Chatbot."""

from sqlmodel import SQLModel

# Import all models to register them with SQLModel's metadata
# Phase 2 models (reused)
from src.models.user import User
from src.models.todo import TodoTask

# Phase 3 models (new)
from src.models.conversation import Conversation
from src.models.message import Message

__all__ = ["SQLModel", "User", "TodoTask", "Conversation", "Message"]