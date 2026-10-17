import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ListTodo,
  Plus,
  Search,
  Filter,
  ArrowRight,
  ShieldAlert,
  CheckCircle2,
  Clock,
  Layers,
  Sparkles,
} from 'lucide-react';
import { api } from '../services/api';
import { Task } from '../types';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent } from '../components/ui/Card';
import { Modal } from '../components/ui/Modal';
import { Input, TextArea } from '../components/ui/Input';

export const TasksPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [search, setSearch] = useState<string>('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newObjective, setNewObjective] = useState('');
  const [newPriority, setNewPriority] = useState('MEDIUM');
  const [isCreating, setIsCreating] = useState(false);
  const navigate = useNavigate();

  const fetchTasks = async () => {
    try {
      setLoading(true);
      let url = '/tasks/?';
      if (statusFilter !== 'ALL') url += `status=${statusFilter}&`;
      if (search) url += `search=${encodeURIComponent(search)}&`;
      const data = await api.get<Task[]>(url);
      setTasks(data || []);
    } catch {
      // Handled
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [statusFilter, search]);

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newObjective.trim()) return;

    setIsCreating(true);
    try {
      const created = await api.post<Task>('/tasks/', {
        objective: newObjective,
        priority: newPriority,
      });
      setIsModalOpen(false);
      navigate(`/app/tasks/${created.id}`);
    } catch (err: any) {
      alert(`Failed to create task plan: ${err.message}`);
    } finally {
      setIsCreating(false);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return <Badge variant="success">Completed</Badge>;
      case 'AWAITING_APPROVAL':
        return <Badge variant="warning">Awaiting Approval</Badge>;
      case 'RUNNING':
        return <Badge variant="info">Executing</Badge>;
      case 'FAILED':
        return <Badge variant="danger">Failed</Badge>;
      case 'CANCELLED':
        return <Badge variant="outline">Cancelled</Badge>;
      default:
        return <Badge variant="default">{status}</Badge>;
    }
  };

  const getRiskBadge = (risk: string) => {
    switch (risk) {
      case 'CRITICAL':
      case 'HIGH':
        return <Badge variant="danger" size="sm">Risk: {risk}</Badge>;
      case 'MEDIUM':
        return <Badge variant="warning" size="sm">Risk: {risk}</Badge>;
      default:
        return <Badge variant="default" size="sm">Risk: {risk}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
            <ListTodo className="w-6 h-6 text-primary" />
            Task Management & Workflow Plans
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Orchestrate multi-step pipelines with automated dependency resolution
          </p>
        </div>

        <Button
          onClick={() => setIsModalOpen(true)}
          icon={<Plus className="w-4 h-4" />}
          variant="primary"
        >
          Create New Plan
        </Button>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between bg-card border border-border p-3 rounded-xl shadow-sm">
        {/* Search Input */}
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-muted-foreground absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search objectives..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-lg border border-border bg-background text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground"
          />
        </div>

        {/* Status Filters */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
          {['ALL', 'AWAITING_APPROVAL', 'RUNNING', 'COMPLETED', 'FAILED'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors whitespace-nowrap ${
                statusFilter === st
                  ? 'bg-primary text-primary-foreground font-semibold'
                  : 'bg-muted/60 text-muted-foreground hover:bg-muted hover:text-foreground'
              }`}
            >
              {st === 'ALL' ? 'All Tasks' : st.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Tasks List */}
      <div className="space-y-3">
        {tasks.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <Layers className="w-10 h-10 text-muted-foreground/40 mx-auto mb-3" />
              <h3 className="text-sm font-semibold text-foreground">No tasks found</h3>
              <p className="text-xs text-muted-foreground mt-1 max-w-sm mx-auto">
                No workflows match your search or filter criteria. Create a new task plan above or click "Seed Demo Data" in the top bar.
              </p>
            </CardContent>
          </Card>
        ) : (
          tasks.map((task) => (
            <Link key={task.id} to={`/app/tasks/${task.id}`} className="block">
              <Card className="hover:border-primary/40 transition-all hover:shadow-md">
                <CardContent className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="space-y-2 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      {getStatusBadge(task.status)}
                      {getRiskBadge(task.risk_level)}
                      <Badge variant="outline" size="sm">Priority: {task.priority}</Badge>
                      <span className="text-[10px] text-muted-foreground font-mono">
                        Complexity: {task.estimated_complexity}
                      </span>
                    </div>

                    <h3 className="text-sm font-semibold text-foreground leading-snug">
                      {task.objective}
                    </h3>

                    {task.description && (
                      <p className="text-xs text-muted-foreground line-clamp-1">{task.description}</p>
                    )}

                    <div className="flex items-center gap-4 text-[11px] text-muted-foreground pt-1">
                      <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                      <span>•</span>
                      <span>{task.step_count || 0} Steps</span>
                      {task.result_summary && (
                        <>
                          <span>•</span>
                          <span className="text-emerald-400 font-medium">Outcome Verified</span>
                        </>
                      )}
                    </div>
                  </div>

                  {/* Progress & Chevron */}
                  <div className="flex items-center gap-4 self-end sm:self-center flex-shrink-0">
                    <div className="w-24 text-right">
                      <span className="text-xs font-semibold text-foreground">{task.progress}%</span>
                      <div className="w-full h-1.5 bg-muted rounded-full overflow-hidden mt-1">
                        <div
                          className="h-full bg-primary rounded-full transition-all duration-300"
                          style={{ width: `${task.progress}%` }}
                        />
                      </div>
                    </div>
                    <ArrowRight className="w-4 h-4 text-muted-foreground" />
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))
        )}
      </div>

      {/* New Task Plan Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Formulate New Agent Plan"
        description="The planning engine will decompose your objective into validated steps with tool assignments and risk ratings."
      >
        <form onSubmit={handleCreateTask} className="space-y-4">
          <TextArea
            label="What is your objective?"
            required
            rows={4}
            placeholder="e.g. Analyze quarterly cloud spend data and export report..."
            value={newObjective}
            onChange={(e) => setNewObjective(e.target.value)}
          />

          <div>
            <label className="block text-xs font-medium text-foreground tracking-wide mb-1.5">
              Priority Level
            </label>
            <select
              value={newPriority}
              onChange={(e) => setNewPriority(e.target.value)}
              className="w-full rounded-lg border border-border bg-background px-3 py-2 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
            >
              <option value="LOW">Low</option>
              <option value="MEDIUM">Medium</option>
              <option value="HIGH">High</option>
              <option value="URGENT">Urgent</option>
            </select>
          </div>

          <div className="pt-2 flex justify-end gap-2">
            <Button type="button" variant="outline" size="sm" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" size="sm" isLoading={isCreating}>
              Decompose Objective
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
