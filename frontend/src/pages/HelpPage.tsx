import React from 'react';
import {
  HelpCircle,
  Bot,
  ShieldCheck,
  Wrench,
  BookOpen,
  Cpu,
  Layers,
  Terminal,
  ExternalLink,
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

export const HelpPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
          <HelpCircle className="w-6 h-6 text-primary" />
          Documentation & User Guide
        </h1>
        <p className="text-xs text-muted-foreground mt-0.5">
          Everything you need to orchestrate workflows and configure AWS Bedrock
        </p>
      </div>

      {/* Guide Cards */}
      <div className="space-y-5">
        {/* Core Agent Lifecycle */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <Bot className="w-5 h-5 text-indigo-400" />
              1. The Verifiable Agent Lifecycle
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6 space-y-3 text-xs text-muted-foreground leading-relaxed">
            <p>
              Unlike traditional chatbots that simply generate prose, ContextPilot AI is an <strong>agentic task orchestrator</strong>. When you submit an objective:
            </p>
            <ol className="list-decimal pl-5 space-y-1.5 text-foreground">
              <li>
                <strong>Planning Engine:</strong> Decomposes natural language into an ordered set of steps mapped to registered tools.
              </li>
              <li>
                <strong>Risk Classification:</strong> Each step is labeled as <span className="text-emerald-400 font-semibold">LOW</span>, <span className="text-amber-400 font-semibold">MEDIUM</span>, or <span className="text-rose-400 font-semibold">HIGH</span> risk.
              </li>
              <li>
                <strong>Approval Gate:</strong> Any consequential step (such as data export or external alerts) triggers a server-side pause until you grant explicit human approval.
              </li>
              <li>
                <strong>Sandboxed Execution:</strong> The backend dispatcher executes the designated tool, records duration and timestamps, and verifies the outcome.
              </li>
            </ol>
          </CardContent>
        </Card>

        {/* Human-in-the-Loop Security */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-amber-400" />
              2. Human-In-The-Loop Approval Gates
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6 space-y-3 text-xs text-muted-foreground leading-relaxed">
            <p>
              Security is enforced on the server, not just in UI presentation. When a task step has <code>requires_approval=True</code>, the backend orchestrator transitions the task to <code>AWAITING_APPROVAL</code> and refuses to execute the tool until a signed decision is posted to <code>{'/api/v1/tasks/{id}/approvals/{approval_id}'}</code>.
            </p>
            <p>
              If you reject the step, the task transitions to <code>CANCELLED</code> and subsequent operations are aborted.
            </p>
          </CardContent>
        </Card>

        {/* Knowledge & RAG Citations */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-sky-400" />
              3. Knowledge Base & Grounded Retrieval
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6 space-y-3 text-xs text-muted-foreground leading-relaxed">
            <p>
              Upload documents in PDF, Markdown, or text format in the <strong>Knowledge Base</strong>. ContextPilot AI breaks documents into overlapping chunks with page metadata. When you ask questions:
            </p>
            <ul className="list-disc pl-5 space-y-1">
              <li>Verified facts are cited with the document name and exact page number.</li>
              <li>If no relevant evidence exists, the agent explicitly reports insufficient evidence rather than hallucinating answers.</li>
            </ul>
          </CardContent>
        </Card>

        {/* AWS Bedrock Configuration */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <Cpu className="w-5 h-5 text-purple-400" />
              4. Amazon Bedrock Configuration (Optional)
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6 space-y-3 text-xs text-muted-foreground leading-relaxed">
            <p>
              By default, ContextPilot AI runs in <strong>Local Demo Mode</strong> with zero external credentials required. To connect genuine Amazon Bedrock models:
            </p>
            <div className="p-3 rounded-lg bg-background border border-border font-mono text-[11px] space-y-1 text-sky-400">
              <p>LLM_PROVIDER=bedrock</p>
              <p>AWS_REGION=us-east-1</p>
              <p>AWS_ACCESS_KEY_ID=your_access_key</p>
              <p>AWS_SECRET_ACCESS_KEY=your_secret_key</p>
              <p>BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0</p>
            </div>
            <p>
              Verify your Bedrock connection anytime in <strong>Settings → Integrations & AWS</strong>.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
