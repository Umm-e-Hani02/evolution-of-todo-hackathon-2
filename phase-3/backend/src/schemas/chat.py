"""Chat schemas for request/response models."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: Optional[int] = None
    message: str


class ToolCall(BaseModel):
    """Tool call information."""
    tool: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: List[ToolCall] = []


class ConversationMessage(BaseModel):
    """Message in a conversation."""
    id: int
    role: str
    content: str
    created_at: str


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history."""
    conversation_id: int
    messages: List[ConversationMessage]
