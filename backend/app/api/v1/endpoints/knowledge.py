import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.all_models import User, KnowledgeDocument, DocumentChunk, AuditEvent
from app.schemas.knowledge import (
    KnowledgeDocumentResponse, GroundedQueryRequest,
    GroundedQueryResponse, SourceCitation
)
from app.security.deps import get_current_user
from app.core.config import settings
from app.knowledge.document_processor import process_document
from app.tools.registry import tool_registry

router = APIRouter()


@router.get("/", response_model=List[KnowledgeDocumentResponse])
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(KnowledgeDocument).filter(
        KnowledgeDocument.user_id == current_user.id
    ).order_by(KnowledgeDocument.created_at.desc()).all()


@router.post("/upload", response_model=KnowledgeDocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    filename = file.filename or "uploaded_doc.txt"
    ext = os.path.splitext(filename)[1].lower()
    allowed_exts = [".pdf", ".txt", ".md", ".json", ".csv"]

    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Supported formats: {', '.join(allowed_exts)}"
        )

    file_bytes = await file.read()
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum size limit of {settings.MAX_UPLOAD_SIZE_BYTES // (1024*1024)}MB."
        )

    # Save to disk
    user_upload_dir = os.path.join(settings.UPLOAD_DIR, current_user.id)
    os.makedirs(user_upload_dir, exist_ok=True)
    save_path = os.path.join(user_upload_dir, filename)

    with open(save_path, "wb") as f:
        f.write(file_bytes)

    # Create document record
    doc = KnowledgeDocument(
        user_id=current_user.id,
        filename=filename,
        file_type=ext.lstrip("."),
        file_size_bytes=len(file_bytes),
        storage_path=save_path,
        processing_status="PENDING",
        chunk_count=0
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Process and index
    try:
        doc = process_document(
            doc_id=doc.id,
            file_bytes=file_bytes,
            filename=filename,
            user=current_user,
            db=db
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

    return doc


@router.get("/{document_id}")
def get_document_details(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(KnowledgeDocument).filter(
        KnowledgeDocument.id == document_id,
        KnowledgeDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    chunks = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == doc.id
    ).order_by(DocumentChunk.chunk_index.asc()).all()

    return {
        "document": doc,
        "chunks_count": len(chunks),
        "chunks": [
            {
                "id": c.id,
                "chunk_index": c.chunk_index,
                "page_number": c.page_number,
                "content": c.content,
                "metadata": c.chunk_metadata
            }
            for c in chunks
        ]
    }


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(KnowledgeDocument).filter(
        KnowledgeDocument.id == document_id,
        KnowledgeDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Remove file from disk if present
    if os.path.exists(doc.storage_path):
        try:
            os.remove(doc.storage_path)
        except Exception:
            pass

    db.delete(doc)
    audit = AuditEvent(
        user_id=current_user.id,
        event_type="DOC_DELETED",
        resource_type="document",
        action="delete_document",
        details={"filename": doc.filename}
    )
    db.add(audit)
    db.commit()
    return {"message": "Document and associated index chunks removed successfully"}


@router.post("/grounded-query", response_model=GroundedQueryResponse)
def grounded_query(
    query_req: GroundedQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    retriever_tool = tool_registry.get_tool("knowledge_retriever")
    if not retriever_tool:
        raise HTTPException(status_code=500, detail="Retriever tool not registered")

    search_res = retriever_tool.execute(
        {"query": query_req.question, "top_k": query_req.top_k or 4},
        context={"user": current_user, "db": db}
    )

    citations_raw = search_res.get("citations", [])
    if not citations_raw:
        return {
            "question": query_req.question,
            "answer": "I searched your uploaded knowledge documents, but found no relevant passages supporting an answer. Please verify that documents containing this information have been indexed.",
            "citations": [],
            "has_sufficient_evidence": False,
            "suggested_followups": [
                "Upload related reference documents in the Knowledge tab",
                "Rephrase your question using specific terminology"
            ]
        }

    citations = [
        SourceCitation(
            document_id=c["document_id"],
            filename=c["filename"],
            page_number=c["page_number"],
            snippet=c["snippet"],
            relevance_score=c["relevance_score"]
        )
        for c in citations_raw
    ]

    answer_parts = [
        f"Based on verified citations from your knowledge base:\n"
    ]
    for c in citations:
        answer_parts.append(
            f"- **{c.filename}** (Page {c.page_number}): \"{c.snippet.strip()}\""
        )
    answer_parts.append("\nThe above facts directly ground this answer. No unverified extrapolations were generated.")

    return {
        "question": query_req.question,
        "answer": "\n".join(answer_parts),
        "citations": citations,
        "has_sufficient_evidence": True,
        "suggested_followups": [
            f"What other topics are covered in {citations[0].filename}?",
            "Create an action plan from these requirements",
            "Export this summary to markdown"
        ]
    }
