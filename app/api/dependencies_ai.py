"""AI service dependencies."""

from fastapi import Depends

from app.ai.gemini import GeminiService
from app.config import Settings, get_settings


def get_gemini_service(settings: Settings = Depends(get_settings)) -> GeminiService:
    return GeminiService(settings.gemini_api_key, settings.gemini_model)
