from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_list_activities():
    # Arrange: nothing to prepare
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Gym Class" in data


def test_signup_and_conflict():
    # Arrange
    act = "Basketball Team"
    email = "player1@school.edu"
    if email in activities[act]["participants"]:
        activities[act]["participants"].remove(email)

    # Act: first signup
    resp = client.post(f"/activities/{act}/signup", params={"email": email})
    # Assert success
    assert resp.status_code == 200
    assert email in activities[act]["participants"]

    # Act: second, duplicate signup
    resp2 = client.post(f"/activities/{act}/signup", params={"email": email})
    # Assert conflict
    assert resp2.status_code == 409


def test_remove_and_not_found():
    # Arrange
    act = "Chess Club"
    email = "removable@school.edu"
    if email not in activities[act]["participants"]:
        activities[act]["participants"].append(email)

    # Act: remove
    resp = client.delete(f"/activities/{act}/participants", params={"email": email})
    # Assert removed
    assert resp.status_code == 200
    assert email not in activities[act]["participants"]

    # Act: remove again
    resp2 = client.delete(f"/activities/{act}/participants", params={"email": email})
    # Assert not found
    assert resp2.status_code == 404


def test_activity_not_found():
    # Arrange: none
    # Act & Assert
    resp = client.post("/activities/NoSuch/signup", params={"email": "x@x"})
    assert resp.status_code == 404
    resp = client.delete("/activities/NoSuch/participants", params={"email": "x@x"})
    assert resp.status_code == 404
