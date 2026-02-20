"""MCP tool for listing tasks."""
from typing import Dict, Any, List
from sqlmodel import Session, select
from src.models.todo import TodoTask


def list_tasks(user_id: str, db: Session = None) -> Dict[str, Any]:
    """
    List all tasks for the user.

    Args:
        user_id: User ID whose tasks to list
        db: Database session

    Returns:
        Dict with tasks array and count
    """
    if not db:
        return {"success": False, "error": "Database session required"}

    try:
        statement = select(TodoTask).where(TodoTask.user_id == user_id).order_by(TodoTask.created_at.desc())
        tasks = db.exec(statement).all()

        task_list = [
            {
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]

        return {
            "success": True,
            "tasks": task_list,
            "count": len(task_list)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
