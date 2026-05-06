from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


# -------------------------------
# MOCK: Ingredient Service
# -------------------------------
def mock_ingredients(*args, **kwargs):
    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {"id": 1, "name": "Tomato"},
        {"id": 2, "name": "Cheese"}
    ]
    return mock_resp


# -------------------------------
# TEST: CREATE SUBSCRIPTION
# -------------------------------
@patch("app.main.requests.get", side_effect=mock_ingredients)
@patch("app.main.send_message")
def test_create_subscription(mock_send, mock_get):
    payload = {
        "user_id": 1,
        "plan_type": "monthly"
    }

    response = client.post("/subscriptions", json=payload)

    assert response.status_code == 200
    data = response.json()

    # бизнес-логика проверки
    assert data["status"] == "created"
    assert "subscription_id" in data

    # проверка вызовов
    mock_get.assert_called_once()
    mock_send.assert_called_once()


# -------------------------------
# TEST: GET SUBSCRIPTIONS
# -------------------------------
def test_get_subscriptions():
    response = client.get("/subscriptions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
