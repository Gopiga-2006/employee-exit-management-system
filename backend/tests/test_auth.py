def test_register_and_login(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Test Employee", "email": "employee@example.com", "password": "Secret1"},
    )
    assert response.status_code == 201
    assert response.json()["data"]["role"] == "employee"

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "employee@example.com", "password": "Secret1"},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["access_token"]
