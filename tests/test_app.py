
import app as app_module


def test_home_page():
    client = app_module.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"TouchGrass AI" in response.data


def test_invalid_minutes_rejected():
    client = app_module.app.test_client()
    response = client.post(
        "/api/mission",
        json={
            "minutes": 10,
            "interest": "nature",
            "difficulty": "beginner",
        },
    )
    assert response.status_code == 400


def test_invalid_interest_rejected():
    client = app_module.app.test_client()
    response = client.post(
        "/api/mission",
        json={
            "minutes": 15,
            "interest": "unknown",
            "difficulty": "beginner",
        },
    )
    assert response.status_code == 400


def test_invalid_difficulty_rejected():
    client = app_module.app.test_client()
    response = client.post(
        "/api/mission",
        json={
            "minutes": 15,
            "interest": "nature",
            "difficulty": "expert",
        },
    )
    assert response.status_code == 400





import json
import urllib.error
from unittest.mock import patch


def test_mission_success_with_mocked_ollama():
    client = app_module.app.test_client()

    fake_response = {
        "message": {
            "content": "Mission: Take a safe 15-minute nature walk."
        }
    }

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps(fake_response).encode("utf-8")

    with patch.object(
        app_module.urllib.request,
        "urlopen",
        return_value=FakeResponse(),
    ):
        response = client.post(
            "/api/mission",
            json={
                "minutes": 15,
                "interest": "nature",
                "difficulty": "beginner",
            },
        )

    assert response.status_code == 200
    assert "nature walk" in response.get_json()["mission"]


def test_mission_handles_ollama_unavailable():
    client = app_module.app.test_client()

    with patch.object(
        app_module.urllib.request,
        "urlopen",
        side_effect=urllib.error.URLError("Ollama unavailable"),
    ):
        response = client.post(
            "/api/mission",
            json={
                "minutes": 15,
                "interest": "nature",
                "difficulty": "beginner",
            },
        )

    assert response.status_code == 503
    assert "error" in response.get_json()
