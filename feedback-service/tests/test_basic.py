from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_feedback():
    response = client.get("/feedback")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_feedback_stats():
    response = client.get("/feedback/stats")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
