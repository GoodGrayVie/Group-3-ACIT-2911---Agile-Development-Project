def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 302


def test_dashboard(client):
    response = client.get("/dashboard")
    assert response.status_code == 200


def test_log_workout(client):
    response = client.get("workouts/add")
    assert response.status_code == 302


def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302


def test_custom_exercise():
    # check if user can add custom parenter they want to track
    # example: track shoulder rotation in cm
    pass
