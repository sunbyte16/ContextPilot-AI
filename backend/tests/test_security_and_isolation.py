from app.tools.registry import tool_registry


def test_cross_user_tenant_isolation(client, auth_headers, second_user_headers):
    # User 1 creates a task
    t1_res = client.post("/api/v1/tasks/", json={
        "objective": "Confidential Project Alpha Execution",
        "priority": "HIGH"
    }, headers=auth_headers)
    t1_id = t1_res.json()["id"]

    # User 1 creates a memory
    m1_res = client.post("/api/v1/memory/", json={
        "category": "FACT",
        "title": "Confidential User1 Secret",
        "content": "Secret internal credential notes."
    }, headers=auth_headers)
    m1_id = m1_res.json()["id"]

    # User 2 lists tasks - User 1's task must NOT appear
    u2_tasks = client.get("/api/v1/tasks/", headers=second_user_headers).json()
    assert all(t["id"] != t1_id for t in u2_tasks)

    # User 2 tries to directly fetch User 1's task by ID - must return 404
    u2_get_t1 = client.get(f"/api/v1/tasks/{t1_id}", headers=second_user_headers)
    assert u2_get_t1.status_code == 404

    # User 2 lists memories - User 1's memory must NOT appear
    u2_mems = client.get("/api/v1/memory/", headers=second_user_headers).json()
    assert all(m["id"] != m1_id for m in u2_mems)

    # User 2 tries to delete User 1's memory - must return 404
    u2_del_m1 = client.delete(f"/api/v1/memory/{m1_id}", headers=second_user_headers)
    assert u2_del_m1.status_code == 404


def test_sensitive_payload_sanitization():
    raw_payload = {
        "account_id": "12345",
        "api_key": "AKIA_SECRET_AWS_KEY_123",
        "user_password": "PlaintextPassword!",
        "normal_field": "public_data"
    }
    sanitized = tool_registry._sanitize_payload(raw_payload)
    assert sanitized["api_key"] == "******[REDACTED]******"
    assert sanitized["user_password"] == "******[REDACTED]******"
    assert sanitized["normal_field"] == "public_data"
    assert sanitized["account_id"] == "12345"
