from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_list_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # verify a few known keys
    assert "Chess Club" in data
    assert "Gym Class" in data


def test_signup_and_conflict():
    act = "Basketball Team"
    email = "player1@school.edu"

    # ensure clean state
    if email in activities[act]["participants"]:
        activities[act]["participants"].remove(email)

    resp = client.post(f"/activities/{act}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[act]["participants"]

    # duplicate attempt should yield 409
    resp2 = client.post(f"/activities/{act}/signup", params={"email": email})
    assert resp2.status_code == 409


def test_remove_and_not_found():
    act = "Chess Club"
    email = "removable@school.edu"

    # add if missing
    if email not in activities[act]["participants"]:
        activities[act]["participants"].append(email)

    resp = client.delete(f"/activities/{act}/participants", params={"email": email})
    assert resp.status_code == 200
    assert email not in activities[act]["participants"]

    # deleting again should 404
    resp2 = client.delete(f"/activities/{act}/participants", params={"email": email})
    assert resp2.status_code == 404


def test_activity_not_found():
    resp = client.post("/activities/NoSuch/signup", params={"email": "x@x"})
    assert resp.status_code == 404
    resp = client.delete("/activities/NoSuch/participants", params={"email": "x@x"})
    assert resp.status_code == 404
