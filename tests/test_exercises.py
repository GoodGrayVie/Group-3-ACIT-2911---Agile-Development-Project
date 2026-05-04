def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 302


def test_login_get(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_login_post_success(client):
    response = client.post(
        "/login",
        data={"username": "Tom", "password": "pass1234"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]


def test_dashboard(client):
    response = client.get("/dashboard")
    assert response.status_code == 200


def test_log_workout(client):
    response = client.get("/log-workout")
    assert response.status_code == 302


def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302
