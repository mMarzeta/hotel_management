def test_register_user_success(client, register_payload, mock_register_user, fixed_uuid):
    response = client.post(
        "/register",
        json=register_payload)

    assert {"id": fixed_uuid,
            "email": register_payload["email"],
            "username": register_payload["username"]} == response.json()
    assert response.status_code == 200


# def test_register_conflict(client, register_payload, mock_register_user)
