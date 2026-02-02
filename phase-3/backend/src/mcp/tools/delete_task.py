"""delete_task MCP tool for Phase-3 AI Chatbot.

This tool deletes a todo task for the authenticated user by interfacing with the shared todo functionality.
"""
from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from ...models.todo import TodoTask  # Import from Phase-3 models (same as Phase-2)


# OpenAI function definition for delete_task tool
delete_task_tool = {
    "type": "function",
    "function": {
        "name": "delete_task",
        "description": "Delete a todo task for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The ID of the task to delete"
                }
            },
            "required": ["task_id"]
        }
    }
}


def delete_task(session: Session, user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Delete a todo task for the user.

    Args:
        session: Database session
        user_id: User ID (string format from authentication)
        task_id: ID of the task to delete

    Returns:
        Dict with success status and confirmation or error message
    """
    try:
        # Validate task_id
        try:
            UUID(task_id)  # Validate UUID format
        except ValueError:
            return {
                "success": False,
                "error": "Invalid task ID format"
            }

        # Find task
        statement = select(TodoTask).where(
            TodoTask.id == task_id,
            TodoTask.user_id == user_id
        )
        task = session.exec(statement).first()

        if not task:
            return {
                "success": False,
                "error": "Task not found or you don't have permission to delete it"
            }

        # Delete the task
        session.delete(task)
        session.commit()

        return {
            "success": True,
            "data": {
                "task_id": str(task.id),
                "title": task.title,
                "deleted": True
            }
        }

    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": f"Failed to delete task: {str(e)}"
        }