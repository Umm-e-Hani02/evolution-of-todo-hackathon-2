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
from ..agent.runner import AgentRunner
from ..mcp.server import mcp_server

router = APIRouter(prefix="/api", tags=["chat"])


# Request/Response models
class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., min_length=1, max_length=10000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID to continue (optional)")


class ToolCallResponse(BaseModel):
    """Tool call response model."""
    tool_name: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    success: bool


class ChatResponse(BaseModel):
    """Chat response model."""
    conversation_id: str
    message: str
    tool_calls: list[ToolCallResponse] = []


from ..deps import get_current_user
from ..models.user import User

# ... (other imports)

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """
    Chat endpoint for conversational AI interactions.

    Args:
        request: Chat request with message and optional conversation_id
        session: Database session
        current_user: The authenticated user object

    Returns:
        ChatResponse with agent message, conversation_id, and tool_calls

    Raises:
        HTTPException: 400 for validation errors, 404 for not found, 500 for server errors
    """
    try:
        user_id = current_user.id
        # Get or create conversation
        if request.conversation_id:
            # Continue existing conversation
            conversation_id = UUID(request.conversation_id)
            
            # Verify conversation belongs to user
            conversation = session.get(Conversation, str(conversation_id))
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
            conversation_id = UUID(conversation.id)

        # Load conversation history (last 50 messages)
        statement = (
            select(Message)
            .where(Message.conversation_id == str(conversation_id))
            .order_by(Message.created_at.asc())
            .limit(50)
        )
        history = session.exec(statement).all()

        # Convert history to OpenAI format
        messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in history
        ]

        # Add current user message
        messages.append({"role": "user", "content": request.message})

        # Save user message
        user_message = Message(
            conversation_id=str(conversation_id),
            role=MessageRole.USER,
            content=request.message
        )
        session.add(user_message)
        session.commit()

        # Initialize agent runner with MCP tools
        agent_runner = AgentRunner(tools=mcp_server.get_tool_definitions())

        # Create tool executor that logs tool calls
        tool_calls_log = []

        def tool_executor(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
            """Execute tool and return result."""
            # Execute tool via MCP server (user_id injected by backend)
            result = mcp_server.execute_tool(tool_name, arguments, session, user_id)

            # Add to response log
            tool_calls_log.append({
                "tool_name": tool_name,
                "input": arguments,
                "output": result,
                "success": result.get("success", False)
            })

            return result

        # Run agent
        agent_response = agent_runner.run(messages, tool_executor)

        # Save assistant message only if there's content
        if agent_response["message"]:
            assistant_message = Message(
                conversation_id=str(conversation_id),
                role=MessageRole.ASSISTANT,
                content=agent_response["message"]
            )
            session.add(assistant_message)
            session.commit()

        # Update conversation timestamp
        conversation.updated_at = datetime.now()
        session.add(conversation)
        session.commit()

        # Return response
        return ChatResponse(
            conversation_id=str(conversation_id),
            message=agent_response["message"],
            tool_calls=[
                ToolCallResponse(**call) for call in tool_calls_log
            ]
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