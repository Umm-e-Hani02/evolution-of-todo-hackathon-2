"""MCP tool for deleting tasks."""
from typing import Dict, Any
from sqlmodel import Session, select
from src.models.todo import TodoTask


def delete_task(user_id: str, task_id: str, db: Session = None) -> Dict[str, Any]:
    """
    Delete a task.

    Args:
        user_id: User ID who owns the task
        task_id: Task ID to delete
        db: Database session

    Returns:
        Dict with success status
    """
    print(f"[MCP delete_task] Called with user_id={user_id}, task_id={task_id}, task_id_type={type(task_id)}")

    if not db:
        return {"success": False, "error": "Database session required"}

    try:
        statement = select(TodoTask).where(
            TodoTask.id == task_id,
            TodoTask.user_id == user_id
        )
        task = db.exec(statement).first()

        if not task:
            print(f"[MCP delete_task] Task not found: task_id={task_id}, user_id={user_id}")
            return {"success": False, "error": "Task not found"}

        title = task.title
        print(f"[MCP delete_task] Deleting task: {title}")
        db.delete(task)
        db.commit()
        print(f"[MCP delete_task] Task deleted successfully")

        return {
            "success": True,
            "task_id": task_id,
            "title": title,
            "message": f"Task '{title}' deleted successfully"
        }
    except Exception as e:
        print(f"[MCP delete_task] Error: {e}")
        db.rollback()
        return {"success": False, "error": str(e)}
