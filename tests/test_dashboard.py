import pytest
from db.models import db, Workout


def test_dashboard_shows_username(client):
    """Test that the dashboard displays the logged-in username."""
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "password123"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"testuser" in response.data


def test_dashboard_shows_workouts(client, app):
    """Test that workout entries appear on the dashboard after logging a workout."""
    with app.app_context():
        Workout.query.delete()
        db.session.commit()

    login_response = client.post(
        "/login",
        data={"username": "testuser", "password": "password123"},
        follow_redirects=True,
    )
    assert login_response.status_code == 200
    assert b"testuser" in login_response.data

    add_response = client.post(
        "/workouts/add",
        data={
            "name": "Morning Run",
            "date": "2026-05-08",
            "notes": "Nice run",
        },
        follow_redirects=True,
    )

    assert add_response.status_code == 200
    assert b"Morning Run" in add_response.data


def test_dashboard_no_username_when_not_logged_in(client):
    """Test that the dashboard does not show a username when not logged in."""
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"testuser" not in response.data
    assert b"Login" in response.data


def test_dashboard_no_workouts_when_empty(client, app):
    """Test that the dashboard shows an empty state when there are no workouts."""
    with app.app_context():
        Workout.query.delete()
        db.session.commit()

    login_response = client.post(
        "/login",
        data={"username": "testuser", "password": "password123"},
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"No workouts logged yet" in response.data
 