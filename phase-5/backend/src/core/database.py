"""Database connection and session management."""
from sqlmodel import SQLModel, create_engine, Session
from src.core.config import settings
from urllib.parse import urlparse

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
