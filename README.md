# Enterprise Multi-Conversation Chatbot

Layered FastAPI foundation for MediAssist AI, the healthcare education chatbot described in `prd.md` and `domain.md`.

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

Gemini uses the REST `generateContent` endpoint. Configure `GEMINI_API_KEY` and `GEMINI_MODEL` in `.env`; the key is sent in a request header and is never returned by the API.

MediAssist AI provides educational healthcare information only. It must not diagnose conditions, prescribe medicines, recommend dosage changes, or replace professional care. Possible emergency symptoms are directed to immediate emergency medical assistance.

SQLite is stored at the path configured by `DATABASE_PATH` and is initialized automatically when the persistence layer is used. Local database files are ignored by Git.

## Run the API

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. OpenAPI documentation is available at `/docs`, and the health check is available at `/health`.

Conversation management endpoints are available under `/conversations`: `POST` and `GET` for create/list, `GET /conversations/{id}` for history, `PATCH /conversations/{id}` for rename, and `DELETE /conversations/{id}` for removal. Send a message with `POST /conversations/{id}/messages` and a JSON body such as `{ "content": "What is diabetes?" }`.

## Test

```powershell
pytest
```

## Architecture

- `app/api`: HTTP routes and request/response concerns
- `app/services`: application and business logic
- `app/repositories`: database persistence abstractions
- `app/database.py`: SQLite connection and schema initialization
- `app/ai`: AI provider integrations
- `app/config.py`: environment-backed settings
- `app/main.py`: application composition and entry point
