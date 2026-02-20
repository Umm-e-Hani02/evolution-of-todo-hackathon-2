"""Todo CRUD API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from src.core.database import get_db
from src.core.rate_limit import limiter
from src.models.user import User
from src.models.todo import TodoTask
from src.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from src.deps import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get(
    "",
    response_model=list[TodoResponse],
    summary="List all todos",
)
def list_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[TodoResponse]:
    """List all todo tasks for the authenticated user."""
    statement = select(TodoTask).where(TodoTask.user_id == current_user.id)
    todos = db.execute(statement).scalars().all()
    return [TodoResponse.model_validate(todo) for todo in todos]


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a todo",
)
@limiter.limit("30/minute")
def create_todo(
    request: Request,
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Create a new todo task for the authenticated user."""
    new_todo = TodoTask(
        user_id=current_user.id,
        title=todo_data.title,
        description=todo_data.description,
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return TodoResponse.model_validate(new_todo)


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Get a todo",
)
def get_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Get a specific todo task by ID."""
    todo = db.get(TodoTask, todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Ensure the todo belongs to the current user
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TodoResponse.model_validate(todo)


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Replace a todo",
)
def replace_todo(
    todo_id: str,
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Replace an existing todo task with new data."""
    todo = db.get(TodoTask, todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Ensure the todo belongs to the current user
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update fields from the provided data (full replacement)
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.completed = todo_data.completed  # Allow completion status to be updated in PUT

    db.commit()
    db.refresh(todo)
    return TodoResponse.model_validate(todo)


@router.patch(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Update a todo",
)
def update_todo(
    todo_id: str,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Update specific fields of an existing todo task."""
    todo = db.get(TodoTask, todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Ensure the todo belongs to the current user
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update only provided fields
    update_data = todo_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    db.commit()
    db.refresh(todo)
    return TodoResponse.model_validate(todo)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
)
def delete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete a todo task."""
    todo = db.get(TodoTask, todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Ensure the todo belongs to the current user
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(todo)
    db.commit()
