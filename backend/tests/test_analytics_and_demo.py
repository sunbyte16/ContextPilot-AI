def test_demo_seed_and_analytics_summary(client, auth_headers):
    # 1. Seed demo data
    seed_res = client.post("/api/v1/demo/seed", headers=auth_headers)
    assert seed_res.status_code == 200
    seed_data = seed_res.json()
    assert seed_data["success"] is True
    assert seed_data["seeded"]["tasks"] == 2

    # 2. Check analytics summary
    analytics_res = client.get("/api/v1/analytics/summary", headers=auth_headers)
    assert analytics_res.status_code == 200
    summary = analytics_res.json()
    assert summary["total_tasks"] >= 2
    assert summary["completed_tasks"] >= 1
    assert summary["pending_approvals"] >= 1
    assert len(summary["status_distribution"]) >= 1
    assert len(summary["recent_trend"]) == 7

    # 3. Check activity & notifications
    notif_res = client.get("/api/v1/activity/notifications", headers=auth_headers)
    assert notif_res.status_code == 200
    assert len(notif_res.json()) >= 1

    # Mark notifications read
    read_all = client.post("/api/v1/activity/notifications/read-all", headers=auth_headers)
    assert read_all.status_code == 200

    # 4. Check settings integrations
    integ_res = client.get("/api/v1/settings/integrations", headers=auth_headers)
    assert integ_res.status_code == 200
    integs = integ_res.json()["integrations"]
    assert any(i["provider"] == "local-demo" for i in integs)
    assert any(i["provider"] == "bedrock" for i in integs)
    assert any(i["provider"] == "simulated-alexa-web" for i in integs)

    # 5. Reset demo data
    reset_res = client.post("/api/v1/demo/reset", headers=auth_headers)
    assert reset_res.status_code == 200
    assert reset_res.json()["success"] is True

    # Confirm tasks empty after reset
    tasks_after = client.get("/api/v1/tasks/", headers=auth_headers).json()
    assert len(tasks_after) == 0
