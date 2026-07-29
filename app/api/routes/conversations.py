"""Conversation management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_conversation_repository, get_message_repository
from app.api.schemas import (
    ConversationCreate,
    ConversationRename,
    ConversationResponse,
    ConversationWithMessages,
    MessageResponse,
)
from app.repositories.conversations import ConversationRepository
from app.repositories.messages import MessageRepository

router = APIRouter(prefix="/conversations", tags=["conversations"])


def not_found() -> HTTPException:
    return HTTPException(status_code=404, detail="Conversation not found")


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(
    payload: ConversationCreate,
    repository: ConversationRepository = Depends(get_conversation_repository),
) -> dict:
    return repository.create(payload.title.strip())


@router.get("", response_model=list[ConversationResponse])
def list_conversations(
    repository: ConversationRepository = Depends(get_conversation_repository),
) -> list[dict]:
    return repository.list()


@router.get("/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(
    conversation_id: int,
    repository: ConversationRepository = Depends(get_conversation_repository),
    messages: MessageRepository = Depends(get_message_repository),
) -> dict:
    conversation = repository.get(conversation_id)
    if conversation is None:
        raise not_found()
    return {**conversation, "messages": messages.list_for_conversation(conversation_id)}


@router.patch("/{conversation_id}", response_model=ConversationResponse)
def rename_conversation(
    conversation_id: int,
    payload: ConversationRename,
    repository: ConversationRepository = Depends(get_conversation_repository),
) -> dict:
    conversation = repository.rename(conversation_id, payload.title.strip())
    if conversation is None:
        raise not_found()
    return conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    repository: ConversationRepository = Depends(get_conversation_repository),
) -> Response:
    if not repository.delete(conversation_id):
        raise not_found()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
