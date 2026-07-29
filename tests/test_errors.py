from fastapi.testclient import TestClient

from app.main import app


def test_validation_errors_are_safe_and_meaningful() -> None:
    response = TestClient(app).post("/conversations", json={"title": "   "})

    assert response.status_code == 422
    assert response.json()["detail"] == "Request validation failed"
    assert "GROQ_API_KEY" not in response.text
