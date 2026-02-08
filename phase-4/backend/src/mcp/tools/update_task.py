"""update_task MCP tool for Phase-3 AI Chatbot.

This tool updates a todo task for the authenticated user by interfacing with the shared todo functionality.
"""
from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from ...models.todo import TodoTask  # Import from Phase-3 models (same as Phase-2)


# OpenAI function definition for update_task tool
update_task_tool = {
    "type": "function",
    "function": {
        "name": "update_task",
        "description": "Update a todo task for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The ID of the task to update"
                },
                "title": {
                    "type": "string",
                    "description": "The new task title"
                },
                "description": {
                    "type": "string",
                    "description": "The new detailed description of the task"
                },
                "completed": {
                    "type": "boolean",
                    "description": "Whether the task is completed"
                }
            },
            "required": ["task_id"]
        }
    }
}


def update_task(
    session: Session, 
    user_id: str, 
    task_id: str, 
    title: str = None, 
    description: str = None, 
    completed: bool = None
) -> Dict[str, Any]:
    """
    Update a todo task for the user.

    Args:
        session: Database session
        user_id: User ID (string format from authentication)
        task_id: ID of the task to update
        title: New task title (optional)
        description: New task description (optional)
        completed: New completion status (optional)

    Returns:
        Dict with success status and updated task data or error message
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
                "error": "Task not found or you don't have permission to update it"
            }

        # Update fields if provided
        if title is not None:
            if len(title) > 500:
                return {
                    "success": False,
                    "error": "Task title cannot exceed 500 characters"
                }
            task.title = title.strip()
        
        if description is not None:
            task.description = description.strip() if description else None
            
        if completed is not None:
            task.completed = completed

        # Update timestamp
        from datetime import datetime, timezone
        task.updated_at = datetime.now(timezone.utc)

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "data": {
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "updated_at": task.updated_at.isoformat()
            }
        }

    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": f"Failed to update task: {str(e)}"
        }