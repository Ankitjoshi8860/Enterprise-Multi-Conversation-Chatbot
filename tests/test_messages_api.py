from fastapi.testclient import TestClient

from app.ai.groq import GroqServiceError
from app.config import get_settings
from app.main import app


class FakeGroq:
    def __init__(self, response="Educational response"):
        self.response = response
        self.histories = []

    def generate(self, messages):
        history = list(messages)
        self.histories.append(history)
        return self.response


def client(tmp_path, fake_groq):
    get_settings.cache_clear()
    get_settings().database_path = str(tmp_path / "messages.sqlite3")
    app.dependency_overrides.clear()
    from app.api.dependencies_ai import get_groq_service

    app.dependency_overrides[get_groq_service] = lambda: fake_groq
    return TestClient(app)


def test_send_message_persists_exchange_and_selected_history(tmp_path) -> None:
    fake = FakeGroq()
    api = client(tmp_path, fake)
    first = api.post("/conversations", json={"title": "Diabetes education"}).json()
    second = api.post("/conversations", json={"title": "Asthma education"}).json()

    response = api.post(
        f"/conversations/{first['id']}/messages", json={"content": "What is diabetes?"}
    )
    assert response.status_code == 201
    assert response.json()["assistant_message"]["content"] == "Educational response"
    assert [message["role"] for message in fake.histories[0]] == ["user"]

    response = api.post(
        f"/conversations/{first['id']}/messages", json={"content": "What foods help?"}
    )
    assert response.status_code == 201
    assert [message["role"] for message in fake.histories[1]] == [
        "user",
        "assistant",
        "user",
    ]
    assert api.get(f"/conversations/{second['id']}").json()["messages"] == []
    app.dependency_overrides.clear()


def test_send_message_validates_missing_and_empty_requests(tmp_path) -> None:
    fake = FakeGroq()
    api = client(tmp_path, fake)
    assert api.post("/conversations/999/messages", json={"content": "Hello"}).status_code == 404
    conversation = api.post("/conversations", json={"title": "Test"}).json()
    assert api.post(
        f"/conversations/{conversation['id']}/messages", json={"content": "   "}
    ).status_code == 422
    assert fake.histories == []
    app.dependency_overrides.clear()


def test_groq_failure_does_not_create_assistant_message(tmp_path) -> None:
    class FailingGroq:
        def generate(self, messages):
            raise GroqServiceError("provider unavailable")

    fake = FailingGroq()
    api = client(tmp_path, fake)
    conversation = api.post("/conversations", json={"title": "Test"}).json()
    response = api.post(
        f"/conversations/{conversation['id']}/messages", json={"content": "Hello"}
    )
    assert response.status_code == 502
    assert len(api.get(f"/conversations/{conversation['id']}").json()["messages"]) == 1
    app.dependency_overrides.clear()
