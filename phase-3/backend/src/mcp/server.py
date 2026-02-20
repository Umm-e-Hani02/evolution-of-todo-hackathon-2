"""MCP Server for task management tools."""
from typing import Dict, Any, Callable
from sqlmodel import Session


class MCPServer:
    """
    Model Context Protocol server that exposes stateless task management tools.

    All tools are stateless and require database session to be passed in.
    """

    def __init__(self):
        """Initialize MCP server with tool registry."""
        from src.mcp.tools import (
            create_task,
            list_tasks,
            update_task,
            complete_task,
            delete_task,
        )

        self.tools: Dict[str, Callable] = {
            "create_task": create_task,
            "list_tasks": list_tasks,
            "update_task": update_task,
            "complete_task": complete_task,
            "delete_task": delete_task,
        }

    def get_tool_schemas(self) -> list[Dict[str, Any]]:
        """
        Get OpenAI function schemas for all MCP tools.

        Returns:
            List of tool schemas in OpenAI function format
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "create_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional description of the task"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task's title, description, or completion status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description for the task"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "Whether the task is completed"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to complete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task by its UUID. Call list_tasks first to get the task_id.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The UUID of the task to delete (get from list_tasks)"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    def call_tool(
        self,
        tool_name: str,
        user_id: str,
        db: Session,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call an MCP tool with the given parameters.

        Args:
            tool_name: Name of the tool to call
            user_id: User ID for authorization
            db: Database session
            **kwargs: Tool-specific parameters

        Returns:
            Tool execution result
        """
        print(f"[MCP Server] Calling tool: {tool_name}")
        print(f"[MCP Server] Parameters: user_id={user_id}, kwargs={kwargs}")

        if tool_name not in self.tools:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}

        tool_func = self.tools[tool_name]

        try:
            # All tools require user_id and db
            result = tool_func(user_id=user_id, db=db, **kwargs)
            print(f"[MCP Server] Tool {tool_name} result: success={result.get('success')}")
            return result
        except Exception as e:
            print(f"[MCP Server] Tool {tool_name} error: {e}")
            return {"success": False, "error": str(e)}


# Global MCP server instance
mcp_server = MCPServer()
