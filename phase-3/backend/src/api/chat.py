"""Chat API endpoint for Phase-3 AI Chatbot.

Handles conversational interactions with the AI agent.
"""
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from ..core.database import get_db
from ..models.conversation import Conversation
from ..models.message import Message, MessageRole
from ..services.openai_service import openai_service
from ..agent.runner import AgentRunner
from ..mcp.server import mcp_server # Import the global MCP server instance

router = APIRouter(prefix="/api", tags=["chat"])


# Request/Response models
class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., min_length=1, max_length=10000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID to continue (optional)")


class ChatResponse(BaseModel):
    """Chat response model."""
    conversation_id: str
    message: str


from ..deps import get_current_user
from ..models.user import User

# Initialize AgentRunner WITHOUT tools for free tier compatibility
agent_runner = AgentRunner(tools=[])  # Empty tools list for basic chat only


def detect_task_intent(message: str) -> bool:
    """
    Detect if the user message is trying to manage tasks.
    Returns True if task-related intent is detected.
    """
    message_lower = message.lower()

    # Task creation keywords
    create_keywords = [
        "create task", "add task", "make task", "new task",
        "create a task", "add a task", "make a task",
        "create todo", "add todo", "make todo", "new todo",
        "remind me to", "remember to", "need to do"
    ]

    # Task listing keywords
    list_keywords = [
        "show task", "list task", "show todo", "list todo",
        "my task", "my todo", "what task", "what todo",
        "see task", "see todo", "view task", "view todo",
        "what do i need", "what should i do"
    ]

    # Task update keywords
    update_keywords = [
        "update task", "edit task", "change task", "modify task",
        "update todo", "edit todo", "change todo", "modify todo"
    ]

    # Task completion keywords
    complete_keywords = [
        "complete task", "finish task", "done task", "mark task",
        "complete todo", "finish todo", "done todo", "mark todo",
        "mark as done", "mark as complete", "check off"
    ]

    # Task deletion keywords
    delete_keywords = [
        "delete task", "remove task", "delete todo", "remove todo",
        "get rid of", "clear task", "clear todo"
    ]

    # Check all keyword categories
    all_keywords = (
        create_keywords + list_keywords + update_keywords +
        complete_keywords + delete_keywords
    )

    for keyword in all_keywords:
        if keyword in message_lower:
            return True

    return False


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """
    Chat endpoint for conversational AI interactions.

    NOTE: This version uses a free model without tool calling support.
    The chatbot can have conversations but cannot create/manage tasks.
    Use the manual task form for task management.

    Args:
        request: Chat request with message and optional conversation_id
        session: Database session
        current_user: The authenticated user object

    Returns:
        ChatResponse with agent message and conversation_id

    Raises:
        HTTPException: 400 for validation errors, 404 for not found, 500 for server errors
    """
    # Tool executor not needed for basic chat
    def tool_executor(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Placeholder - tools not supported in free tier."""
        return {"success": False, "error": "Tool calling not available with free models"}

    try:
        user_id = current_user.id
        # Get or create conversation
        if request.conversation_id:
            # Continue existing conversation
            try:
                conversation_id_uuid = UUID(request.conversation_id)
                conversation_id = str(conversation_id_uuid)  # Convert to string immediately
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid conversation ID format"
                )

            # Verify conversation belongs to user
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or you don't have permission to access it"
                )
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id, title="New Conversation")
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            conversation_id = conversation.id  # Use the string ID directly

        # Load conversation history (last 10 messages)
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(10)  # Limit to last 10 messages for context
        )
        history = session.exec(statement).all()

        # Convert history to OpenAI format (using enum values)
        messages = [
            {"role": msg.role.value, "content": msg.content}  # Use the role value
            for msg in history
        ]

        # Add current user message
        messages.append({"role": "user", "content": request.message})

        # Save user message
        user_message = Message(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=request.message
        )
        session.add(user_message)
        session.commit()

        # Check if user is trying to manage tasks - respond immediately without LLM call
        if detect_task_intent(request.message):
            print(f"Task intent detected in message: {request.message[:50]}...")
            ai_response = (
                "I can help you think through and plan your tasks, but for accuracy and reliability, "
                "tasks are created and managed using the task form on the page."
            )
        else:
            # Get AI response using AgentRunner for non-task conversations
            try:
                print(f"Calling AgentRunner with {len(messages)} messages in history")
                result = agent_runner.run(messages, tool_executor)
                ai_response = result["message"]
                print(f"AgentRunner response received: {ai_response[:100] if ai_response else 'None'}...")
            except Exception as e:
                print(f"Error calling AgentRunner: {e}")
                print(f"Error type: {type(e).__name__}")
                # Return a friendly fallback message instead of showing the error
                ai_response = (
                    "I'm here to help! I can chat with you about productivity, time management, "
                    "and planning strategies. What would you like to talk about?"
                )

        # Save assistant message
        assistant_message = Message(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response
        )
        session.add(assistant_message)
        session.commit()

        # Update conversation timestamp
        conversation.updated_at = datetime.now()
        session.add(conversation)
        session.commit()

        # Return response
        return ChatResponse(
            conversation_id=conversation_id,
            message=ai_response
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )