# Enterprise Multi-Conversation Chatbot

Layered FastAPI foundation for the enterprise multi-conversation chatbot described in `prd.md`.

## Local setup

Python 3.11 or newer is required.

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

The Gemini API key is intentionally blank in `.env.example`. Add credentials only to the untracked `.env` file when AI integration is implemented.

## Run the API

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. OpenAPI documentation is available at `/docs`, and the health check is available at `/health`.

## Test

```powershell
pytest
```

## Architecture

- `app/api`: HTTP routes and request/response concerns
- `app/services`: application and business logic
- `app/repositories`: database persistence abstractions
- `app/ai`: AI provider integrations
- `app/config.py`: environment-backed settings
- `app/main.py`: application composition and entry point
