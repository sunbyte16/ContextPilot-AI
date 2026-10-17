import React, { useState, useEffect } from 'react';
import {
  Brain,
  Plus,
  Search,
  Pin,
  Trash2,
  Edit2,
  Layers,
  Sparkles,
  ShieldCheck,
  Tag,
} from 'lucide-react';
import { api } from '../services/api';
import { MemoryItem } from '../types';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Modal } from '../components/ui/Modal';
import { Input, TextArea } from '../components/ui/Input';

export const MemoryPage: React.FC = () => {
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [categoryFilter, setCategoryFilter] = useState<string>('ALL');
  const [search, setSearch] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [category, setCategory] = useState<'FACT' | 'PREFERENCE' | 'PROJECT_CONTEXT' | 'NOTE' | 'TASK_OUTCOME'>('FACT');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isPinned, setIsPinned] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const fetchMemories = async () => {
    try {
      setLoading(true);
      let url = '/memory/?';
      if (categoryFilter !== 'ALL') url += `category=${categoryFilter}&`;
      if (search) url += `search=${encodeURIComponent(search)}&`;
      const data = await api.get<MemoryItem[]>(url);
      setMemories(data || []);
    } catch {
      // Handled
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMemories();
  }, [categoryFilter, search]);

  const handleOpenCreate = () => {
    setEditingId(null);
    setCategory('FACT');
    setTitle('');
    setContent('');
    setIsPinned(false);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (m: MemoryItem) => {
    setEditingId(m.id);
    setCategory(m.category);
    setTitle(m.title);
    setContent(m.content);
    setIsPinned(m.is_pinned);
    setIsModalOpen(true);
  };

  const handleSaveMemory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;

    setIsSaving(true);
    try {
      if (editingId) {
        await api.put(`/memory/${editingId}`, {
          category,
          title,
          content,
          is_pinned: isPinned,
        });
      } else {
        await api.post('/memory/', {
          category,
          title,
          content,
          is_pinned: isPinned,
        });
      }
      setIsModalOpen(false);
      await fetchMemories();
    } catch (err: any) {
      alert(`Save error: ${err.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteMemory = async (id: string) => {
    if (!confirm('Are you sure you want to delete this memory?')) return;
    try {
      await api.delete(`/memory/${id}`);
      setMemories(memories.filter((m) => m.id !== id));
    } catch (err: any) {
      alert(`Delete error: ${err.message}`);
    }
  };

  const handleClearAll = async () => {
    if (!confirm('Clear all stored context memories? This action is permanent.')) return;
    try {
      await api.delete('/memory/');
      setMemories([]);
    } catch (err: any) {
      alert(`Clear error: ${err.message}`);
    }
  };

  const getCategoryColor = (cat: string) => {
    switch (cat) {
      case 'FACT':
        return 'info';
      case 'PREFERENCE':
        return 'purple';
      case 'PROJECT_CONTEXT':
        return 'success';
      case 'NOTE':
        return 'warning';
      case 'TASK_OUTCOME':
        return 'default';
      default:
        return 'default';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
            <Brain className="w-6 h-6 text-primary" />
            Context Memory Management
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Inspect, edit, and curate persistent facts and user preferences used by the agent
          </p>
        </div>

        <div className="flex items-center gap-2">
          {memories.length > 0 && (
            <Button variant="outline" size="sm" onClick={handleClearAll} icon={<Trash2 className="w-3.5 h-3.5 text-rose-400" />}>
              Clear All
            </Button>
          )}
          <Button variant="primary" size="sm" onClick={handleOpenCreate} icon={<Plus className="w-4 h-4" />}>
            Add Memory
          </Button>
        </div>
      </div>

      {/* Info Callout */}
      <div className="p-3.5 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-xs text-muted-foreground flex items-center gap-3">
        <Sparkles className="w-4 h-4 text-indigo-400 flex-shrink-0" />
        <span>
          Context memories are transparently injected into agent planning and reasoning. Pinned memories take highest priority.
        </span>
      </div>

      {/* Search & Filter */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between bg-card border border-border p-3 rounded-xl shadow-sm">
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-muted-foreground absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search saved facts & notes..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-lg border border-border bg-background text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
          {['ALL', 'FACT', 'PREFERENCE', 'PROJECT_CONTEXT', 'NOTE'].map((cat) => (
            <button
              key={cat}
              onClick={() => setCategoryFilter(cat)}
              className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors whitespace-nowrap ${
                categoryFilter === cat
                  ? 'bg-primary text-primary-foreground font-semibold'
                  : 'bg-muted/60 text-muted-foreground hover:bg-muted hover:text-foreground'
              }`}
            >
              {cat.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Memory Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {memories.length === 0 ? (
          <div className="col-span-full py-12 text-center">
            <Brain className="w-10 h-10 text-muted-foreground/40 mx-auto mb-2" />
            <h3 className="text-sm font-semibold text-foreground">No memories saved</h3>
            <p className="text-xs text-muted-foreground mt-1 max-w-sm mx-auto">
              Add explicit facts, deadlines, or preferences, or click "Seed Demo Data" to load realistic examples.
            </p>
          </div>
        ) : (
          memories.map((m) => (
            <Card key={m.id} className="hover:border-primary/40 transition-all flex flex-col justify-between">
              <CardContent className="p-5 space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <Badge variant={getCategoryColor(m.category)} size="sm">
                      {m.category.replace('_', ' ')}
                    </Badge>
                    {m.is_pinned && (
                      <span className="flex items-center gap-1 text-[10px] text-amber-400 font-semibold bg-amber-400/10 px-1.5 py-0.5 rounded border border-amber-400/20">
                        <Pin className="w-2.5 h-2.5 fill-current" />
                        Pinned
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => handleOpenEdit(m)}
                      className="p-1 rounded text-muted-foreground hover:text-foreground"
                      title="Edit memory"
                    >
                      <Edit2 className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => handleDeleteMemory(m.id)}
                      className="p-1 rounded text-muted-foreground hover:text-rose-400"
                      title="Delete memory"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-bold text-foreground mb-1">{m.title}</h3>
                  <p className="text-xs text-muted-foreground leading-relaxed whitespace-pre-wrap">
                    {m.content}
                  </p>
                </div>
              </CardContent>

              <div className="px-5 py-2.5 border-t border-border/40 text-[10px] text-slate-500 flex justify-between items-center">
                <span>Updated: {new Date(m.updated_at).toLocaleDateString()}</span>
                <span>Active Context</span>
              </div>
            </Card>
          ))
        )}
      </div>

      {/* Memory Create / Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingId ? 'Edit Stored Memory' : 'Record New Context Memory'}
        description="Preserve useful guidelines, dates, constraints, or preferences for agent orchestration."
      >
        <form onSubmit={handleSaveMemory} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-foreground tracking-wide mb-1.5">
              Category
            </label>
            <select
              value={category}
              onChange={(e: any) => setCategory(e.target.value)}
              className="w-full rounded-lg border border-border bg-background px-3 py-2 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
            >
              <option value="FACT">Fact</option>
              <option value="PREFERENCE">Preference</option>
              <option value="PROJECT_CONTEXT">Project Context</option>
              <option value="NOTE">Note</option>
              <option value="TASK_OUTCOME">Task Outcome</option>
            </select>
          </div>

          <Input
            label="Title"
            required
            placeholder="e.g. ML Exam Date"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <TextArea
            label="Content"
            required
            rows={3}
            placeholder="Details or guidelines for the agent to remember..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />

          <label className="flex items-center gap-2 cursor-pointer text-xs text-foreground">
            <input
              type="checkbox"
              checked={isPinned}
              onChange={(e) => setIsPinned(e.target.checked)}
              className="rounded border-border text-primary focus:ring-primary"
            />
            <span>Pin this memory (Prioritize in all agent prompts)</span>
          </label>

          <div className="flex justify-end gap-2 pt-2">
            <Button type="button" variant="outline" size="sm" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" size="sm" isLoading={isSaving}>
              {editingId ? 'Update Memory' : 'Save Memory'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
