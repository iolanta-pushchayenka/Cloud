from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# -------------------------------
# TEST: FEEDBACK LIST
# -------------------------------
def test_get_feedback():
    response = client.get("/feedback")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# -------------------------------
# TEST: FEEDBACK STATS (BUSINESS LOGIC)
# -------------------------------
def test_feedback_stats():
    response = client.get("/feedback/stats")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    # проверка структуры бизнес-агрегации
    if len(data) > 0:
        item = data[0]
        assert "subscription_id" in item
        assert "avg_rating" in item
        assert "total_reviews" in item