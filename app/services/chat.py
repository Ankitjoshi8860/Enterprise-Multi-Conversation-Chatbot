"""Business logic for sending messages through the configured AI provider."""

from app.ai.groq import GroqService
from app.repositories.conversations import ConversationRepository
from app.repositories.messages import MessageRepository


class ConversationNotFoundError(LookupError):
    """Raised when a message targets a missing conversation."""


class ChatService:
    def __init__(
        self,
        conversations: ConversationRepository,
        messages: MessageRepository,
        ai: GroqService,
    ) -> None:
        self.conversations = conversations
        self.messages = messages
        self.ai = ai

    def send_message(self, conversation_id: int, content: str) -> dict:
        if self.conversations.get(conversation_id) is None:
            raise ConversationNotFoundError

        user_message = self.messages.create(conversation_id, "user", content)
        history = self.messages.list_for_conversation(conversation_id)
        assistant_content = self.ai.generate(history)
        assistant_message = self.messages.create(
            conversation_id, "assistant", assistant_content
        )
        return {"user_message": user_message, "assistant_message": assistant_message}
