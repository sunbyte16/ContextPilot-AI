import React from 'react';
import { Link } from 'react-router-dom';
import { Bot, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/Button';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4 text-center">
      <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-4 border border-indigo-500/20">
        <Bot className="w-8 h-8" />
      </div>
      <h1 className="text-4xl font-extrabold text-foreground mb-2">404</h1>
      <h2 className="text-base font-semibold text-foreground mb-2">Page Not Found</h2>
      <p className="text-xs text-muted-foreground max-w-sm mb-6">
        The requested path does not exist in the ContextPilot AI application routes.
      </p>
      <Link to="/app">
        <Button variant="primary" size="sm" icon={<ArrowLeft className="w-4 h-4" />}>
          Return to Dashboard
        </Button>
      </Link>
    </div>
  );
};
