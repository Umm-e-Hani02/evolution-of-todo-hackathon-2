"""Database connection and session management."""
from sqlmodel import SQLModel, create_engine, Session, select
from src.core.config import settings

# Create SQLModel engine
# Use SQLite for testing to avoid PostgreSQL dependency issues
engine = create_engine(
    "sqlite:///./test.db",
    echo=settings.debug,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)


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
