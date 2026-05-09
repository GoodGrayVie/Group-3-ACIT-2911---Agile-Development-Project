import pytest
from app import workout_store


def test_dashboard_shows_username(client):
    """Test that the dashboard displays the logged-in username."""
    # Simulate login
    client.post("/login", data={"username": "testuser", "password": "password123"})

    # Access the dashboard
    response = client.get("/dashboard")

    # Check that the username appears in the response
    assert response.status_code == 200
    assert b"testuser" in response.data


def test_dashboard_shows_workouts(client):
    """Test that the dashboard displays the user's workout history."""
    # Clear any existing workouts for this user
    workout_store["testuser"] = []

    # Simulate login
    client.post("/login", data={"username": "testuser", "password": "password123"})

    # Log a workout
    client.post("/log-workout", data={
        "date": "2023-10-01",
        "type": "Running",
        "length": "45",
        "calories": "300"
    })

    # Access the dashboard
    response = client.get("/dashboard")

    # Check that the workout appears in the response
    assert response.status_code == 200
    assert b"Running" in response.data
    assert b"45" in response.data
    assert b"300" in response.data


def test_dashboard_no_username_when_not_logged_in(client):
    """Test that the dashboard does not show a username when not logged in."""
    # Access the dashboard without logging in
    response = client.get("/dashboard")

    # Check that no username is displayed (should show login link instead)
    assert response.status_code == 200
    assert b"testuser" not in response.data
    assert b"Login" in response.data


def test_dashboard_no_workouts_when_empty(client):
    """Test that the dashboard shows empty state when no workouts exist."""
    # Simulate login
    client.post("/login", data={"username": "testuser", "password": "password123"})

    # Clear workouts
    workout_store["testuser"] = []

    # Access the dashboard
    response = client.get("/dashboard")

    # Check for empty state message
    assert response.status_code == 200
    assert b"No workouts logged yet." in response.data</content>
    assert b"No workouts logged yet." in response.data
