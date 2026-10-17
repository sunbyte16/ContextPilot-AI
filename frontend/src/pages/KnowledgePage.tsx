import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  Upload,
  FileText,
  Trash2,
  Search,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  FileCode,
  Layers,
  ArrowRight,
} from 'lucide-react';
import { api } from '../services/api';
import { KnowledgeDocument, DocumentChunk, GroundedQueryResult, SourceCitation } from '../types';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Modal } from '../components/ui/Modal';

export const KnowledgePage: React.FC = () => {
  const [documents, setDocuments] = useState<KnowledgeDocument[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<{ doc: KnowledgeDocument; chunks: DocumentChunk[] } | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [loading, setLoading] = useState(true);

  // Grounded Query Sandbox
  const [qaQuestion, setQaQuestion] = useState('');
  const [qaLoading, setQaLoading] = useState(false);
  const [qaResult, setQaResult] = useState<{
    answer: string;
    citations: SourceCitation[];
    hasEvidence: boolean;
  } | null>(null);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const data = await api.get<KnowledgeDocument[]>('/knowledge/');
      setDocuments(data || []);
    } catch {
      // Handled
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setIsUploading(true);
    try {
      await api.post('/knowledge/upload', formData);
      await fetchDocuments();
    } catch (err: any) {
      alert(`Upload failed: ${err.message}`);
    } finally {
      setIsUploading(false);
      e.target.value = '';
    }
  };

  const handleViewChunks = async (docId: string) => {
    try {
      const res = await api.get<{ document: KnowledgeDocument; chunks: DocumentChunk[] }>(`/knowledge/${docId}`);
      setSelectedDoc({ doc: res.document, chunks: res.chunks || [] });
    } catch (err: any) {
      alert(`Failed to load chunks: ${err.message}`);
    }
  };

  const handleDeleteDocument = async (docId: string) => {
    if (!confirm('Are you sure you want to delete this document and all indexed chunks?')) return;
    try {
      await api.delete(`/knowledge/${docId}`);
      setDocuments(documents.filter((d) => d.id !== docId));
      if (selectedDoc?.doc.id === docId) setSelectedDoc(null);
    } catch (err: any) {
      alert(`Delete failed: ${err.message}`);
    }
  };

  const handleRunGroundedQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!qaQuestion.trim()) return;

    setQaLoading(true);
    try {
      const res = await api.post<{
        answer: string;
        citations: SourceCitation[];
        has_sufficient_evidence: boolean;
      }>('/knowledge/grounded-query', {
        question: qaQuestion,
        top_k: 3,
      });

      setQaResult({
        answer: res.answer,
        citations: res.citations || [],
        hasEvidence: res.has_sufficient_evidence,
      });
    } catch (err: any) {
      alert(`Query failed: ${err.message}`);
    } finally {
      setQaLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-primary" />
            Knowledge Base & Grounded RAG
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Upload domain documents (PDF, Markdown, Text) for verified semantic retrieval and grounded answers
          </p>
        </div>

        {/* Upload Trigger */}
        <label className="cursor-pointer">
          <input
            type="file"
            accept=".pdf,.txt,.md,.json,.csv"
            className="hidden"
            onChange={handleFileUpload}
            disabled={isUploading}
          />
          <div className="inline-flex items-center justify-center font-medium rounded-lg text-sm px-4 py-2 gap-2 bg-primary text-primary-foreground hover:bg-indigo-600 transition-colors shadow-sm select-none">
            <Upload className="w-4 h-4" />
            <span>{isUploading ? 'Chunking & Indexing...' : 'Upload Document'}</span>
          </div>
        </label>
      </div>

      {/* Grounded Query Tester Card */}
      <Card className="border-sky-500/30 bg-sky-500/5">
        <CardHeader className="py-3">
          <CardTitle className="text-sm font-bold text-sky-400 flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            Grounded Q&A Verification Sandbox
          </CardTitle>
          <p className="text-xs text-muted-foreground">
            Test how the agent retrieves passages and verifies claims against your uploaded documents
          </p>
        </CardHeader>
        <CardContent className="p-4 space-y-4">
          <form onSubmit={handleRunGroundedQuery} className="flex gap-2">
            <input
              type="text"
              placeholder="e.g. What does the guide say about human approvals?"
              value={qaQuestion}
              onChange={(e) => setQaQuestion(e.target.value)}
              className="flex-1 px-3.5 py-2 rounded-lg border border-border bg-background text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
            />
            <Button type="submit" size="sm" variant="primary" isLoading={qaLoading}>
              Ask Knowledge Base
            </Button>
          </form>

          {qaResult && (
            <div className="p-4 rounded-xl bg-card border border-border/80 space-y-3 animate-in fade-in">
              <div className="flex items-center gap-2">
                <Badge variant={qaResult.hasEvidence ? 'success' : 'warning'} size="sm">
                  {qaResult.hasEvidence ? 'Sufficient Evidence' : 'Insufficient Evidence Disclosed'}
                </Badge>
                <span className="text-[11px] text-muted-foreground font-mono">
                  {qaResult.citations.length} Verified Citation{qaResult.citations.length !== 1 ? 's' : ''}
                </span>
              </div>

              <p className="text-xs text-foreground whitespace-pre-wrap leading-relaxed">
                {qaResult.answer}
              </p>

              {qaResult.citations.length > 0 && (
                <div className="space-y-1.5 pt-2 border-t border-border/40">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider block">
                    Source Citations:
                  </span>
                  {qaResult.citations.map((c, i) => (
                    <div
                      key={i}
                      className="p-2 rounded bg-muted/30 border border-border/40 text-[11px] text-muted-foreground space-y-0.5"
                    >
                      <div className="flex items-center justify-between text-foreground font-semibold text-[10px]">
                        <span>📄 {c.filename} (Page {c.page_number})</span>
                        <span className="text-sky-400 font-mono">Relevance: {c.relevance_score}</span>
                      </div>
                      <p className="italic">"{c.snippet}"</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Documents Grid */}
      <div className="space-y-3">
        <h2 className="text-sm font-bold text-foreground flex items-center gap-2">
          <Layers className="w-4 h-4 text-primary" />
          Indexed Knowledge Documents ({documents.length})
        </h2>

        {documents.length === 0 ? (
          <Card>
            <CardContent className="p-10 text-center">
              <FileText className="w-8 h-8 text-muted-foreground/40 mx-auto mb-2" />
              <h3 className="text-sm font-semibold text-foreground">No documents uploaded</h3>
              <p className="text-xs text-muted-foreground mt-1 max-w-sm mx-auto">
                Upload a PDF or markdown document above, or click "Seed Demo Data" to load our sample Bedrock architecture guide.
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {documents.map((doc) => (
              <Card key={doc.id} className="hover:border-primary/40 transition-all flex flex-col justify-between">
                <CardContent className="p-5 space-y-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="w-8 h-8 rounded-lg bg-sky-500/10 text-sky-400 flex items-center justify-center font-bold text-xs uppercase flex-shrink-0">
                      {doc.file_type}
                    </div>
                    <Badge variant={doc.processing_status === 'INDEXED' ? 'success' : 'danger'} size="sm">
                      {doc.processing_status}
                    </Badge>
                  </div>

                  <div>
                    <h3 className="text-xs font-bold text-foreground truncate" title={doc.filename}>
                      {doc.filename}
                    </h3>
                    <p className="text-[11px] text-muted-foreground mt-1">
                      {(doc.file_size_bytes / 1024).toFixed(1)} KB • {doc.chunk_count} Text Chunks
                    </p>
                  </div>

                  <div className="flex items-center justify-between pt-2 border-t border-border/40">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleViewChunks(doc.id)}
                    >
                      Inspect Chunks
                    </Button>
                    <button
                      onClick={() => handleDeleteDocument(doc.id)}
                      className="p-1 text-muted-foreground hover:text-rose-400 transition-colors"
                      title="Delete document"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Chunks Inspector Modal */}
      <Modal
        isOpen={!!selectedDoc}
        onClose={() => setSelectedDoc(null)}
        title={`Chunk Index: ${selectedDoc?.doc.filename || ''}`}
        description={`${selectedDoc?.chunks.length || 0} chunks extracted and indexed`}
        maxWidth="lg"
      >
        <div className="max-h-[60vh] overflow-y-auto space-y-3 pr-1">
          {selectedDoc?.chunks.map((ch) => (
            <div key={ch.id} className="p-3 rounded-lg border border-border/70 bg-background space-y-1.5">
              <div className="flex items-center justify-between text-[10px] text-muted-foreground font-mono">
                <span>Chunk #{ch.chunk_index + 1}</span>
                <span>Page {ch.page_number}</span>
              </div>
              <p className="text-xs text-foreground font-mono leading-relaxed whitespace-pre-wrap">
                {ch.content}
              </p>
            </div>
          ))}
        </div>
      </Modal>
    </div>
  );
};
