"""Message exchange endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.ai.groq import GroqService, GroqServiceError
from app.api.dependencies import get_conversation_repository
from app.api.dependencies import get_message_repository
from app.api.dependencies_ai import get_groq_service
from app.api.schemas import ChatResponse, MessageCreate
from app.repositories.conversations import ConversationRepository
from app.repositories.messages import MessageRepository
from app.services.chat import ChatService, ConversationNotFoundError

router = APIRouter(prefix="/conversations", tags=["messages"])


@router.post(
    "/{conversation_id}/messages",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    conversation_id: int,
    payload: MessageCreate,
    conversations: ConversationRepository = Depends(get_conversation_repository),
    messages: MessageRepository = Depends(get_message_repository),
    ai: GroqService = Depends(get_groq_service),
) -> dict:
    service = ChatService(conversations, messages, ai)
    try:
        return service.send_message(conversation_id, payload.content)
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Conversation not found") from exc
    except GroqServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail="The AI service could not generate a response",
        ) from exc
