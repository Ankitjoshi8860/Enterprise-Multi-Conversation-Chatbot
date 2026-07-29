# API reference

Start the server with `uvicorn app.main:app --reload`; interactive OpenAPI documentation is available at `/docs`.

## System

`GET /health` returns the application status and environment.

## Conversations

- `POST /conversations` with `{ "title": "Diabetes education" }` creates a conversation.
- `GET /conversations` lists conversations ordered by most recent update.
- `GET /conversations/{id}` returns the conversation and its messages.
- `PATCH /conversations/{id}` with `{ "title": "New title" }` renames a conversation.
- `DELETE /conversations/{id}` removes the conversation and its messages.

## Messages

`POST /conversations/{id}/messages` with `{ "content": "What is diabetes?" }`:

1. Validates the message.
2. Loads only the selected conversation.
3. Stores the user message.
4. Sends the complete selected history to Gemini.
5. Stores and returns the assistant response.

Missing conversations return `404`, invalid requests return `422`, and provider failures return `502` without exposing credentials.
