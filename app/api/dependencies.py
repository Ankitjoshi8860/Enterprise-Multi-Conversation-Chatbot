"""Dependencies shared by API routes."""

from fastapi import Depends

from app.config import Settings, get_settings
from app.repositories.conversations import ConversationRepository
from app.repositories.messages import MessageRepository


def get_conversation_repository(
    settings: Settings = Depends(get_settings),
) -> ConversationRepository:
    return ConversationRepository(settings.database_path)


def get_message_repository(
    settings: Settings = Depends(get_settings),
) -> MessageRepository:
    return MessageRepository(settings.database_path)
