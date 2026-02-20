"""MCP tool for creating tasks."""
from typing import Dict, Any
from sqlmodel import Session
from src.models.todo import TodoTask


def create_task(user_id: str, title: str, description: str = None, db: Session = None) -> Dict[str, Any]:
    """
    Create a new task for the user.

    Args:
        user_id: User ID who owns the task
        title: Task title (required)
        description: Optional task description
        db: Database session

    Returns:
        Dict with task_id, title, and success status
    """
    print(f"[MCP create_task] Called with user_id={user_id}, title={title}")

    if not db:
        return {"success": False, "error": "Database session required"}

    if not title or not title.strip():
        return {"success": False, "error": "Task title is required"}

    try:
        new_task = TodoTask(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        print(f"[MCP create_task] Task created successfully: {new_task.id}")

        return {
            "success": True,
            "task_id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed
        }
    except Exception as e:
        print(f"[MCP create_task] Error: {e}")
        db.rollback()
        return {"success": False, "error": str(e)}
