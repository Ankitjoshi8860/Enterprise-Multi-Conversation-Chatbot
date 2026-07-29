import httpx
import pytest

from app.ai.groq import GroqService, GroqServiceError


def test_build_messages_preserves_conversation_roles() -> None:
    assert GroqService.build_messages(
        [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
    ) == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
    ]


def test_generate_sends_safety_policy_and_normalizes_response() -> None:
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "Hello back"}}]},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    service = GroqService("test-key", "llama-3.3-70b-versatile", client=client)
    assert service.generate([{"role": "user", "content": "Hello"}]) == "Hello back"
    assert requests[0].headers["authorization"] == "Bearer test-key"
    body = requests[0].json()
    assert body["model"] == "llama-3.3-70b-versatile"
    assert body["messages"][1] == {"role": "user", "content": "Hello"}
    assert "Never diagnose conditions" in body["messages"][0]["content"]
    client.close()


def test_missing_key_and_provider_failure_are_safe_errors() -> None:
    with pytest.raises(GroqServiceError, match="not configured"):
        GroqService(None, "llama-3.3-70b-versatile").generate([])

    client = httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(429)))
    with pytest.raises(GroqServiceError, match="request failed"):
        GroqService("test-key", "llama-3.3-70b-versatile", client=client).generate([])
    client.close()
