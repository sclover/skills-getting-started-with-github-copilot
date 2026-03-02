from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_cannot_register_twice():
    # Arrange: choose existing activity and participant
    act = "Chess Club"
    email = activities[act]["participants"][0]

    # Act: attempt to sign up again
    resp = client.post(f"/activities/{act}/signup", params={"email": email})

    # Assert: conflict error returned
    assert resp.status_code == 409
    assert "already signed up" in resp.json()["detail"]

def test_signup_new_student():
    # Arrange
    act = "Gym Class"
    email = "new@student.edu"
    if email in activities[act]["participants"]:
        activities[act]["participants"].remove(email)

    # Act
    resp = client.post(f"/activities/{act}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert resp.json()["message"].startswith("Signed up")
    assert email in activities[act]["participants"]

def test_unregister_student():
    # Arrange
    act = "Programming Class"
    email = "test@x.edu"
    if email not in activities[act]["participants"]:
        activities[act]["participants"].append(email)

    # Act
    resp = client.delete(f"/activities/{act}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in activities[act]["participants"]


def test_unregister_nonexistent():
    # Arrange
    act = "Soccer Club"
    email = "not@here.edu"
    if email in activities[act]["participants"]:
        activities[act]["participants"].remove(email)

    # Act
    resp = client.delete(f"/activities/{act}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404

