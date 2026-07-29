"""AI service dependencies."""

from fastapi import Depends

from app.ai.groq import GroqService
from app.config import Settings, get_settings


def get_groq_service(settings: Settings = Depends(get_settings)) -> GroqService:
    return GroqService(settings.groq_api_key, settings.groq_model)
