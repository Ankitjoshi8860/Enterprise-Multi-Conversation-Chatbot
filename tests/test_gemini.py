import httpx
import pytest

from app.ai.gemini import GeminiService, GeminiServiceError


def test_build_contents_maps_application_roles() -> None:
    contents = GeminiService.build_contents(
        [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
    )

    assert contents == [
        {"role": "user", "parts": [{"text": "Hello"}]},
        {"role": "model", "parts": [{"text": "Hi"}]},
    ]


def test_generate_sends_history_and_normalizes_response() -> None:
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={"candidates": [{"content": {"parts": [{"text": "Hello back"}]}}]},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    service = GeminiService("test-key", "gemini-test", client=client)
    assert service.generate([{"role": "user", "content": "Hello"}]) == "Hello back"
    assert requests[0].headers["x-goog-api-key"] == "test-key"
    assert requests[0].json()["contents"][0]["parts"][0]["text"] == "Hello"
    assert "Never diagnose conditions" in requests[0].json()["systemInstruction"]["parts"][0]["text"]
    client.close()


def test_missing_key_and_provider_failure_are_safe_errors() -> None:
    with pytest.raises(GeminiServiceError, match="not configured"):
        GeminiService(None, "gemini-test").generate([])

    client = httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(503)))
    with pytest.raises(GeminiServiceError, match="request failed"):
        GeminiService("test-key", "gemini-test", client=client).generate([])
    client.close()
