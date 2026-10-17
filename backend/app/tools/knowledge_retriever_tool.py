import re
from typing import Dict, Any, Optional, List
from app.tools.base import BaseTool
from app.models.all_models import KnowledgeDocument, DocumentChunk, Memory


STOP_WORDS = {
    "a", "an", "the", "in", "on", "at", "to", "for", "with", "is", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "shall", "should", "can", "could", "may", "might", "must",
    "of", "and", "or", "but", "if", "what", "which", "who", "whom", "this",
    "that", "these", "those", "how", "why", "when", "where", "it", "its"
}


def calculate_bm25_score(query_tokens: List[str], text_tokens: List[str], doc_len: int, avg_doc_len: float) -> float:
    # Simplified BM25 ranking formulation
    k1 = 1.5
    b = 0.75
    score = 0.0
    text_token_counts = {}
    for tok in text_tokens:
        text_token_counts[tok] = text_token_counts.get(tok, 0) + 1

    content_tokens = [q for q in query_tokens if q not in STOP_WORDS]
    if not content_tokens:
        content_tokens = query_tokens

    matched_content = False
    for q in content_tokens:
        if q in text_token_counts:
            matched_content = True
            tf = text_token_counts[q]
            idf = 1.0  # Normalized weight
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (doc_len / (avg_doc_len or 1.0)))
            score += idf * (numerator / (denominator or 1.0))
    return score if matched_content else 0.0


class KnowledgeRetrieverTool(BaseTool):
    tool_id = "knowledge_retriever"
    name = "Knowledge & Document Retriever"
    description = "Searches authorized user knowledge documents and returns matching chunks with citations and source pages."
    version = "1.0.0"
    risk_level = "LOW"
    requires_approval = False
    implementation_type = "local"

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language query or keywords to search"
                },
                "top_k": {
                    "type": "integer",
                    "default": 3,
                    "description": "Maximum number of passages to return"
                }
            },
            "required": ["query"]
        }

    def get_output_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "query": {"type": "string"},
                "results_count": {"type": "integer"},
                "citations": {"type": "array"}
            }
        }

    def execute(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        query = params.get("query", "").strip()
        top_k = params.get("top_k", 3)
        db = context.get("db") if context else None
        user = context.get("user") if context else None

        if not db or not user:
            raise ValueError("Database and user context required for KnowledgeRetrieverTool.")

        if not query:
            return {"success": True, "query": "", "results_count": 0, "citations": []}

        # Query all chunks belonging to user's documents
        chunks = (
            db.query(DocumentChunk, KnowledgeDocument)
            .join(KnowledgeDocument, DocumentChunk.document_id == KnowledgeDocument.id)
            .filter(KnowledgeDocument.user_id == user.id)
            .all()
        )

        query_tokens = [tok.lower() for tok in re.findall(r'\w+', query)]
        if not query_tokens or not chunks:
            return {"success": True, "query": query, "results_count": 0, "citations": []}

        # Calculate average chunk length
        total_len = sum(len(c.content.split()) for c, _ in chunks)
        avg_len = total_len / len(chunks) if chunks else 1.0

        scored = []
        for chunk, doc in chunks:
            chunk_tokens = [tok.lower() for tok in re.findall(r'\w+', chunk.content)]
            score = calculate_bm25_score(query_tokens, chunk_tokens, len(chunk_tokens), avg_len)
            if score > 0:
                # Highlight or create snippet
                snippet = chunk.content[:300] + ("..." if len(chunk.content) > 300 else "")
                scored.append({
                    "document_id": doc.id,
                    "filename": doc.filename,
                    "page_number": chunk.page_number,
                    "snippet": snippet,
                    "full_content": chunk.content,
                    "relevance_score": round(score, 3)
                })

        # Sort descending by score
        scored.sort(key=lambda x: x["relevance_score"], reverse=True)
        top_results = scored[:top_k]

        return {
            "success": True,
            "query": query,
            "results_count": len(top_results),
            "citations": top_results
        }
