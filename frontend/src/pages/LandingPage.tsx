import React from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  Bot,
  ShieldCheck,
  Zap,
  BookOpen,
  ArrowRight,
  CheckCircle2,
  Terminal,
  Activity,
  Workflow,
  Lock,
  Cpu,
} from 'lucide-react';
import { Button } from '../components/ui/Button';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col selection:bg-indigo-500/20">
      {/* Top Navigation */}
      <header className="border-b border-border/60 bg-card/60 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-400 via-indigo-500 to-purple-500 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
              <Sparkles className="w-5 h-5" />
            </div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-base tracking-tight text-foreground">ContextPilot</span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                AI
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Link to="/login">
              <Button variant="ghost" size="sm">
                Sign In
              </Button>
            </Link>
            <Link to="/register">
              <Button variant="primary" size="sm" icon={<ArrowRight className="w-4 h-4" />}>
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 sm:py-28 px-4 text-center max-w-5xl mx-auto relative overflow-hidden">
        {/* Subtle background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-6">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Amazon Developer Hackathon | Production Agentic AI Platform</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-foreground leading-[1.15]">
          Understand Goals. Plan Steps. <br />
          <span className="bg-gradient-to-r from-sky-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
            Execute Approved Actions with Proof.
          </span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          An Alexa+-inspired ambient agentic assistant that decomposes natural-language objectives into transparent plans, connects sandboxed tools, enforces server-side human approval for sensitive operations, and verifies real outputs.
        </p>

        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <Link to="/register">
            <Button size="lg" icon={<Zap className="w-4 h-4 text-amber-300" />}>
              Launch AI Workspace
            </Button>
          </Link>
          <Link to="/login">
            <Button variant="outline" size="lg">
              Explore Demo Environment
            </Button>
          </Link>
        </div>

        {/* Live Simulation Notice */}
        <div className="mt-6 text-xs text-muted-foreground/80 max-w-lg mx-auto bg-muted/40 p-2.5 rounded-lg border border-border/40">
          <span className="font-semibold text-foreground">Hackathon Disclosure:</span> ContextPilot AI is built as a web-based ambient assistant simulation inspired by Alexa+. It runs offline locally with zero paid API dependencies and includes an Amazon Bedrock adapter.
        </div>
      </section>

      {/* Interactive 5-Step Agent Loop Visualizer */}
      <section className="py-12 px-4 max-w-6xl mx-auto w-full">
        <div className="text-center mb-10">
          <h2 className="text-2xl font-bold text-foreground">The Verifiable Agentic Lifecycle</h2>
          <p className="text-xs text-muted-foreground mt-1">Never hallucinates execution. Every step is validated, approved, and logged.</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {[
            {
              step: '01',
              title: 'Objective Intent',
              desc: 'Parses goal, evaluates active context memories & uploaded documents.',
              icon: Bot,
              color: 'text-sky-400',
            },
            {
              step: '02',
              title: 'Structured Plan',
              desc: 'Decomposes objective into ordered steps mapped to registered tools.',
              icon: Workflow,
              color: 'text-indigo-400',
            },
            {
              step: '03',
              title: 'Human Approval',
              desc: 'Server-side gate stops execution for consequential actions until approved.',
              icon: ShieldCheck,
              color: 'text-amber-400',
            },
            {
              step: '04',
              title: 'Sandboxed Tools',
              desc: 'Executes AST calculator, tabular analysis, RAG, and export utilities.',
              icon: Terminal,
              color: 'text-purple-400',
            },
            {
              step: '05',
              title: 'Audit & Outcome',
              desc: 'Verifies real returned outputs against expected outcome schemas.',
              icon: Activity,
              color: 'text-emerald-400',
            },
          ].map((item, idx) => {
            const Icon = item.icon;
            return (
              <div
                key={idx}
                className="bg-card border border-border rounded-xl p-5 relative overflow-hidden flex flex-col justify-between hover:border-indigo-500/40 transition-all shadow-sm"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-mono font-bold text-muted-foreground">{item.step}</span>
                    <Icon className={`w-5 h-5 ${item.color}`} />
                  </div>
                  <h3 className="text-sm font-semibold text-foreground mb-1">{item.title}</h3>
                  <p className="text-xs text-muted-foreground leading-relaxed">{item.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Core Capabilities */}
      <section className="py-16 px-4 bg-muted/20 border-y border-border/60">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold text-foreground">Production-Ready Architecture</h2>
            <p className="text-xs sm:text-sm text-muted-foreground mt-2 max-w-xl mx-auto">
              Engineered with full-stack fidelity: FastAPI backend, strict tenant isolation, Pydantic v2 schemas, and persistent SQLite/PostgreSQL storage.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-card border border-border rounded-xl p-6 shadow-sm">
              <div className="w-10 h-10 rounded-lg bg-sky-500/10 text-sky-400 flex items-center justify-center mb-4 border border-sky-500/20">
                <Cpu className="w-5 h-5" />
              </div>
              <h3 className="text-base font-semibold text-foreground mb-2">Amazon Bedrock & Local Engine</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Seamlessly toggle between our deterministic offline local demo provider and real AWS Bedrock Converse API for live model reasoning.
              </p>
            </div>

            <div className="bg-card border border-border rounded-xl p-6 shadow-sm">
              <div className="w-10 h-10 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-4 border border-indigo-500/20">
                <Lock className="w-5 h-5" />
              </div>
              <h3 className="text-base font-semibold text-foreground mb-2">Server-Side Safety Gates</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Approval enforcement is hardwired in the backend execution engine. AI agents cannot bypass human sign-off for consequential operations.
              </p>
            </div>

            <div className="bg-card border border-border rounded-xl p-6 shadow-sm">
              <div className="w-10 h-10 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center mb-4 border border-purple-500/20">
                <BookOpen className="w-5 h-5" />
              </div>
              <h3 className="text-base font-semibold text-foreground mb-2">Grounded RAG with Citations</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Upload PDFs and markdown docs. The retriever quotes exact source snippets and page numbers, explicitly acknowledging when evidence is insufficient.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-border/60 bg-card/40 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-foreground">ContextPilot AI</span>
            <span>© 2026 Amazon Developer Hackathon Submission.</span>
          </div>
          <div className="flex items-center gap-6">
            <Link to="/privacy" className="hover:text-foreground transition-colors">
              Privacy Policy
            </Link>
            <Link to="/terms" className="hover:text-foreground transition-colors">
              Terms of Use
            </Link>
            <a
              href="https://aws.amazon.com/bedrock/"
              target="_blank"
              rel="noreferrer"
              className="hover:text-foreground transition-colors"
            >
              Amazon Bedrock Docs
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
};
