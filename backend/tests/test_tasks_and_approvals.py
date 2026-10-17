def test_task_plan_and_human_approval_gate(client, auth_headers):
    # 1. Create a task that triggers an approval-gated step (e.g. data spend & export)
    create_res = client.post("/api/v1/tasks/", json={
        "objective": "Analyze quarterly cloud spend and export financial audit report",
        "priority": "HIGH"
    }, headers=auth_headers)
    assert create_res.status_code == 200
    task_data = create_res.json()
    task_id = task_data["id"]
    assert len(task_data["steps"]) >= 3
    assert task_data["status"] == "AWAITING_APPROVAL"
    assert len(task_data["approvals"]) >= 1

    approval_id = task_data["approvals"][0]["id"]
    assert task_data["approvals"][0]["status"] == "PENDING"

    # 2. Try executing before approval
    exec_res = client.post(f"/api/v1/tasks/{task_id}/execute", headers=auth_headers)
    assert exec_res.status_code == 200
    exec_data = exec_res.json()
    # It must halt execution when encountering the approval gate
    assert exec_data["status"] == "AWAITING_APPROVAL"

    # 3. Approve the consequential action
    approve_res = client.post(f"/api/v1/tasks/{task_id}/approvals/{approval_id}", json={
        "approved": True,
        "decision_notes": "Financial export authorized by workspace admin."
    }, headers=auth_headers)
    assert approve_res.status_code == 200
    appr_data = approve_res.json()
    assert appr_data["status"] == "COMPLETED"
    assert appr_data["progress"] == 100

    # 4. Verify task state in database
    detail_res = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert detail_res.status_code == 200
    final_task = detail_res.json()
    assert final_task["status"] == "COMPLETED"
    assert final_task["progress"] == 100
    assert "verified" in final_task["result_summary"].lower()


def test_task_approval_rejection_cancels_task(client, auth_headers):
    create_res = client.post("/api/v1/tasks/", json={
        "objective": "Analyze quarterly cloud spend and export financial report",
        "priority": "MEDIUM"
    }, headers=auth_headers)
    task_data = create_res.json()
    task_id = task_data["id"]
    approval_id = task_data["approvals"][0]["id"]

    # Reject the action
    reject_res = client.post(f"/api/v1/tasks/{task_id}/approvals/{approval_id}", json={
        "approved": False,
        "decision_notes": "Unapproved export format."
    }, headers=auth_headers)
    assert reject_res.status_code == 200
    assert reject_res.json()["status"] == "REJECTED"

    # Verify task is cancelled
    detail_res = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert detail_res.json()["status"] == "CANCELLED"
