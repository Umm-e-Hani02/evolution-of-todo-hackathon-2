"""Database connection and session management."""
from sqlmodel import SQLModel, create_engine, Session, select
from src.core.config import settings

import os
from urllib.parse import urlparse
import logging

def create_database_engine():
    """Create database engine with appropriate settings based on URL scheme."""
    # Clean the database URL by removing any shell command prefixes like "psql '"
    raw_database_url = settings.database_url
    database_url = raw_database_url.strip()

    # Remove common shell command prefixes that might be accidentally included
    if database_url.startswith("psql '"):
        database_url = database_url[6:]  # Remove "psql '" prefix
    elif database_url.startswith("psql \""):
        database_url = database_url[6:]  # Remove 'psql "' prefix
    elif database_url.startswith("'") and database_url.endswith("'"):
        database_url = database_url[1:-1]  # Remove surrounding quotes
    elif database_url.startswith('"') and database_url.endswith('"'):
        database_url = database_url[1:-1]  # Remove surrounding quotes

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
        # PostgreSQL configuration for production - use cleaned URL
        print("Using PostgreSQL for production")

        # Ensure the URL specifies the psycopg driver if not already specified
        if database_url.startswith("postgresql://") and "+psycopg" not in database_url:
            # Replace postgresql:// with postgresql+psycopg:// to force the correct driver
            corrected_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        else:
            corrected_url = database_url

        return create_engine(
            corrected_url,  # Use the corrected URL with proper driver
            echo=settings.debug,
            # PostgreSQL-specific options for production
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=5,  # Reduced for Railway free tier
            max_overflow=10,
            # Use connection parameters from the URL
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
