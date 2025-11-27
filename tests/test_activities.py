from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # expect at least one known activity from seed data
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "teststudent@example.com"

    # ensure email not already present
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    participants = data[activity]["participants"]
    if email in participants:
        # try to remove if present from previous run
        client.delete(f"/activities/{activity}/participants/{email}")

    # sign up
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    assert "Signed up" in signup.json().get("message", "")

    # verify participant present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email in participants

    # remove participant
    rem = client.delete(f"/activities/{activity}/participants/{email}")
    assert rem.status_code == 200
    assert "Removed" in rem.json().get("message", "")

    # verify removed
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email not in participants
