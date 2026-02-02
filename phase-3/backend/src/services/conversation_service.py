"""
ConversationService for Phase III AI Chatbot.

Handles conversation CRUD operations and conversation history loading.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from sqlmodel import Session, select, desc

from ..models.conversation import Conversation
from ..models.message import Message, MessageRole


class ConversationService:
    """Service for managing conversations."""

    def __init__(self, session: Session):
        """
        Initialize ConversationService.

        Args:
            session: Database session
        """
        self.session = session

    def create_conversation(self, user_id: str) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: User ID who owns the conversation (string format from Phase II)

        Returns:
            Conversation: Created conversation
        """
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: UUID, user_id: str) -> Optional[Conversation]:
        """
        Get a conversation by ID, ensuring it belongs to the user.

        Args:
            conversation_id: Conversation ID
            user_id: User ID for authorization check (string format from Phase II)

        Returns:
            Optional[Conversation]: Conversation if found and authorized, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
            Conversation.deleted_at.is_(None)
        )
        return self.session.exec(statement).first()

    def load_conversation_history(
        self,
        conversation_id: UUID,
        limit: int = 50
    ) -> List[Message]:
        """
        Load conversation history (last N messages in chronological order).

        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages to load (default: 50)

        Returns:
            List[Message]: Messages in chronological order (oldest first)
        """
        # Load last N messages in reverse chronological order
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(desc(Message.timestamp))
            .limit(limit)
        )
        messages = self.session.exec(statement).all()

        # Reverse to chronological order (oldest first)
        return list(reversed(messages))

    def update_conversation_timestamp(self, conversation_id: UUID) -> None:
        """
        Update conversation's updated_at timestamp.

        Args:
            conversation_id: Conversation ID
        """
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = self.session.exec(statement).first()
        if conversation:
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()
