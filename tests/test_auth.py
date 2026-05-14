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


def test_no_login():
    # test that a user not logged in cannot create or add a workout
    # as they must be logged in first
    pass
