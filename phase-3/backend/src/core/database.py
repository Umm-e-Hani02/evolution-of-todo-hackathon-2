"""Database connection and session management."""
from sqlmodel import SQLModel, create_engine, Session, select
from src.core.config import settings

import os
from urllib.parse import urlparse
import logging

def create_database_engine():
    """Create database engine with appropriate settings based on URL scheme."""
    database_url = settings.database_url
    print(f"Attempting to connect to database: {database_url[:50]}...")

    parsed_url = urlparse(database_url)

    if parsed_url.scheme == 'sqlite':
        print("Using SQLite for local development")
        return create_engine(
            database_url,
            echo=settings.debug,
            connect_args={"check_same_thread": False}
        )
    else:
        print("Using PostgreSQL for production")
        return create_engine(
            database_url,
            echo=settings.debug,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=5,
            max_overflow=10,
        )

# Create SQLModel engine
try:
    engine = create_database_engine()
    print("Database engine created successfully")
except Exception as e:
    print(f"Error creating database engine: {e}")
    raise


def get_db() -> Session:
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session


def init_db() -> None:
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)


def get_user_by_id(db: Session, user_id: str) -> "User | None":
    """Get user by UUID."""
    from src.models.user import User
    statement = select(User).where(User.id == user_id)
    return db.exec(statement).first()


def get_todos_by_user(db: Session, user_id: str) -> list["TodoTask"]:
    """Get all todos for a user."""
    from src.models.todo import TodoTask
    statement = select(TodoTask).where(TodoTask.user_id == user_id)
    return db.exec(statement).all()


def get_todo_by_id_and_user(
    db: Session, todo_id: str, user_id: str
) -> "TodoTask | None":
    """Get a specific todo only if it belongs to the user."""
    from src.models.todo import TodoTask
    statement = select(TodoTask).where(
        TodoTask.id == todo_id, TodoTask.user_id == user_id
    )
    return db.exec(statement).first()
