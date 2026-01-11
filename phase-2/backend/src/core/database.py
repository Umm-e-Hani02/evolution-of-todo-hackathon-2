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

    # Parse the database URL to determine the type
    parsed_url = urlparse(database_url)

    if parsed_url.scheme == 'sqlite':
        # SQLite configuration for local development
        print("Using SQLite for local development")
        return create_engine(
            database_url,
            echo=settings.debug,
            connect_args={"check_same_thread": False}  # Needed for SQLite
        )
    else:
        # PostgreSQL configuration for production
        print("Using PostgreSQL for production")

        # Enhance the database URL with proper SSL settings if not present
        enhanced_url = database_url
        if "sslmode" not in database_url.lower():
            if "?" in database_url:
                enhanced_url = f"{database_url}&sslmode=require"
            else:
                enhanced_url = f"{database_url}?sslmode=require"

        print(f"Enhanced database URL: {enhanced_url[:50]}...")

        return create_engine(
            enhanced_url,
            echo=settings.debug,
            # PostgreSQL-specific options for production
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=5,  # Reduced for Railway free tier
            max_overflow=10,
            # Handle SSL properly for cloud databases like Neon/Railway
            connect_args={
                "connect_timeout": 30,  # Increased timeout for Railway
                "sslmode": "require"
            }
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
