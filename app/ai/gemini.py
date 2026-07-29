"""Google Gemini provider integration."""

from typing import Any, Iterable

import httpx

from app.ai.policy import MEDIASSIST_SYSTEM_INSTRUCTION


class GeminiServiceError(RuntimeError):
    """Safe application-level error for Gemini failures."""


class GeminiService:
    """Generate responses through Gemini's generateContent REST endpoint."""

    def __init__(
        self,
        api_key: str | None,
        model: str,
        client: httpx.Client | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self._client = client
        self.timeout = timeout

    @staticmethod
    def build_contents(messages: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
        """Translate stored application messages into Gemini content objects."""

        return [
            {
                "role": "model" if message["role"] == "assistant" else "user",
                "parts": [{"text": message["content"]}],
            }
            for message in messages
        ]

    def generate(self, messages: Iterable[dict[str, Any]]) -> str:
        """Send conversation history and return the first text candidate."""

        if not self.api_key:
            raise GeminiServiceError("Gemini API key is not configured")

        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/{self.model}:generateContent"
        )
        payload = {
            "systemInstruction": {"parts": [{"text": MEDIASSIST_SYSTEM_INSTRUCTION}]},
            "contents": self.build_contents(messages),
        }
        client = self._client or httpx.Client(timeout=self.timeout)
        should_close = self._client is None
        try:
            response = client.post(
                endpoint,
                headers={"x-goog-api-key": self.api_key},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise GeminiServiceError("Gemini request failed") from exc
        finally:
            if should_close:
                client.close()

        try:
            parts = data["candidates"][0]["content"]["parts"]
            text = "".join(part["text"] for part in parts if "text" in part).strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise GeminiServiceError("Gemini returned an invalid response") from exc
        if not text:
            raise GeminiServiceError("Gemini returned an empty response")
        return text
