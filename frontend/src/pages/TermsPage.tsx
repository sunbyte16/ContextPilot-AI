import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, FileText, CheckCircle, AlertTriangle } from 'lucide-react';

export const TermsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-background text-foreground py-12 px-4 sm:px-6 max-w-4xl mx-auto">
      <Link to="/" className="inline-flex items-center gap-2 text-xs font-semibold text-primary hover:underline mb-8">
        <ArrowLeft className="w-4 h-4" />
        Back to Home
      </Link>

      <div className="bg-card border border-border rounded-2xl p-8 sm:p-12 shadow-sm">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-foreground">Terms of Use & Hackathon Constraints</h1>
            <p className="text-xs text-muted-foreground">ContextPilot AI Platform Usage Guidelines</p>
          </div>
        </div>

        <div className="prose prose-invert max-w-none text-xs sm:text-sm text-muted-foreground space-y-6 leading-relaxed">
          <section>
            <h2 className="text-base font-semibold text-foreground flex items-center gap-2 mb-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" /> 1. Alexa+ Simulation Disclosure
            </h2>
            <p>
              ContextPilot AI is submitted to the Amazon Developer Hackathon as an Alexa+-inspired simulated web application. This application does not claim to be the official Alexa+ product, an official Amazon Alexa+ integration, or a certified Alexa+ implementation. The application runs on standard developer computers and does not require Echo devices, Fire TV, Bee wearables, or Ring devices.
            </p>
          </section>

          <section>
            <h2 className="text-base font-semibold text-foreground flex items-center gap-2 mb-2">
              <CheckCircle className="w-4 h-4 text-emerald-400" /> 2. Safe Tool Execution
            </h2>
            <p>
              Tools registered in ContextPilot AI execute within controlled python dispatchers. The platform strictly prohibits arbitrary code execution, dynamic eval, shell command execution, or uncontrolled host access. Consequential actions require explicit human approval via server-side gates.
            </p>
          </section>

          <section>
            <h2 className="text-base font-semibold text-foreground flex items-center gap-2 mb-2">
              <FileText className="w-4 h-4 text-sky-400" /> 3. Grounded Outputs & Verifiable Results
            </h2>
            <p>
              The platform is designed to report verifiable outcomes from executed tools rather than fabricating simulated success. Users must review plan steps before granting approvals.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
};
