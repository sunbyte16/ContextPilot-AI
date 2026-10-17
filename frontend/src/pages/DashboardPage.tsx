import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Sparkles,
  Bot,
  ListTodo,
  ShieldAlert,
  ArrowRight,
  CheckCircle2,
  Clock,
  Wrench,
  Activity,
  Layers,
  FileText,
  AlertTriangle,
  Play,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { Task, ToolDefinition, AnalyticsSummary, IntegrationStatus } from '../types';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [objectiveInput, setObjectiveInput] = useState('');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [integrations, setIntegrations] = useState<IntegrationStatus[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [tasksRes, analyticsRes, integRes] = await Promise.all([
        api.get<Task[]>('/tasks/'),
        api.get<AnalyticsSummary>('/analytics/summary'),
        api.get<{ integrations: IntegrationStatus[] }>('/settings/integrations'),
      ]);
      setTasks(tasksRes || []);
      setAnalytics(analyticsRes);
      setIntegrations(integRes.integrations || []);
    } catch {
      // Handled
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleStartObjective = (e: React.FormEvent) => {
    e.preventDefault();
    if (!objectiveInput.trim()) return;
    navigate('/app/assistant', { state: { initialPrompt: objectiveInput } });
  };

  const handlePromptClick = (prompt: string) => {
    navigate('/app/assistant', { state: { initialPrompt: prompt } });
  };

  const pendingApprovals = tasks.filter((t) => t.status === 'AWAITING_APPROVAL');

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

  return (
    <div className="space-y-6">
      {/* Greeting & Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
            Welcome back, {user?.full_name?.split(' ')[0] || 'Pilot'}
            <span className="text-lg">👋</span>
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Agentic AI Workspace & Task Orchestrator | Alexa+ Inspired Environment
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link to="/app/assistant">
            <Button size="sm" icon={<Bot className="w-4 h-4 text-sky-400" />}>
              Open Assistant
            </Button>
          </Link>
          <Link to="/app/tasks">
            <Button variant="outline" size="sm" icon={<ListTodo className="w-4 h-4" />}>
              View All Tasks
            </Button>
          </Link>
        </div>
      </div>

      {/* Quick Objective Composer */}
      <Card className="bg-gradient-to-br from-card via-card to-indigo-950/20 border-border/80 shadow-md">
        <CardContent className="p-6">
          <div className="max-w-3xl">
            <div className="flex items-center gap-2 text-xs font-semibold text-primary mb-2">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>What would you like ContextPilot to execute?</span>
            </div>
            <form onSubmit={handleStartObjective} className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                placeholder="e.g. Prepare a study plan for my machine learning exam..."
                value={objectiveInput}
                onChange={(e) => setObjectiveInput(e.target.value)}
                className="flex-1 px-4 py-2.5 rounded-xl border border-border bg-background/80 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 text-foreground placeholder:text-muted-foreground"
              />
              <Button type="submit" size="md" icon={<ArrowRight className="w-4 h-4" />}>
                Decompose & Plan
              </Button>
            </form>

            <div className="mt-4 flex flex-wrap items-center gap-2">
              <span className="text-[11px] text-muted-foreground font-medium">Quick suggestions:</span>
              {[
                'Prepare a study plan for my machine learning exam',
                'Analyze quarterly cloud spend data and export report',
                'Summarize my uploaded project documents',
                'Calculate (14500 * 1.18) + sqrt(256)',
              ].map((p, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handlePromptClick(p)}
                  className="text-[11px] px-2.5 py-1 rounded-lg bg-muted/60 hover:bg-muted text-muted-foreground hover:text-foreground transition-colors border border-border/40 text-left"
                >
                  {p}
                </button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Pending Approvals Warning Callout (if any) */}
      {pendingApprovals.length > 0 && (
        <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 animate-in fade-in">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center flex-shrink-0">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-semibold text-foreground">
                {pendingApprovals.length} Action{pendingApprovals.length > 1 ? 's' : ''} Awaiting Human Approval
              </p>
              <p className="text-[11px] text-muted-foreground mt-0.5">
                Consequential steps are paused. Review required permissions and approve or reject to continue.
              </p>
            </div>
          </div>
          <Link to={`/app/tasks/${pendingApprovals[0].id}`}>
            <Button size="sm" variant="primary" icon={<ArrowRight className="w-3.5 h-3.5" />}>
              Review Action
            </Button>
          </Link>
        </div>
      )}

      {/* Metrics Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-sky-500/10 text-sky-400 flex items-center justify-center">
              <ListTodo className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[11px] text-muted-foreground font-medium">Total Workflows</p>
              <p className="text-xl font-bold text-foreground">{analytics?.total_tasks ?? 0}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[11px] text-muted-foreground font-medium">Verified Completed</p>
              <p className="text-xl font-bold text-foreground">{analytics?.completed_tasks ?? 0}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[11px] text-muted-foreground font-medium">Pending Approvals</p>
              <p className="text-xl font-bold text-foreground">{analytics?.pending_approvals ?? 0}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
              <Wrench className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[11px] text-muted-foreground font-medium">Tool Executions</p>
              <p className="text-xl font-bold text-foreground">{analytics?.total_tool_executions ?? 0}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Grid: Active Tasks & System Integrations */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Tasks List */}
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between py-4">
              <div>
                <CardTitle>Recent Task Workflows</CardTitle>
                <p className="text-xs text-muted-foreground mt-0.5">Persisted agent plans and execution states</p>
              </div>
              <Link to="/app/tasks" className="text-xs text-primary hover:underline font-medium">
                View All
              </Link>
            </CardHeader>
            <CardContent className="p-0 divide-y divide-border/40">
              {tasks.length === 0 ? (
                <div className="p-8 text-center">
                  <Bot className="w-8 h-8 text-muted-foreground mx-auto mb-2 opacity-50" />
                  <p className="text-xs font-semibold text-foreground">No tasks recorded yet</p>
                  <p className="text-[11px] text-muted-foreground mt-1 max-w-xs mx-auto">
                    Submit your first objective above or click "Seed Demo Data" in the top bar to explore pre-built workflows.
                  </p>
                </div>
              ) : (
                tasks.slice(0, 5).map((task) => (
                  <Link
                    key={task.id}
                    to={`/app/tasks/${task.id}`}
                    className="p-4 flex items-center justify-between hover:bg-muted/40 transition-colors block"
                  >
                    <div className="space-y-1 max-w-md pr-4">
                      <div className="flex items-center gap-2">
                        {getStatusBadge(task.status)}
                        <span className="text-[10px] text-muted-foreground uppercase font-mono tracking-wider">
                          Risk: {task.risk_level}
                        </span>
                      </div>
                      <p className="text-xs font-semibold text-foreground line-clamp-1">
                        {task.objective}
                      </p>
                      <div className="flex items-center gap-3 text-[10px] text-muted-foreground">
                        <span>{new Date(task.created_at).toLocaleDateString()}</span>
                        <span>•</span>
                        <span>{task.step_count || 0} Steps</span>
                        {task.result_summary && (
                          <>
                            <span>•</span>
                            <span className="text-emerald-400">Verified Output Available</span>
                          </>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center gap-3 flex-shrink-0">
                      <div className="w-20 hidden sm:block">
                        <div className="flex justify-between text-[10px] text-muted-foreground mb-1">
                          <span>Progress</span>
                          <span>{task.progress}%</span>
                        </div>
                        <div className="w-full h-1.5 bg-muted rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary rounded-full transition-all duration-300"
                            style={{ width: `${task.progress}%` }}
                          />
                        </div>
                      </div>
                      <ArrowRight className="w-4 h-4 text-muted-foreground" />
                    </div>
                  </Link>
                ))
              )}
            </CardContent>
          </Card>
        </div>

        {/* Integration Status & Ecosystem */}
        <div className="space-y-4">
          <Card>
            <CardHeader className="py-4">
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-4 h-4 text-sky-400" />
                Integration Status
              </CardTitle>
              <p className="text-xs text-muted-foreground mt-0.5">Real-time adapter health inspection</p>
            </CardHeader>
            <CardContent className="p-4 space-y-3">
              {integrations.map((integ, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-lg border border-border/50 bg-background/50 flex flex-col gap-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-foreground">{integ.name}</span>
                    <Badge
                      variant={
                        integ.status === 'CONNECTED'
                          ? 'success'
                          : integ.status === 'SIMULATED'
                          ? 'info'
                          : 'default'
                      }
                      size="sm"
                    >
                      {integ.status}
                    </Badge>
                  </div>
                  <p className="text-[11px] text-muted-foreground leading-relaxed">{integ.details}</p>
                  <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1 border-t border-border/30">
                    <span>Provider: {integ.provider}</span>
                    {integ.latency_ms !== undefined && <span>{integ.latency_ms}ms</span>}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};
