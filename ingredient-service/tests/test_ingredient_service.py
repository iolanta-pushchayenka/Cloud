from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_ingredients():
    response = client.get("/ingredients")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    # проверка бизнес-логики поля available
    if len(data) > 0:
        item = data[0]
        assert "available" in item
        assert item["available"] >= 0
