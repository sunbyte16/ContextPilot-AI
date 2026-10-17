from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict


class DocumentChunkResponse(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    page_number: int
    content: str
    chunk_metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class KnowledgeDocumentResponse(BaseModel):
    id: str
    user_id: str
    filename: str
    file_type: str
    file_size_bytes: int
    processing_status: str
    error_message: Optional[str] = None
    chunk_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SourceCitation(BaseModel):
    document_id: str
    filename: str
    page_number: int
    snippet: str
    relevance_score: float


class GroundedQueryRequest(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None
    top_k: Optional[int] = 4


class GroundedQueryResponse(BaseModel):
    question: str
    answer: str
    citations: List[SourceCitation] = []
    has_sufficient_evidence: bool = True
    suggested_followups: List[str] = []
