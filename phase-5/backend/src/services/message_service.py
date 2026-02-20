"""
MessageService for Phase III AI Chatbot.

Handles message persistence and retrieval.
"""
from typing import List
from uuid import UUID

from sqlmodel import Session, select

from ..models.message import Message, MessageRole


class MessageService:
    """Service for managing messages."""

    def __init__(self, session: Session):
        """
        Initialize MessageService.

        Args:
            session: Database session
        """
        self.session = session

    def save_message(
        self,
        conversation_id: UUID,
        role: MessageRole,
        content: str
    ) -> Message:
        """
        Save a message to the database.

        Args:
            conversation_id: Conversation ID
            role: Message role (user or assistant)
            content: Message content

        Returns:
            Message: Saved message
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_messages_by_conversation(self, conversation_id: UUID) -> List[Message]:
        """
        Get all messages for a conversation in chronological order.

        Args:
            conversation_id: Conversation ID

        Returns:
            List[Message]: Messages in chronological order
        """
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp)
        )
        return list(self.session.exec(statement).all())
