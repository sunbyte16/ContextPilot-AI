import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Play,
  RotateCcw,
  Ban,
  CheckCircle2,
  Clock,
  ShieldAlert,
  ShieldCheck,
  Terminal,
  Activity,
  Layers,
  AlertTriangle,
  ChevronDown,
  ChevronUp,
  FileCheck,
} from 'lucide-react';
import { api } from '../services/api';
import { Task, TaskStep, ApprovalRequest, ExecutionEvent } from '../types';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Modal } from '../components/ui/Modal';
import { TextArea } from '../components/ui/Input';

export const TaskDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [task, setTask] = useState<Task | null>(null);
  const [events, setEvents] = useState<ExecutionEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const [expandedSteps, setExpandedSteps] = useState<Record<string, boolean>>({});
  const [decisionNotes, setDecisionNotes] = useState('');
  const [decisionModal, setDecisionModal] = useState<{ isOpen: boolean; approval: ApprovalRequest | null; approve: boolean }>({
    isOpen: false,
    approval: null,
    approve: true,
  });

  const fetchTaskDetail = async () => {
    if (!id) return;
    try {
      setLoading(true);
      const [taskRes, eventsRes] = await Promise.all([
        api.get<Task>(`/tasks/${id}`),
        api.get<ExecutionEvent[]>(`/tasks/${id}/events`),
      ]);
      setTask(taskRes);
      setEvents(eventsRes || []);
    } catch (err: any) {
      alert(`Failed to load task: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTaskDetail();
  }, [id]);

  const handleExecute = async () => {
    if (!id) return;
    setExecuting(true);
    try {
      await api.post(`/tasks/${id}/execute`);
      await fetchTaskDetail();
    } catch (err: any) {
      alert(`Execution error: ${err.message}`);
    } finally {
      setExecuting(false);
    }
  };

  const handleCancel = async () => {
    if (!id) return;
    try {
      await api.post(`/tasks/${id}/cancel`);
      await fetchTaskDetail();
    } catch (err: any) {
      alert(`Failed to cancel: ${err.message}`);
    }
  };

  const handleRetry = async () => {
    if (!id) return;
    setExecuting(true);
    try {
      await api.post(`/tasks/${id}/retry`);
      await fetchTaskDetail();
    } catch (err: any) {
      alert(`Retry failed: ${err.message}`);
    } finally {
      setExecuting(false);
    }
  };

  const submitDecision = async () => {
    if (!id || !decisionModal.approval) return;
    try {
      await api.post(`/tasks/${id}/approvals/${decisionModal.approval.id}`, {
        approved: decisionModal.approve,
        decision_notes: decisionNotes || undefined,
      });
      setDecisionModal({ isOpen: false, approval: null, approve: true });
      setDecisionNotes('');
      await fetchTaskDetail();
    } catch (err: any) {
      alert(`Approval submission error: ${err.message}`);
    }
  };

  const toggleStepExpanded = (stepId: string) => {
    setExpandedSteps((prev) => ({ ...prev, [stepId]: !prev[stepId] }));
  };

  if (loading && !task) {
    return (
      <div className="py-20 text-center text-xs text-muted-foreground">
        Loading task execution details...
      </div>
    );
  }

  if (!task) {
    return (
      <div className="py-20 text-center">
        <h2 className="text-sm font-semibold text-foreground">Task not found</h2>
        <Link to="/app/tasks" className="text-xs text-primary hover:underline mt-2 inline-block">
          Return to Tasks List
        </Link>
      </div>
    );
  }

  const pendingApprovals = (task.approvals || []).filter((a) => a.status === 'PENDING');

  return (
    <div className="space-y-6">
      {/* Back and Action Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <Link
            to="/app/tasks"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            Back to Task Monitor
          </Link>
          <h1 className="text-xl sm:text-2xl font-bold text-foreground leading-tight">
            {task.objective}
          </h1>
          <div className="flex flex-wrap items-center gap-2 pt-1">
            <Badge
              variant={
                task.status === 'COMPLETED'
                  ? 'success'
                  : task.status === 'AWAITING_APPROVAL'
                  ? 'warning'
                  : task.status === 'RUNNING'
                  ? 'info'
                  : task.status === 'FAILED'
                  ? 'danger'
                  : 'default'
              }
            >
              {task.status}
            </Badge>
            <Badge variant="outline" size="sm">Risk: {task.risk_level}</Badge>
            <Badge variant="outline" size="sm">Priority: {task.priority}</Badge>
            <span className="text-[11px] text-muted-foreground font-mono">
              Created: {new Date(task.created_at).toLocaleString()}
            </span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2 self-start sm:self-auto">
          {task.status !== 'COMPLETED' && task.status !== 'CANCELLED' && (
            <Button
              variant="primary"
              size="sm"
              onClick={handleExecute}
              isLoading={executing}
              icon={<Play className="w-3.5 h-3.5 fill-current" />}
            >
              {task.status === 'AWAITING_APPROVAL' ? 'Execute Unpaused' : 'Execute Plan'}
            </Button>
          )}

          {task.status === 'FAILED' && (
            <Button
              variant="secondary"
              size="sm"
              onClick={handleRetry}
              isLoading={executing}
              icon={<RotateCcw className="w-3.5 h-3.5" />}
            >
              Retry Step
            </Button>
          )}

          {task.status !== 'COMPLETED' && task.status !== 'CANCELLED' && (
            <Button variant="outline" size="sm" onClick={handleCancel} icon={<Ban className="w-3.5 h-3.5 text-rose-400" />}>
              Cancel
            </Button>
          )}
        </div>
      </div>

      {/* Verified Outcome Summary (if completed) */}
      {task.status === 'COMPLETED' && task.result_summary && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-start gap-3">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0 mt-0.5 text-emerald-400" />
          <div className="space-y-1">
            <p className="text-xs font-bold text-foreground">Verified Execution Outcome</p>
            <p className="text-xs text-muted-foreground">{task.result_summary}</p>
          </div>
        </div>
      )}

      {/* Human Approval Required Callout */}
      {pendingApprovals.length > 0 && (
        <Card className="border-amber-500/40 bg-amber-500/5 shadow-md">
          <CardHeader className="py-3 bg-amber-500/10 border-b border-amber-500/20">
            <CardTitle className="text-sm font-bold text-amber-400 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4" />
              Human-In-The-Loop Approval Required
            </CardTitle>
          </CardHeader>
          <CardContent className="p-5 space-y-4">
            {pendingApprovals.map((appr) => (
              <div
                key={appr.id}
                className="p-4 rounded-xl bg-card border border-border/80 flex flex-col md:flex-row md:items-center justify-between gap-4"
              >
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-foreground">{appr.action_name}</span>
                    <Badge variant="danger" size="sm">Risk: {appr.risk_level}</Badge>
                    <span className="text-[10px] text-muted-foreground font-mono">
                      Target: {appr.target_resource}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground">{appr.action_purpose}</p>

                  {appr.parameters_summary && (
                    <div className="mt-2 p-2 rounded bg-muted/40 font-mono text-[11px] text-muted-foreground">
                      Parameters: {JSON.stringify(appr.parameters_summary)}
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2 self-end md:self-center">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => setDecisionModal({ isOpen: true, approval: appr, approve: false })}
                  >
                    Reject Action
                  </Button>
                  <Button
                    size="sm"
                    variant="success"
                    icon={<ShieldCheck className="w-4 h-4" />}
                    onClick={() => setDecisionModal({ isOpen: true, approval: appr, approve: true })}
                  >
                    Approve Action
                  </Button>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Two Column Layout: Ordered Steps & Live Telemetry Events */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Ordered Execution Steps */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-foreground flex items-center gap-2">
              <Layers className="w-4 h-4 text-primary" />
              Ordered Execution Steps ({task.steps?.length || 0})
            </h2>
            <span className="text-xs text-muted-foreground font-medium">Progress: {task.progress}%</span>
          </div>

          <div className="space-y-3">
            {task.steps?.map((step) => {
              const isExpanded = !!expandedSteps[step.id];

              return (
                <Card
                  key={step.id}
                  className={`border transition-all ${
                    step.status === 'RUNNING'
                      ? 'border-sky-500/50 ring-1 ring-sky-500/20'
                      : step.status === 'COMPLETED'
                      ? 'border-emerald-500/30'
                      : step.status === 'AWAITING_APPROVAL'
                      ? 'border-amber-500/40 bg-amber-500/5'
                      : 'border-border'
                  }`}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-start gap-3">
                        <div
                          className={`w-7 h-7 rounded-lg flex items-center justify-center font-mono text-xs font-bold flex-shrink-0 mt-0.5 ${
                            step.status === 'COMPLETED'
                              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                              : step.status === 'RUNNING'
                              ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30 animate-pulse'
                              : step.status === 'AWAITING_APPROVAL'
                              ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                              : 'bg-muted text-muted-foreground'
                          }`}
                        >
                          {step.step_order}
                        </div>

                        <div className="space-y-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-xs font-semibold text-foreground">
                              {step.description}
                            </span>
                          </div>

                          <div className="flex flex-wrap items-center gap-2 pt-0.5">
                            <Badge variant="outline" size="sm" className="font-mono text-[10px]">
                              Tool: {step.tool_name || 'internal'}
                            </Badge>
                            <Badge
                              variant={
                                step.status === 'COMPLETED'
                                  ? 'success'
                                  : step.status === 'AWAITING_APPROVAL'
                                  ? 'warning'
                                  : step.status === 'RUNNING'
                                  ? 'info'
                                  : step.status === 'FAILED'
                                  ? 'danger'
                                  : 'default'
                              }
                              size="sm"
                            >
                              {step.status}
                            </Badge>
                            {step.execution_time_ms > 0 && (
                              <span className="text-[10px] text-muted-foreground font-mono">
                                {step.execution_time_ms}ms
                              </span>
                            )}
                          </div>
                        </div>
                      </div>

                      <button
                        onClick={() => toggleStepExpanded(step.id)}
                        className="p-1 rounded text-muted-foreground hover:text-foreground"
                      >
                        {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                      </button>
                    </div>

                    {/* Step Error Notice */}
                    {step.error_message && (
                      <div className="mt-3 p-2 rounded bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs">
                        Error: {step.error_message}
                      </div>
                    )}

                    {/* Collapsible Inspector */}
                    {isExpanded && (
                      <div className="mt-4 pt-3 border-t border-border/50 space-y-3 text-xs animate-in fade-in">
                        {step.tool_input && (
                          <div>
                            <span className="text-[11px] font-semibold text-muted-foreground block mb-1">
                              Tool Input Payload:
                            </span>
                            <pre className="p-2.5 rounded-lg bg-background border border-border text-[11px] overflow-x-auto text-sky-400 font-mono">
                              {JSON.stringify(step.tool_input, null, 2)}
                            </pre>
                          </div>
                        )}

                        {step.actual_output && (
                          <div>
                            <span className="text-[11px] font-semibold text-muted-foreground block mb-1">
                              Actual Tool Output (Verified):
                            </span>
                            <pre className="p-2.5 rounded-lg bg-background border border-border text-[11px] overflow-x-auto text-emerald-400 font-mono">
                              {JSON.stringify(step.actual_output, null, 2)}
                            </pre>
                          </div>
                        )}
                      </div>
                    )}
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Right Col: Live Execution Telemetry Stream */}
        <div className="space-y-4">
          <h2 className="text-sm font-bold text-foreground flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            Execution Telemetry & Trace
          </h2>

          <Card className="max-h-[500px] overflow-y-auto">
            <CardContent className="p-4 space-y-3 font-mono text-[11px]">
              {events.length === 0 ? (
                <div className="text-center py-6 text-muted-foreground">No events recorded.</div>
              ) : (
                events.map((ev) => (
                  <div key={ev.id} className="p-2 rounded bg-muted/40 border border-border/40 space-y-1">
                    <div className="flex items-center justify-between text-[10px] text-muted-foreground">
                      <span className="font-bold text-sky-400">{ev.event_type}</span>
                      <span>{new Date(ev.created_at).toLocaleTimeString()}</span>
                    </div>
                    <p className="text-foreground leading-snug">{ev.message}</p>
                  </div>
                ))
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Human Approval Decision Modal */}
      <Modal
        isOpen={decisionModal.isOpen}
        onClose={() => setDecisionModal({ isOpen: false, approval: null, approve: true })}
        title={decisionModal.approve ? 'Approve Consequential Action' : 'Reject Action'}
        description={`Target tool: ${decisionModal.approval?.target_resource || 'System'}`}
      >
        <div className="space-y-4">
          <p className="text-xs text-muted-foreground">
            {decisionModal.approve
              ? 'By approving, you authorize ContextPilot AI to execute this operation through registered tool dispatchers.'
              : 'Rejecting this step will cancel subsequent workflow actions and mark the task cancelled.'}
          </p>

          <TextArea
            label="Decision Notes (Optional)"
            placeholder="Add rationale or audit notes..."
            value={decisionNotes}
            onChange={(e) => setDecisionNotes(e.target.value)}
          />

          <div className="flex justify-end gap-2 pt-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setDecisionModal({ isOpen: false, approval: null, approve: true })}
            >
              Cancel
            </Button>
            <Button
              type="button"
              variant={decisionModal.approve ? 'success' : 'destructive'}
              size="sm"
              onClick={submitDecision}
            >
              {decisionModal.approve ? 'Confirm Approval' : 'Confirm Rejection'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};
