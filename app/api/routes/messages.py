"""Message exchange endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.ai.gemini import GeminiService, GeminiServiceError
from app.api.dependencies import get_conversation_repository, get_gemini_service
from app.api.dependencies import get_message_repository
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
    ai: GeminiService = Depends(get_gemini_service),
) -> dict:
    service = ChatService(conversations, messages, ai)
    try:
        return service.send_message(conversation_id, payload.content)
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Conversation not found") from exc
    except GeminiServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail="The AI service could not generate a response",
        ) from exc
