from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app


def client(tmp_path):
    get_settings.cache_clear()
    get_settings().database_path = str(tmp_path / "api.sqlite3")
    return TestClient(app)


def test_conversation_crud_and_history(tmp_path) -> None:
    api = client(tmp_path)
    created = api.post("/conversations", json={"title": "First chat"})
    assert created.status_code == 201
    conversation_id = created.json()["id"]

    listed = api.get("/conversations")
    assert listed.status_code == 200
    assert listed.json()[0]["title"] == "First chat"

    detail = api.get(f"/conversations/{conversation_id}")
    assert detail.status_code == 200
    assert detail.json()["messages"] == []

    renamed = api.patch(
        f"/conversations/{conversation_id}", json={"title": "Renamed chat"}
    )
    assert renamed.status_code == 200
    assert renamed.json()["title"] == "Renamed chat"

    deleted = api.delete(f"/conversations/{conversation_id}")
    assert deleted.status_code == 204
    assert api.get(f"/conversations/{conversation_id}").status_code == 404


def test_conversation_validation_and_missing_ids(tmp_path) -> None:
    api = client(tmp_path)
    assert api.post("/conversations", json={"title": "   "}).status_code == 422
    assert api.patch("/conversations/999", json={"title": "Missing"}).status_code == 404
    assert api.get("/conversations/999").status_code == 404
    assert api.delete("/conversations/999").status_code == 404
