"""Chat API endpoint for stateless AI chatbot functionality."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.core.database import get_db
from src.models.user import User
from src.deps import get_current_user
from src.services.stateless_chatbot import stateless_chatbot_service
from src.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    ConversationMessage,
    ToolCall
)
from src.models.conversation import Conversation
from src.models.message import Message

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ChatResponse:
    """
    Stateless chat endpoint.

    Request:
        - conversation_id (optional): Resume existing conversation
        - message: User's message

    Response:
        - conversation_id: ID to use for next message
        - response: Assistant's response
        - tool_calls: List of tools executed

    STATELESS: Server holds no memory after response is returned.
    All state is stored in the database.
    """
    try:
        result = stateless_chatbot_service.handle_chat(
            user_id=current_user.id,
            message=request.message,
            conversation_id=request.conversation_id,
            db=db
        )

        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=[ToolCall(**tc) for tc in result["tool_calls"]]
        )

    except Exception as e:
        import traceback
        print(f"ERROR in chat endpoint: {type(e).__name__}: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}"
        )


@router.get("/conversations/{conversation_id}/messages", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ConversationHistoryResponse:
    """
    Get conversation history from database.

    Used by frontend to restore conversation after page refresh.
    """
    try:
        # Verify conversation belongs to user
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        conversation = db.exec(statement).first()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # Fetch messages
        message_statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        messages = db.exec(message_statement).all()

        return ConversationHistoryResponse(
            conversation_id=conversation_id,
            messages=[
                ConversationMessage(
                    id=msg.id,
                    role=msg.role,
                    content=msg.content,
                    created_at=msg.created_at.isoformat()
                )
                for msg in messages
            ]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching conversation: {str(e)}"
        )
