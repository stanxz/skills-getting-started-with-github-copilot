import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_unregister_flow():
    activity = "Basketball"
    email = "test_user@example.com"

    # Ensure a clean starting state for this test
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json().get("message", "")

    # Verify participant present
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]

    # Unregister
    resp3 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp3.status_code == 200
    assert f"Removed {email}" in resp3.json().get("message", "")

    # Verify participant removed
    resp4 = client.get("/activities")
    assert email not in resp4.json()[activity]["participants"]
