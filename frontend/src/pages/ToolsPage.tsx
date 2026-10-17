import React, { useState, useEffect } from 'react';
import {
  Wrench,
  CheckCircle2,
  Clock,
  ShieldAlert,
  Play,
  Terminal,
  Code,
  Layers,
  Sparkles,
  ShieldCheck,
} from 'lucide-react';
import { api } from '../services/api';
import { ToolDefinition } from '../types';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Modal } from '../components/ui/Modal';
import { TextArea } from '../components/ui/Input';

export const ToolsPage: React.FC = () => {
  const [tools, setTools] = useState<ToolDefinition[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedTool, setSelectedTool] = useState<ToolDefinition | null>(null);
  const [testPayload, setTestPayload] = useState<string>('{}');
  const [testResult, setTestResult] = useState<any>(null);
  const [isExecuting, setIsExecuting] = useState(false);

  const fetchTools = async () => {
    try {
      setLoading(true);
      const data = await api.get<ToolDefinition[]>('/tools/');
      setTools(data || []);
    } catch {
      // Handled
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTools();
  }, []);

  const handleOpenTest = (tool: ToolDefinition) => {
    setSelectedTool(tool);
    setTestResult(null);

    // Provide pre-filled sample payload based on tool_id
    if (tool.tool_id === 'safe_calculator') {
      setTestPayload(JSON.stringify({ expression: '(14500 * 1.18) + sqrt(256)' }, null, 2));
    } else if (tool.tool_id === 'date_time') {
      setTestPayload(JSON.stringify({ operation: 'current_time' }, null, 2));
    } else if (tool.tool_id === 'data_analysis') {
      setTestPayload(
        JSON.stringify(
          {
            records: [
              { dept: 'Tech', cost: 420 },
              { dept: 'Tech', cost: 680 },
              { dept: 'Ops', cost: 310 },
            ],
            value_field: 'cost',
            group_by_field: 'dept',
          },
          null,
          2
        )
      );
    } else if (tool.tool_id === 'structured_summarizer') {
      setTestPayload(
        JSON.stringify(
          {
            text: 'ContextPilot AI orchestrates multi-step workflows. All operations require verified outputs. Sensitive actions must pass human approval.',
            max_takeaways: 3,
          },
          null,
          2
        )
      );
    } else if (tool.tool_id === 'notification_center') {
      setTestPayload(
        JSON.stringify(
          {
            action: 'create_notification',
            title: 'Direct Tool Execution Test',
            message: 'Notification invoked from the Tools Testbench.',
            notification_type: 'INFO',
          },
          null,
          2
        )
      );
    } else if (tool.tool_id === 'task_manager') {
      setTestPayload(JSON.stringify({ action: 'list_tasks' }, null, 2));
    } else {
      setTestPayload(JSON.stringify({}, null, 2));
    }
  };

  const handleExecuteTool = async () => {
    if (!selectedTool) return;
    setIsExecuting(true);
    setTestResult(null);

    try {
      let parsed = {};
      try {
        parsed = JSON.parse(testPayload);
      } catch {
        alert('Invalid JSON input payload');
        setIsExecuting(false);
        return;
      }

      const res = await api.post('/tools/execute', {
        tool_name: selectedTool.tool_id,
        input_payload: parsed,
      });
      setTestResult(res);
      await fetchTools();
    } catch (err: any) {
      setTestResult({ error: err.message, status: 'FAILURE' });
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
            <Wrench className="w-6 h-6 text-primary" />
            Registered Tools & Safety Registry
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Strictly sandboxed execution dispatchers. All tools enforce input validation and risk boundaries.
          </p>
        </div>

        <Badge variant="purple" size="md">
          {tools.length} Registered Tools Active
        </Badge>
      </div>

      {/* Safety Notice */}
      <div className="p-4 rounded-xl bg-muted/40 border border-border/70 flex items-start gap-3 text-xs text-muted-foreground">
        <ShieldCheck className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
        <div className="space-y-0.5">
          <p className="font-semibold text-foreground">Controlled Dispatcher & Security Policy</p>
          <p>
            AI agents cannot execute arbitrary bash, python exec, or shell calls. Every tool specifies an exact input and output JSON schema. Consequential operations (such as data export) strictly require human approval.
          </p>
        </div>
      </div>

      {/* Tools Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {tools.map((t) => (
          <Card key={t.tool_id} className="hover:border-primary/40 transition-all flex flex-col justify-between">
            <CardContent className="p-5 space-y-3">
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center font-bold text-xs border border-indigo-500/20">
                    <Terminal className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-foreground leading-snug">{t.name}</h3>
                    <span className="text-[10px] text-muted-foreground font-mono">id: {t.tool_id}</span>
                  </div>
                </div>

                <Badge
                  variant={
                    t.risk_level === 'HIGH' || t.risk_level === 'CRITICAL'
                      ? 'danger'
                      : t.risk_level === 'MEDIUM'
                      ? 'warning'
                      : 'default'
                  }
                  size="sm"
                >
                  {t.risk_level}
                </Badge>
              </div>

              <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">
                {t.description}
              </p>

              <div className="flex flex-wrap items-center gap-1.5 pt-1">
                {t.requires_approval ? (
                  <span className="text-[10px] text-amber-400 font-semibold bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                    Requires Human Approval
                  </span>
                ) : (
                  <span className="text-[10px] text-emerald-400 font-semibold bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                    Autonomous Safe
                  </span>
                )}
                <span className="text-[10px] text-muted-foreground bg-muted px-2 py-0.5 rounded font-mono">
                  v{t.version}
                </span>
              </div>
            </CardContent>

            <div className="p-4 border-t border-border/40 flex items-center justify-between text-[11px]">
              <span className="text-muted-foreground text-[10px]">
                {t.last_executed_at
                  ? `Last Run: ${new Date(t.last_executed_at).toLocaleTimeString()}`
                  : 'Idle (Ready)'}
              </span>

              <Button
                size="sm"
                variant="outline"
                onClick={() => handleOpenTest(t)}
                icon={<Play className="w-3 h-3 fill-current" />}
              >
                Test Tool
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Test Execution Modal */}
      <Modal
        isOpen={!!selectedTool}
        onClose={() => setSelectedTool(null)}
        title={`Testbench: ${selectedTool?.name || ''}`}
        description={`Direct controlled invocation of '${selectedTool?.tool_id}'.`}
        maxWidth="lg"
      >
        <div className="space-y-4">
          <TextArea
            label="Input Arguments (JSON)"
            rows={5}
            value={testPayload}
            onChange={(e) => setTestPayload(e.target.value)}
            className="font-mono text-xs"
          />

          <div className="flex justify-end gap-2">
            <Button variant="outline" size="sm" onClick={() => setSelectedTool(null)}>
              Cancel
            </Button>
            <Button
              variant="primary"
              size="sm"
              onClick={handleExecuteTool}
              isLoading={isExecuting}
              icon={<Play className="w-3.5 h-3.5" />}
            >
              Run Execution
            </Button>
          </div>

          {testResult && (
            <div className="space-y-1.5 pt-2 border-t border-border/40">
              <span className="text-[11px] font-semibold text-muted-foreground block">
                Execution Output Result:
              </span>
              <pre className="p-3 rounded-lg bg-background border border-border text-xs overflow-x-auto text-emerald-400 font-mono max-h-56">
                {JSON.stringify(testResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </Modal>
    </div>
  );
};
