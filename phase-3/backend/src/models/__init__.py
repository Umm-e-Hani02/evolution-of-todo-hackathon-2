# Models Package
from sqlmodel import SQLModel

# Import all models to register them with SQLModel's metadata
from src.models.user import User
from src.models.todo import TodoTask
from src.models.conversation import Conversation
from src.models.message import Message

__all__ = ["SQLModel", "User", "TodoTask", "Conversation", "Message"]
