"""list_tasks MCP tool for Phase-3 AI Chatbot.

This tool lists all todo tasks for the authenticated user by interfacing with the shared todo functionality.
"""
from typing import Dict, Any
from sqlmodel import Session, select
from ...models.todo import TodoTask  # Import from Phase-3 models (same as Phase-2)


# OpenAI function definition for list_tasks tool
list_tasks_tool = {
    "type": "function",
    "function": {
        "name": "list_tasks",
        "description": "List all todo tasks for the user, optionally filtered by completion status",
        "parameters": {
            "type": "object",
            "properties": {
                "filter": {
                    "type": "string",
                    "description": "Filter tasks by status: 'all', 'completed', or 'incomplete'",
                    "enum": ["all", "completed", "incomplete"]
                }
            },
            "required": []
        }
    }
}


def list_tasks(session: Session, user_id: str, filter: str = "all") -> Dict[str, Any]:
    """
    List all todo tasks for the user with optional filtering.

    Args:
        session: Database session
        user_id: User ID (string format from authentication)
        filter: Filter by status - "all", "completed", or "incomplete" (default: "all")

    Returns:
        Dict with success status and list of tasks or error message
    """
    try:
        # Build query
        statement = select(TodoTask).where(TodoTask.user_id == user_id)

        # Apply filter
        if filter == "completed":
            statement = statement.where(TodoTask.completed == True)
        elif filter == "incomplete":
            statement = statement.where(TodoTask.completed == False)
        # "all" - no additional filter

        # Execute query
        tasks = session.exec(statement).all()

        # Format tasks
        task_list = [
            {
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]

        return {
            "success": True,
            "data": {
                "tasks": task_list,
                "count": len(task_list),
                "filter": filter or "all"
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list tasks: {str(e)}"
        }