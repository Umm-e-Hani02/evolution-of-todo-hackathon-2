"""MCP tool for completing tasks."""
from typing import Dict, Any
from sqlmodel import Session, select
from src.models.todo import TodoTask
from datetime import datetime, timezone


def complete_task(user_id: str, task_id: str, db: Session = None) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        user_id: User ID who owns the task
        task_id: Task ID to complete
        db: Database session

    Returns:
        Dict with success status and task details
    """
    if not db:
        return {"success": False, "error": "Database session required"}

    try:
        statement = select(TodoTask).where(
            TodoTask.id == task_id,
            TodoTask.user_id == user_id
        )
        task = db.exec(statement).first()

        if not task:
            return {"success": False, "error": "Task not found"}

        task.completed = True
        task.updated_at = datetime.now(timezone.utc)

        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "success": True,
            "task_id": task.id,
            "title": task.title,
            "completed": task.completed
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
