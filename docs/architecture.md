# Architecture

MediAssist AI follows a layered architecture so the healthcare domain behavior remains separate from transport and persistence details.

```text
Browser UI
   |
FastAPI routes and schemas (app/api)
   |
Business orchestration (app/services)
   |------------------|
SQLite repositories  AI provider service (app/ai)
   |                  |
SQLite database       GroqCloud chat completions API
```

## Responsibilities

- `app/static`: vanilla HTML, CSS, and JavaScript frontend.
- `app/api`: HTTP routes, request validation, dependency wiring, and safe errors.
- `app/services`: application workflows such as message exchange.
- `app/repositories`: SQLite persistence and conversation-history isolation.
- `app/ai`: provider integration and the MediAssist safety instruction.
- `app/config.py`: environment-backed runtime configuration.

The AI provider is isolated behind `GroqService`, so another provider can be introduced without changing the API or database layers. Conversation memory is owned by the application: the selected conversation's stored messages are loaded and sent to the provider for each exchange.
