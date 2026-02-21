"""Stateless chatbot service with database-backed conversation persistence."""
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlmodel import Session, select
from openai import OpenAI

from src.models.conversation import Conversation
from src.models.message import Message
from src.mcp.server import mcp_server
from src.services.intent_detector import IntentDetector


class StatelessChatbotService:
    """
    Stateless chatbot service that stores all conversation state in the database.

    CRITICAL: This service maintains NO in-memory state. Every request:
    1. Fetches conversation history from database
    2. Builds agent context from database records
    3. Executes agent with MCP tools
    4. Stores results in database
    5. Returns response (server forgets everything)
    """

    def __init__(self):
        """Initialize OpenAI client and intent detector."""
        from src.core.config import settings

        api_key = settings.openai_api_key
        if not api_key:
            print("WARNING: OPENAI_API_KEY not set. Task operations will still work via intent detection.")
            self.client = None
        else:
            # Check if this is an OpenRouter key
            if api_key.startswith("sk-or-"):
                print(f"INFO: Using OpenRouter with key: {api_key[:20]}...")
                self.client = OpenAI(
                    api_key=api_key,
                    base_url="https://openrouter.ai/api/v1"
                )
                # Use OpenRouter model format if not explicitly set
                self.model = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")
            else:
                print(f"INFO: OpenAI client initialized with key: {api_key[:20]}...")
                self.client = OpenAI(api_key=api_key)
                # Use standard OpenAI model format
                self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        self.intent_detector = IntentDetector()

    def get_or_create_conversation(
        self,
        user_id: str,
        conversation_id: Optional[int],
        db: Session
    ) -> Conversation:
        """
        Get existing conversation or create new one.

        Args:
            user_id: User ID
            conversation_id: Optional conversation ID
            db: Database session

        Returns:
            Conversation object
        """
        if conversation_id:
            # Fetch existing conversation
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            conversation = db.exec(statement).first()

            if conversation:
                return conversation

        # Create new conversation
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    def get_conversation_messages(
        self,
        conversation_id: int,
        db: Session
    ) -> List[Message]:
        """
        Fetch all messages for a conversation from database.

        Args:
            conversation_id: Conversation ID
            db: Database session

        Returns:
            List of messages ordered by creation time
        """
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        return db.exec(statement).all()

    def store_message(
        self,
        user_id: str,
        conversation_id: int,
        role: str,
        content: str,
        db: Session
    ) -> Message:
        """
        Store a message in the database.

        Args:
            user_id: User ID
            conversation_id: Conversation ID
            role: Message role ('user' or 'assistant')
            content: Message content
            db: Database session

        Returns:
            Created message object
        """
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        # Update conversation timestamp
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = db.exec(statement).first()
        if conversation:
            conversation.updated_at = datetime.now(timezone.utc)
            db.add(conversation)
            db.commit()

        return message

    def build_messages_for_agent(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        Build OpenAI messages array from database messages.

        Args:
            messages: List of Message objects from database

        Returns:
            List of message dicts for OpenAI API
        """
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

    def handle_chat(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[int],
        db: Session
    ) -> Dict[str, Any]:
        """
        Handle a chat message in a stateless manner.

        STATELESS FLOW:
        1. Get or create conversation (from DB)
        2. Fetch all previous messages (from DB)
        3. Store new user message (to DB)
        4. Build agent context (from DB records)
        5. Run agent with MCP tools
        6. Store assistant response (to DB)
        7. Return response + conversation_id
        8. Forget everything (no in-memory state)

        Args:
            user_id: User ID
            message: User's message
            conversation_id: Optional conversation ID
            db: Database session

        Returns:
            Dict with conversation_id, response, and tool_calls
        """
        try:
            # Step 1: Get or create conversation
            conversation = self.get_or_create_conversation(user_id, conversation_id, db)

            # Step 2: Fetch all previous messages from database
            previous_messages = self.get_conversation_messages(conversation.id, db)

            # Debug: Log conversation history
            print(f"[DEBUG] Conversation {conversation.id}: Fetched {len(previous_messages)} previous messages")
            for msg in previous_messages[-5:]:  # Show last 5 messages
                print(f"  {msg.role}: {msg.content[:100]}")

            # Step 3: Store user message in database
            self.store_message(user_id, conversation.id, "user", message, db)

            print(f"[DEBUG] Stored new user message: {message}")

            # Step 4: Check if OpenAI client is available
            if not self.client:
                # Fallback to intent detection when OpenAI is not configured
                intent = self.intent_detector.detect_intent(message)

                if intent["is_task_related"]:
                    response_text = self._handle_task_intent(intent, user_id, db)
                else:
                    response_text = "I'm here to help you manage your tasks! You can ask me to add tasks, show your task list, or help with other task management needs."

                tool_calls_data = []

                # Store assistant response in database
                self.store_message(user_id, conversation.id, "assistant", response_text, db)

                # Return response
                return {
                    "conversation_id": conversation.id,
                    "response": response_text,
                    "tool_calls": tool_calls_data
                }

            # Step 4: Build agent context from database records (OpenAI available)
            messages = self.build_messages_for_agent(previous_messages)
            messages.append({"role": "user", "content": message})

            # Debug: Log what's being sent to OpenAI
            print(f"[DEBUG] Sending {len(messages)} messages to OpenAI:")
            for i, msg in enumerate(messages[-5:]):  # Show last 5 messages
                print(f"  {i}: {msg['role']}: {msg['content'][:100]}")

            # Step 5: Run OpenAI agent with MCP tools
            system_message = {
                "role": "system",
                "content": """You are a helpful AI assistant that manages tasks using natural language.

Your job:
- Understand natural language and respond conversationally
- Manage tasks using the provided tools when needed
- Be friendly, helpful, and human-like

Rules:
- When users want to add, delete, update, complete, or list tasks, use the appropriate tool
- When users ask general questions or greet you, respond naturally without using tools
- Do not repeat the same greeting - vary your responses
- Do not show technical instructions or mention API keys
- Maintain context from conversation history
- Be concise but friendly

IMPORTANT - Task IDs:
- Tasks have UUID IDs (e.g., "abc-123-def-456")
- When user says "delete task 1", you MUST:
  1. First call list_tasks to see all tasks
  2. Find the task at position 1 in the list
  3. Extract its task_id (the UUID)
  4. Call delete_task with that UUID
- NEVER pass "1" or "2" as task_id - always use the actual UUID from list_tasks

Examples:

User: What can you do?
You: I can help you manage your tasks! You can ask me to add tasks, show your list, mark tasks as complete, or delete tasks. What would you like to do?

User: Add a task to buy milk
You: (Use create_task tool, then respond) Got it! I've added "buy milk" to your tasks.

User: Show my tasks
You: (Use list_tasks tool, then show the list naturally)

User: Delete task 1
You: (First use list_tasks to get all tasks, find task at index 0, extract its task_id UUID, then use delete_task with that UUID) Done! I've removed that task.

User: Hi
You: Hey! How can I help you with your tasks today?

Remember: Be conversational and natural. Use tools when needed, but respond like a human assistant. Always get the actual UUID from list_tasks before deleting."""
            }

            # Function calling loop - allow AI to make multiple tool calls
            conversation_messages = [system_message] + messages
            tool_calls_data = []
            max_iterations = 5  # Prevent infinite loops

            for iteration in range(max_iterations):
                print(f"[DEBUG] Function calling iteration {iteration + 1}")

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=conversation_messages,
                    tools=mcp_server.get_tool_schemas(),
                    tool_choice="auto",
                    max_tokens=500,
                    temperature=0.7
                )

                print(f"[DEBUG] OpenAI response received")
                print(f"[DEBUG] Model used: {response.model}")
                print(f"[DEBUG] Finish reason: {response.choices[0].finish_reason}")

                assistant_message = response.choices[0].message

                print(f"[DEBUG] Assistant message content: {assistant_message.content[:200] if assistant_message.content else 'None'}")
                print(f"[DEBUG] Tool calls: {len(assistant_message.tool_calls) if assistant_message.tool_calls else 0}")

                # If no tool calls, AI is done - return the response
                if not assistant_message.tool_calls:
                    response_text = assistant_message.content or "I'm here to help with your tasks!"
                    break

                # Add assistant message with tool calls to conversation
                conversation_messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })

                # Execute all tool calls and add results to conversation
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    print(f"[DEBUG] Executing tool: {tool_name} with args: {tool_args}")

                    # Execute MCP tool (stateless, uses DB)
                    result = mcp_server.call_tool(
                        tool_name=tool_name,
                        user_id=user_id,
                        db=db,
                        **tool_args
                    )

                    print(f"[DEBUG] Tool result: {result}")

                    tool_calls_data.append({
                        "tool": tool_name,
                        "arguments": tool_args,
                        "result": result
                    })

                    # Add tool result to conversation so AI can see it
                    conversation_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })

                # Continue loop - AI will see tool results and decide next action
            else:
                # Max iterations reached
                print(f"[DEBUG] Max iterations reached, formatting tool results")
                response_text = self._format_tool_response(tool_calls_data)

            # Step 6: Store assistant response in database
            self.store_message(user_id, conversation.id, "assistant", response_text, db)

            # Step 7: Return response (server forgets everything after this)
            return {
                "conversation_id": conversation.id,
                "response": response_text,
                "tool_calls": tool_calls_data
            }

        except Exception as e:
            print(f"Chat error: {e}")
            # Use conversation.id (always valid) instead of conversation_id parameter (could be None)
            return {
                "conversation_id": conversation.id,
                "response": f"Sorry, I encountered an error: {str(e)}",
                "tool_calls": []
            }

    def _handle_task_intent(self, intent: Dict[str, Any], user_id: str, db: Session) -> str:
        """
        Handle task-related intents directly via MCP tools (no OpenAI needed).

        Args:
            intent: Intent detection result
            user_id: User ID
            db: Database session

        Returns:
            Response message
        """
        action = intent["action"]
        entities = intent["entities"]

        if action == "create":
            title = entities.get("title")
            if not title:
                return "What task would you like me to add? Just tell me the task name!"

            result = mcp_server.call_tool("create_task", user_id, db, title=title)
            if result.get("success"):
                return f"✓ Got it! I've added '{result['title']}' to your task list."
            else:
                return f"I had trouble adding that task. Could you try again?"

        elif action == "list":
            result = mcp_server.call_tool("list_tasks", user_id, db)
            if result.get("success"):
                count = result.get("count", 0)
                if count == 0:
                    return "You don't have any tasks yet. Want to add one?"

                tasks = result.get("tasks", [])
                task_list = []
                for idx, task in enumerate(tasks, 1):
                    status = "✓" if task["completed"] else "○"
                    task_list.append(f"{idx}. {status} {task['title']}")

                return f"Here are your {count} task(s):\n" + "\n".join(task_list)
            else:
                return "I couldn't retrieve your tasks right now. Please try again."

        elif action == "delete":
            # Check if task number or name was provided
            task_number = entities.get("task_number")
            task_name = entities.get("task_name")

            # Get user's tasks
            result = mcp_server.call_tool("list_tasks", user_id, db)
            if not result.get("success"):
                return "I couldn't retrieve your tasks right now. Please try again."

            tasks = result.get("tasks", [])
            if not tasks:
                return "You don't have any tasks to delete."

            # Find the task to delete
            task_to_delete = None

            if task_number:
                # Delete by number (1-indexed)
                if 1 <= task_number <= len(tasks):
                    task_to_delete = tasks[task_number - 1]
                else:
                    return f"I couldn't find task number {task_number}. You have {len(tasks)} task(s)."

            elif task_name:
                # Delete by name (fuzzy match)
                task_name_lower = task_name.lower()
                for task in tasks:
                    if task_name_lower in task["title"].lower():
                        task_to_delete = task
                        break

                if not task_to_delete:
                    return f"I couldn't find a task matching '{task_name}'. Could you be more specific?"

            if task_to_delete:
                # Execute delete
                delete_result = mcp_server.call_tool("delete_task", user_id, db, task_id=task_to_delete["task_id"])
                if delete_result.get("success"):
                    return f"✓ Done! I've deleted '{task_to_delete['title']}' from your list."
                else:
                    return "I had trouble deleting that task. Please try again."

            # No identifier provided - list tasks and ask
            task_list = []
            for idx, task in enumerate(tasks, 1):
                status = "✓" if task["completed"] else "○"
                task_list.append(f"{idx}. {status} {task['title']}")

            return f"Sure! Which task would you like me to delete?\n\n" + "\n".join(task_list) + "\n\nJust tell me the number or name of the task."

        elif action == "complete":
            # Check if task number or name was provided
            task_number = entities.get("task_number")
            task_name = entities.get("task_name")

            # Get user's tasks
            result = mcp_server.call_tool("list_tasks", user_id, db)
            if not result.get("success"):
                return "I couldn't retrieve your tasks right now. Please try again."

            tasks = result.get("tasks", [])
            incomplete_tasks = [t for t in tasks if not t["completed"]]

            if not incomplete_tasks:
                return "Great! You've completed all your tasks! 🎉"

            # Find the task to complete
            task_to_complete = None

            if task_number:
                # Complete by number (1-indexed, from incomplete tasks only)
                if 1 <= task_number <= len(incomplete_tasks):
                    task_to_complete = incomplete_tasks[task_number - 1]
                else:
                    return f"I couldn't find incomplete task number {task_number}. You have {len(incomplete_tasks)} incomplete task(s)."

            elif task_name:
                # Complete by name (fuzzy match)
                task_name_lower = task_name.lower()
                for task in incomplete_tasks:
                    if task_name_lower in task["title"].lower():
                        task_to_complete = task
                        break

                if not task_to_complete:
                    return f"I couldn't find an incomplete task matching '{task_name}'. Could you be more specific?"

            if task_to_complete:
                # Execute complete
                complete_result = mcp_server.call_tool("complete_task", user_id, db, task_id=task_to_complete["task_id"])
                if complete_result.get("success"):
                    return f"✓ Awesome! I've marked '{task_to_complete['title']}' as complete. Great work!"
                else:
                    return "I had trouble completing that task. Please try again."

            # No identifier provided - list incomplete tasks and ask
            task_list = []
            for idx, task in enumerate(incomplete_tasks, 1):
                task_list.append(f"{idx}. {task['title']}")

            return f"Which task did you complete?\n\n" + "\n".join(task_list) + "\n\nJust tell me the number or name."

        elif action == "update":
            # Check if task number or name was provided
            task_number = entities.get("task_number")
            task_name = entities.get("task_name")

            # Get user's tasks
            result = mcp_server.call_tool("list_tasks", user_id, db)
            if not result.get("success"):
                return "I couldn't retrieve your tasks right now. Please try again."

            tasks = result.get("tasks", [])
            if not tasks:
                return "You don't have any tasks to update."

            # Find the task to update
            task_to_update = None

            if task_number:
                # Update by number (1-indexed)
                if 1 <= task_number <= len(tasks):
                    task_to_update = tasks[task_number - 1]
                else:
                    return f"I couldn't find task number {task_number}. You have {len(tasks)} task(s)."

            elif task_name:
                # Update by name (fuzzy match)
                task_name_lower = task_name.lower()
                for task in tasks:
                    if task_name_lower in task["title"].lower():
                        task_to_update = task
                        break

                if not task_to_update:
                    return f"I couldn't find a task matching '{task_name}'. Could you be more specific?"

            if task_to_update:
                # For now, just acknowledge - full update requires new title/description
                return f"I found the task '{task_to_update['title']}'. What would you like to change about it? (Note: Full update functionality coming soon - for now, you can delete and recreate the task with new details)"

            # No identifier provided - list tasks and ask
            task_list = []
            for idx, task in enumerate(tasks, 1):
                status = "✓" if task["completed"] else "○"
                task_list.append(f"{idx}. {status} {task['title']}")

            return f"Which task would you like to update?\n\n" + "\n".join(task_list) + "\n\nTell me the number or name, and what you'd like to change."

        else:
            return "I'm here to help with your tasks! You can ask me to add tasks, show your list, mark tasks as complete, or delete tasks."

    def _format_tool_response(self, tool_calls: List[Dict[str, Any]]) -> str:
        """Format tool call results into a friendly response."""
        responses = []

        for call in tool_calls:
            tool = call["tool"]
            result = call["result"]

            if not result.get("success"):
                responses.append(f"❌ {result.get('error', 'Operation failed')}")
                continue

            if tool == "create_task":
                responses.append(f"✓ Created task: {result['title']}")
            elif tool == "list_tasks":
                count = result.get("count", 0)
                if count == 0:
                    responses.append("You don't have any tasks yet.")
                else:
                    tasks = result.get("tasks", [])
                    task_list = []
                    for task in tasks:
                        status = "✓" if task["completed"] else "○"
                        task_list.append(f"{status} {task['title']}")
                    responses.append(f"You have {count} task(s):\n" + "\n".join(task_list))
            elif tool == "complete_task":
                responses.append(f"✓ Completed task: {result['title']}")
            elif tool == "update_task":
                responses.append(f"✓ Updated task: {result['title']}")
            elif tool == "delete_task":
                responses.append(f"✓ Deleted task: {result['title']}")

        return "\n".join(responses) if responses else "Done!"


# Global stateless chatbot service instance
stateless_chatbot_service = StatelessChatbotService()
