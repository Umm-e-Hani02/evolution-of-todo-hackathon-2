"""create_task MCP tool for Phase-3 AI Chatbot.

This tool creates a new todo task for the authenticated user by interfacing with the shared todo functionality.
"""
from typing import Dict, Any
from sqlmodel import Session
from ...models.todo import TodoTask  # Import from Phase-3 models (same as Phase-2)


# OpenAI function definition for create_task tool
create_task_tool = {
    "type": "function",
    "function": {
        "name": "create_task",
        "description": "Create a new todo task for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The task title/description"
                },
                "description": {
                    "type": "string",
                    "description": "Optional detailed description of the task"
                }
            },
            "required": ["title"]
        }
    }
}


def create_task(session: Session, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
    """
    Create a new todo task for the user.

    Args:
        session: Database session
        user_id: User ID (string format from authentication)
        title: Task title/description
        description: Optional detailed description

    Returns:
        Dict with success status and task data or error message
    """
    try:
        # Validate inputs
        if not title or len(title.strip()) == 0:
            return {
                "success": False,
                "error": "Task title cannot be empty"
            }

        if len(title) > 500:
            return {
                "success": False,
                "error": "Task title cannot exceed 500 characters"
            }

        # Create task using shared TodoTask model
        task = TodoTask(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )

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
                "created_at": task.created_at.isoformat()
            }
        }

    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": f"Failed to create task: {str(e)}"
        }