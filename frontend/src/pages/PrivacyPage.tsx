import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Shield, Lock, Trash2, Database, Eye } from 'lucide-react';
import { Button } from '../components/ui/Button';

export const PrivacyPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-background text-foreground py-12 px-4 sm:px-6 max-w-4xl mx-auto">
      <Link to="/" className="inline-flex items-center gap-2 text-xs font-semibold text-primary hover:underline mb-8">
        <ArrowLeft className="w-4 h-4" />
        Back to Home
      </Link>

      <div className="bg-card border border-border rounded-2xl p-8 sm:p-12 shadow-sm">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-foreground">Privacy Policy & Security Notice</h1>
            <p className="text-xs text-muted-foreground">ContextPilot AI Platform Transparency & User Controls</p>
          </div>
        </div>

        <div className="prose prose-invert max-w-none text-xs sm:text-sm text-muted-foreground space-y-6 leading-relaxed">
          <section>
            <h2 className="text-base font-semibold text-foreground flex items-center gap-2 mb-2">
              <Database className="w-4 h-4 text-sky-400" /> 1. Data Isolation & Storage
            </h2>
            <p>
              ContextPilot AI isolates user data strictly by account tenant ID. Your tasks, conversation histories, context memories, uploaded documents, and audit logs are scoped exclusively to your authenticated identity. Cross-user access is blocked at the database query level on the backend.
            </p>
          </section>

          <section>
            <h2 className="text-base font-semibold text-foreground flex items-center gap-2 mb-2">
              <Lock className="w-4 h-4 text-emerald-400" /> 2. Model Inference & AI Providers
            </h2>
            <p>
              When running in <strong>Local Demo Mode</strong>, all reasoning and plan generation occurs 100% locally on your machine with zero external network transmission. When configured with <strong>Amazon Bedrock</strong>, prompt messages and knowledge excerpts are passed through your configured AWS IAM credentials to the specified model runtime. No data is sold or used for model training without your explicit authorization.
            </p>
          </section>

          <section>
            <h2 className="text-base font-semibold text-foreground flex items-center gap-2 mb-2">
              <Eye className="w-4 h-4 text-amber-400" /> 3. Redaction & Credential Hygiene
            </h2>
            <p>
              All tool invocation logs and telemetry automatically redact sensitive keys such as passwords, API tokens, and authorization headers before persistence. Server secrets are maintained in environment variables and never surfaced in frontend API responses.
            </p>
          </section>

          <section>
            <h2 className="text-base font-semibold text-foreground flex items-center gap-2 mb-2">
              <Trash2 className="w-4 h-4 text-rose-400" /> 4. User Deletion Rights
            </h2>
            <p>
              You maintain total control over stored context. You can selectively edit or delete individual memories, clear conversation histories, delete uploaded documents, or delete your entire account and all associated databases with a single button in <strong>Settings</strong>.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
};
