"""MCP Server for Phase-3 AI Chatbot.

Manages and provides access to all MCP tools for the AI agent.
"""
from typing import Dict, Any, List, Callable
from sqlmodel import Session

from .tools.create_task import create_task_tool, create_task
from .tools.list_tasks import list_tasks_tool, list_tasks
from .tools.update_task import update_task_tool, update_task
from .tools.complete_task import complete_task_tool, complete_task
from .tools.delete_task import delete_task_tool, delete_task


class MCPServer:
    """
    MCP Server for managing and executing tools.

    Provides a registry of tools and executes them with proper session management.
    """

    def __init__(self):
        """Initialize MCP Server with tool registry."""
        self.tools: Dict[str, Callable] = {
            "create_task": create_task,
            "list_tasks": list_tasks,
            "update_task": update_task,
            "complete_task": complete_task,
            "delete_task": delete_task
        }

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get OpenAI-compatible tool definitions for all registered tools.

        Returns:
            List[Dict]: Tool definitions in OpenAI function format
        """
        return [
            create_task_tool,
            list_tasks_tool,
            update_task_tool,
            complete_task_tool,
            delete_task_tool
        ]

    def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        session: Session,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Execute a tool by name with given arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments (from agent)
            session: Database session for tool execution
            user_id: Authenticated user ID (injected by backend)

        Returns:
            Dict: Tool execution result with success status and data/error
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        try:
            tool_func = self.tools[tool_name]
            # Inject user_id into arguments - agent never sees this
            result = tool_func(session=session, user_id=user_id, **arguments)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global MCP server instance
mcp_server = MCPServer()