"""GroqCloud provider integration using its OpenAI-compatible API."""

from typing import Any, Iterable
import logging

import httpx

from app.ai.policy import MEDIASSIST_SYSTEM_INSTRUCTION

logger = logging.getLogger(__name__)


class GroqServiceError(RuntimeError):
    """Safe application-level error for GroqCloud failures."""


class GroqService:
    """Generate responses through GroqCloud chat completions."""

    endpoint = "https://api.groq.com/openai/v1/chat/completions"

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
    def build_messages(messages: Iterable[dict[str, Any]]) -> list[dict[str, str]]:
        return [
            {
                "role": message["role"],
                "content": message["content"],
            }
            for message in messages
        ]

    def generate(self, messages: Iterable[dict[str, Any]]) -> str:
        if not self.api_key:
            raise GroqServiceError("Groq API key is not configured")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": MEDIASSIST_SYSTEM_INSTRUCTION},
                *self.build_messages(messages),
            ],
        }
        client = self._client or httpx.Client(timeout=self.timeout)
        should_close = self._client is None
        try:
            response = client.post(
                self.endpoint,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            if isinstance(exc, httpx.HTTPStatusError):
                logger.error("Groq request failed with HTTP %s: %s", exc.response.status_code, exc.response.text[:500])
            else:
                logger.error("Groq request failed: %s", exc)
            raise GroqServiceError("Groq request failed") from exc
        finally:
            if should_close:
                client.close()

        try:
            text = data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError, AttributeError) as exc:
            raise GroqServiceError("Groq returned an invalid response") from exc
        if not text:
            raise GroqServiceError("Groq returned an empty response")
        return text
