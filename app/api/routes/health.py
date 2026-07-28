"""Health and readiness endpoints."""

from fastapi import APIRouter

from app.config import get_settings

router = APIRouter(tags=["system"])


@router.get("/health", summary="Check API health")
def health_check() -> dict[str, str]:
    """Return a safe response suitable for local checks and probes."""

    settings = get_settings()
    return {"status": "ok", "environment": settings.app_env}
