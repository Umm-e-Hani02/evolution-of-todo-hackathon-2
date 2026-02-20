"""Agent runner for Phase-3 AI Chatbot.

Handles OpenAI Agent initialization and execution using the OpenAI Agents SDK.
"""
import os
import json
from typing import List, Dict, Any

from openai import OpenAI
from dotenv import load_dotenv

from .instructions import AGENT_INSTRUCTIONS

# Load environment variables
load_dotenv()

# Get OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "30"))

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")


class AgentRunner:
    """
    Agent runner for executing conversational AI with MCP tools.

    Uses OpenAI Agents SDK to process user messages and execute tool calls.
    """

    def __init__(self, tools: List[Dict[str, Any]]):
        """
        Initialize AgentRunner with MCP tools.

        Args:
            tools: List of MCP tool definitions (OpenAI function format)
        """
        # Check if using OpenRouter API key (starts with sk-or-v1)
        if OPENAI_API_KEY.startswith("sk-or-v1-"):
            # Configure for OpenRouter
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENAI_API_KEY,
            )
            # Default to a model that works well with OpenRouter
            self.model = OPENAI_MODEL if OPENAI_MODEL else "openai/gpt-3.5-turbo"
        else:
            # Standard OpenAI configuration
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.model = OPENAI_MODEL if OPENAI_MODEL else "gpt-4"

        self.tools = tools
        self.instructions = AGENT_INSTRUCTIONS

    def run(
        self,
        messages: List[Dict[str, str]],
        tool_executor: callable
    ) -> Dict[str, Any]:
        """
        Run the agent with conversation history and execute tool calls.

        Args:
            messages: Conversation history in OpenAI format
                     [{"role": "user", "content": "..."}, ...]
            tool_executor: Callable that executes tool calls
                          Takes (tool_name, arguments) and returns result

        Returns:
            Dict containing:
                - message: Agent's response message
                - tool_calls: List of tool calls executed
        """
        # Add system message with instructions
        full_messages = [
            {"role": "system", "content": self.instructions}
        ] + messages

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            tools=self.tools if self.tools else None,
            tool_choice="auto" if self.tools else None,
            timeout=AGENT_TIMEOUT
        )

        # Extract response
        message = response.choices[0].message
        tool_calls_executed = []

        # Execute tool calls if any
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name

                # Parse JSON arguments safely
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError as e:
                    # If JSON parsing fails, return error
                    tool_args = {}
                    tool_result = {
                        "success": False,
                        "error": f"Invalid JSON in tool arguments: {str(e)}"
                    }
                else:
                    # Execute tool
                    tool_result = tool_executor(tool_name, tool_args)

                tool_calls_executed.append({
                    "tool_name": tool_name,
                    "input": tool_args,
                    "output": tool_result,
                    "success": tool_result.get("success", False)
                })

                # Add tool result to messages for next iteration
                full_messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }]
                })
                full_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result)
                })

            # Get final response after tool execution
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                timeout=AGENT_TIMEOUT
            )
            final_message = final_response.choices[0].message.content
        else:
            final_message = message.content

        return {
            "message": final_message or "",
            "tool_calls": tool_calls_executed
        }