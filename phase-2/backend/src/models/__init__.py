# Models Package
from sqlmodel import SQLModel

# Import all models to register them with SQLModel's metadata
from src.models.user import User
from src.models.todo import TodoTask

__all__ = ["SQLModel", "User", "TodoTask"]
