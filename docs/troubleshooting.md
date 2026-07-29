# Troubleshooting

## `pytest` is not recognized

Create and activate the virtual environment, then install development dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Gemini requests fail

Confirm that `.env` exists and contains `GEMINI_API_KEY`. The key must not be placed in source files. Also verify `GEMINI_MODEL` names a model available to the configured API key.

## Database problems

Delete the local `chatbot.db` only when resetting development data, then restart the application. The schema is recreated automatically. Production data should be backed up before any reset.

## UI shows an error toast

Inspect the API response and server logs. The browser intentionally receives a safe error message; detailed exception information stays in server logs.
