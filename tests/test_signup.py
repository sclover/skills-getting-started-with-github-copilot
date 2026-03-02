from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_cannot_register_twice():
    # pick an existing activity and participant
    act = "Chess Club"
    email = activities[act]["participants"][0]

    # first signup should be allowed (it’s already there, but our in‑memory
    # data starts populated).
    resp = client.post(f"/activities/{act}/signup", params={"email": email})
    assert resp.status_code == 409
    assert "already signed up" in resp.json()["detail"]

def test_signup_new_student():
    act = "Gym Class"
    email = "new@student.edu"
    # ensure clean state
    if email in activities[act]["participants"]:
        activities[act]["participants"].remove(email)

    resp = client.post(f"/activities/{act}/signup", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"].startswith("Signed up")
    assert email in activities[act]["participants"]