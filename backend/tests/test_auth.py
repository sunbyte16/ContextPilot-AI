def test_register_and_login(client):
    reg_res = client.post("/api/v1/auth/register", json={
        "email": "alice@example.com",
        "password": "SecurePassword123!",
        "full_name": "Alice Developer"
    })
    assert reg_res.status_code == 200
    data = reg_res.json()
    assert data["email"] == "alice@example.com"
    assert "hashed_password" not in data
    assert "id" in data

    # Attempt duplicate registration
    dup_res = client.post("/api/v1/auth/register", json={
        "email": "alice@example.com",
        "password": "AnotherPassword!",
        "full_name": "Alice Duplicate"
    })
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"]

    # Login with correct password
    login_res = client.post("/api/v1/auth/login", json={
        "email": "alice@example.com",
        "password": "SecurePassword123!"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Login with wrong password
    bad_login = client.post("/api/v1/auth/login", json={
        "email": "alice@example.com",
        "password": "WrongPassword!"
    })
    assert bad_login.status_code == 401


def test_protected_routes(client, auth_headers):
    # Clear cookies to verify unauthenticated rejection
    client.cookies.clear()
    unauth = client.get("/api/v1/auth/me")
    assert unauth.status_code == 401

    # Authenticated access succeeds
    auth = client.get("/api/v1/auth/me", headers=auth_headers)
    assert auth.status_code == 200
    assert auth.json()["email"] == "test@contextpilot.ai"
