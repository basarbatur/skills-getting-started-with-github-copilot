import copy
import pytest

import src.app as app_module


def test_get_activities(client):
    # Arrange: client fixture provided
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data
    assert "Chess Club" in data
    sample = data["Tennis Club"]
    assert all(k in sample for k in ("description", "schedule", "max_participants", "participants"))


def test_signup_success(client):
    # Arrange
    activity = "Tennis Club"
    email = "tester@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in resp.json().get("message", "")
    assert email in app_module.activities[activity]["participants"]


def test_duplicate_signup(client):
    # Arrange
    activity = "Tennis Club"
    email = "duplicate@mergington.edu"
    # first signup
    r1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r1.status_code == 200

    # Act: attempt duplicate
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert r2.status_code == 400
    assert f"Student {email} is already signed up for {activity}" in r2.json().get("detail", "")


def test_activity_not_found(client):
    # Arrange
    activity = "NoSuch"
    email = "x@y.com"

    # Act
    r = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert r.status_code == 404
    assert r.json().get("detail") == "Activity not found"


def test_activity_full(client):
    # Arrange
    activity = "Tennis Club"
    # make it full
    max_p = app_module.activities[activity]["max_participants"]
    app_module.activities[activity]["participants"] = [f"u{i}@m.edu" for i in range(max_p)]
    email = "new@mergington.edu"

    # Act
    r = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert r.status_code == 400
    assert f"Activity {activity} is full" in r.json().get("detail", "")
