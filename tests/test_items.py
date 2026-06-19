from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_stories() -> None:
    response = client.get("/userstories")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_story() -> None:
    response = client.post(
        "/userstories",
        json={
            "title": "Neu",
            "description": "Test",
            "source": "csv",
            "status": "Nicht begonnen",
            "priority": "Mittel",
            "tags": ["demo"],
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Neu"
