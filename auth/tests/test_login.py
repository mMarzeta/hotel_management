def test_login_successful(client, mock_get_user, mock_verify_password, login_payload):
    response = client.post(
        "/login",
        data=login_payload)

    assert response.status_code == 200

    response = response.json()
    assert set(response) == {"access_token", "token_type"}
    assert response['token_type'] == "bearer"


def test_login_failed_no_user(client, login_payload):
    response = client.post(
        "/login",
        data=login_payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login_failed_wrong_password(client, mock_get_user, login_payload):
    response = client.post(
        "/login",
        data=login_payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

