"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routes.health import router as health_router
from app.api.routes.conversations import router as conversations_router
from app.api.routes.messages import router as messages_router
from app.config import get_settings


def create_app() -> FastAPI:
    """Build and configure the application instance."""

    settings = get_settings()
    application = FastAPI(title=settings.app_name, version="0.1.0")
    application.include_router(health_router)
    application.include_router(conversations_router)
    application.include_router(messages_router)
    static_directory = Path(__file__).parent / "static"
    application.mount("/static", StaticFiles(directory=static_directory), name="static")

    @application.get("/", include_in_schema=False)
    def frontend() -> FileResponse:
        return FileResponse(static_directory / "index.html")

    return application


app = create_app()
