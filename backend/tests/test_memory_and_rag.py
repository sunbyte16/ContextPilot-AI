import io


def test_memory_crud_flow(client, auth_headers):
    # 1. Create memory
    create_res = client.post("/api/v1/memory/", json={
        "category": "FACT",
        "title": "Machine Learning Exam Date",
        "content": "Scheduled for December 15, 2026.",
        "is_pinned": True
    }, headers=auth_headers)
    assert create_res.status_code == 200
    mem_id = create_res.json()["id"]
    assert create_res.json()["is_pinned"] is True

    # 2. List memories
    list_res = client.get("/api/v1/memory/", headers=auth_headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # Filter by category
    fact_res = client.get("/api/v1/memory/?category=FACT", headers=auth_headers)
    assert len(fact_res.json()) == 1

    note_res = client.get("/api/v1/memory/?category=NOTE", headers=auth_headers)
    assert len(note_res.json()) == 0

    # 3. Update memory
    upd_res = client.put(f"/api/v1/memory/{mem_id}", json={
        "content": "Rescheduled for December 18, 2026."
    }, headers=auth_headers)
    assert upd_res.status_code == 200
    assert "December 18" in upd_res.json()["content"]

    # 4. Delete memory
    del_res = client.delete(f"/api/v1/memory/{mem_id}", headers=auth_headers)
    assert del_res.status_code == 200

    # Confirm empty
    empty_res = client.get("/api/v1/memory/", headers=auth_headers)
    assert len(empty_res.json()) == 0


def test_knowledge_upload_and_grounded_rag(client, auth_headers):
    sample_text = (
        "ContextPilot AI Architecture Overview.\n"
        "Section 1: The Agent Orchestrator manages planning and approval state machines.\n"
        "Section 2: Amazon Bedrock powers natural language task planning with strict parameter validation.\n"
        "Section 3: The system maintains 100% tenant isolation across database entities."
    )
    file_payload = {"file": ("architecture_guide.txt", io.BytesIO(sample_text.encode("utf-8")), "text/plain")}

    # 1. Upload document
    upload_res = client.post("/api/v1/knowledge/upload", files=file_payload, headers=auth_headers)
    assert upload_res.status_code == 200
    doc_data = upload_res.json()
    assert doc_data["processing_status"] == "INDEXED"
    assert doc_data["chunk_count"] >= 1
    doc_id = doc_data["id"]

    # 2. Grounded question answering with citations
    query_res = client.post("/api/v1/knowledge/grounded-query", json={
        "question": "What does the Agent Orchestrator manage?",
        "top_k": 2
    }, headers=auth_headers)
    assert query_res.status_code == 200
    q_data = query_res.json()
    assert q_data["has_sufficient_evidence"] is True
    assert len(q_data["citations"]) > 0
    assert "architecture_guide.txt" in q_data["citations"][0]["filename"]

    # 3. Grounded query on completely irrelevant topic
    irrelevant_res = client.post("/api/v1/knowledge/grounded-query", json={
        "question": "What is the speed of light in vacuum?",
        "top_k": 2
    }, headers=auth_headers)
    assert irrelevant_res.status_code == 200
    irrel_data = irrelevant_res.json()
    assert irrel_data["has_sufficient_evidence"] is False
    assert len(irrel_data["citations"]) == 0
    assert "no relevant passages" in irrel_data["answer"].lower()

    # 4. Delete document
    del_res = client.delete(f"/api/v1/knowledge/{doc_id}", headers=auth_headers)
    assert del_res.status_code == 200
