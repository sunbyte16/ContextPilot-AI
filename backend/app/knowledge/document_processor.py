import os
import re
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.all_models import KnowledgeDocument, DocumentChunk, AuditEvent, User
from app.core.config import settings

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 60) -> List[str]:
    """Splits plain text into overlapping chunks cleanly on sentence/word boundaries."""
    if len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:].strip())
            break

        # Look for clean newline or punctuation boundary
        split_idx = text.rfind("\n\n", start, end)
        if split_idx == -1:
            split_idx = text.rfind(". ", start, end)
        if split_idx == -1:
            split_idx = text.rfind(" ", start, end)
        if split_idx == -1 or split_idx <= start:
            split_idx = end

        chunk_str = text[start:split_idx].strip()
        if chunk_str:
            chunks.append(chunk_str)
        start = split_idx + 1 - overlap if overlap < (split_idx - start) else split_idx + 1

    return chunks


def process_document(
    doc_id: str,
    file_bytes: bytes,
    filename: str,
    user: User,
    db: Session
) -> KnowledgeDocument:
    """Extracts text, splits into page-attributed chunks, and indexes."""
    doc = db.query(KnowledgeDocument).filter(
        KnowledgeDocument.id == doc_id,
        KnowledgeDocument.user_id == user.id
    ).first()

    if not doc:
        raise ValueError("Document record not found.")

    doc.processing_status = "PROCESSING"
    db.commit()

    try:
        pages_content: List[Tuple[int, str]] = []
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".pdf":
            if not PYPDF_AVAILABLE:
                raise RuntimeError("pypdf is not available for PDF processing.")
            import io
            reader = PdfReader(io.BytesIO(file_bytes))
            for page_idx, page in enumerate(reader.pages):
                txt = page.extract_text() or ""
                if txt.strip():
                    pages_content.append((page_idx + 1, txt))
            if not pages_content:
                # PDF was scanned or had no selectable text
                pages_content.append((1, f"[Scanned/Empty PDF: {filename}. OCR requires external OCR engine.]"))

        elif ext in [".txt", ".md", ".json", ".csv"]:
            decoded_text = file_bytes.decode("utf-8", errors="replace")
            pages_content.append((1, decoded_text))

        else:
            raise ValueError(f"Unsupported file extension: {ext}")

        # Chunk each page
        chunk_index = 0
        for page_num, p_text in pages_content:
            page_chunks = chunk_text(p_text, chunk_size=500, overlap=50)
            for ch in page_chunks:
                chunk_record = DocumentChunk(
                    document_id=doc.id,
                    chunk_index=chunk_index,
                    page_number=page_num,
                    content=ch,
                    chunk_metadata={"source_file": filename, "page": page_num}
                )
                db.add(chunk_record)
                chunk_index += 1

        doc.chunk_count = chunk_index
        doc.processing_status = "INDEXED"
        doc.error_message = None

        # Add audit event
        audit = AuditEvent(
            user_id=user.id,
            event_type="DOC_UPLOADED",
            resource_type="document",
            resource_id=doc.id,
            action="index_document",
            details={"filename": filename, "chunks": chunk_index, "file_size": len(file_bytes)}
        )
        db.add(audit)
        db.commit()
        db.refresh(doc)
        return doc

    except Exception as e:
        doc.processing_status = "FAILED"
        doc.error_message = str(e)
        db.commit()
        raise e
