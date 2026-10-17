import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Settings,
  User,
  Cpu,
  Shield,
  Trash2,
  Download,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Sparkles,
  Layers,
  Activity,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { UserPreference, IntegrationStatus } from '../types';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Input } from '../components/ui/Input';

export const SettingsPage: React.FC = () => {
  const { user, logout, refreshUser } = useAuth();
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState<'profile' | 'assistant' | 'integrations' | 'privacy'>('profile');
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [preferences, setPreferences] = useState<UserPreference | null>(null);
  const [integrations, setIntegrations] = useState<IntegrationStatus[]>([]);
  const [testingInteg, setTestingInteg] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const fetchData = async () => {
    try {
      const [prefRes, integRes] = await Promise.all([
        api.get<UserPreference>('/settings/preferences'),
        api.get<{ integrations: IntegrationStatus[] }>('/settings/integrations'),
      ]);
      setPreferences(prefRes);
      setIntegrations(integRes.integrations || []);
    } catch {
      // Handled
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      await api.put('/auth/me', { full_name: fullName });
      await refreshUser();
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 2500);
    } catch (err: any) {
      alert(`Profile update failed: ${err.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  const handleSavePreferences = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!preferences) return;
    setIsSaving(true);
    try {
      const updated = await api.put<UserPreference>('/settings/preferences', {
        preferred_model: preferences.preferred_model,
        response_style: preferences.response_style,
        memory_enabled: preferences.memory_enabled,
        default_approval_behavior: preferences.default_approval_behavior,
        execution_timeout_seconds: preferences.execution_timeout_seconds,
      });
      setPreferences(updated);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 2500);
    } catch (err: any) {
      alert(`Preferences update failed: ${err.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  const handleTestIntegration = async (provider: string) => {
    setTestingInteg(provider);
    try {
      const res = await api.post<any>(`/settings/integrations/test?provider_name=${provider}`);
      alert(`Integration Test [${provider}]: ${res.status}\n${res.details || ''}`);
      await fetchData();
    } catch (err: any) {
      alert(`Test error: ${err.message}`);
    } finally {
      setTestingInteg(null);
    }
  };

  const handleResetData = async () => {
    if (!confirm('Reset all demo data and clean workspace state?')) return;
    try {
      await api.post('/demo/reset');
      alert('All workspace tasks, conversations, memories, and documents have been reset.');
      navigate('/app');
    } catch (err: any) {
      alert(`Reset failed: ${err.message}`);
    }
  };

  const handleDeleteAccount = async () => {
    if (!confirm('DANGER: Are you completely sure you want to permanently delete your account and all associated tenant data?')) return;
    try {
      await api.delete('/auth/me');
      await logout();
      navigate('/login');
    } catch (err: any) {
      alert(`Account deletion failed: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
          <Settings className="w-6 h-6 text-primary" />
          Settings & Configuration
        </h1>
        <p className="text-xs text-muted-foreground mt-0.5">
          Manage your account profile, AI provider selection, and privacy controls
        </p>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-border/70 gap-2 overflow-x-auto pb-1">
        {[
          { id: 'profile', label: 'User Profile', icon: User },
          { id: 'assistant', label: 'Assistant Preferences', icon: Cpu },
          { id: 'integrations', label: 'Integrations & AWS', icon: Activity },
          { id: 'privacy', label: 'Privacy & Data', icon: Shield },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-t-lg text-xs font-semibold border-b-2 transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-primary text-primary bg-primary/5'
                  : 'border-transparent text-muted-foreground hover:text-foreground'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Profile Tab */}
      {activeTab === 'profile' && (
        <Card className="max-w-2xl">
          <CardHeader>
            <CardTitle>Profile Details</CardTitle>
            <p className="text-xs text-muted-foreground">Personal information and tenant identity</p>
          </CardHeader>
          <CardContent className="p-6">
            <form onSubmit={handleSaveProfile} className="space-y-4">
              <Input
                label="Full Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />

              <Input
                label="Email Address"
                value={user?.email || ''}
                disabled
                helperText="Email cannot be changed directly in demo mode."
              />

              <div className="pt-2 flex items-center justify-between">
                {saveSuccess && (
                  <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4" /> Profile saved successfully!
                  </span>
                )}
                <Button type="submit" variant="primary" size="sm" isLoading={isSaving} className="ml-auto">
                  Save Changes
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Assistant Preferences Tab */}
      {activeTab === 'assistant' && preferences && (
        <Card className="max-w-2xl">
          <CardHeader>
            <CardTitle>Assistant Reasoning & Execution Preferences</CardTitle>
            <p className="text-xs text-muted-foreground">
              Customize how the agent orchestrator formulates plans and triggers tools
            </p>
          </CardHeader>
          <CardContent className="p-6">
            <form onSubmit={handleSavePreferences} className="space-y-5">
              <div>
                <label className="block text-xs font-medium text-foreground tracking-wide mb-1.5">
                  Inference Provider
                </label>
                <select
                  value={preferences.preferred_model}
                  onChange={(e) => setPreferences({ ...preferences, preferred_model: e.target.value })}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
                >
                  <option value="local-demo">Deterministic Local Demo Engine (Offline / Zero-Cost)</option>
                  <option value="bedrock">Amazon Bedrock (Claude 3 Sonnet / Titan)</option>
                </select>
                <p className="text-[11px] text-muted-foreground mt-1">
                  Local demo mode runs completely offline without requiring paid AWS credentials.
                </p>
              </div>

              <div>
                <label className="block text-xs font-medium text-foreground tracking-wide mb-1.5">
                  Response Style
                </label>
                <select
                  value={preferences.response_style}
                  onChange={(e) => setPreferences({ ...preferences, response_style: e.target.value })}
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
                >
                  <option value="concise">Concise (Direct answers & steps)</option>
                  <option value="precise">Precise (Evidence-grounded with citations)</option>
                  <option value="detailed">Detailed (Comprehensive explanations)</option>
                </select>
              </div>

              <div className="pt-2">
                <label className="flex items-center gap-2 cursor-pointer text-xs text-foreground">
                  <input
                    type="checkbox"
                    checked={preferences.memory_enabled}
                    onChange={(e) => setPreferences({ ...preferences, memory_enabled: e.target.checked })}
                    className="rounded border-border text-primary focus:ring-primary"
                  />
                  <span>Inject active context memories into agent prompt assembly</span>
                </label>
              </div>

              <div className="pt-2 flex items-center justify-between">
                {saveSuccess && (
                  <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4" /> Preferences saved!
                  </span>
                )}
                <Button type="submit" variant="primary" size="sm" isLoading={isSaving} className="ml-auto">
                  Save Preferences
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Integrations Tab */}
      {activeTab === 'integrations' && (
        <div className="space-y-4 max-w-3xl">
          <Card>
            <CardHeader>
              <CardTitle>Connected Ecosystem Adapters</CardTitle>
              <p className="text-xs text-muted-foreground">
                Inspect connectivity status of local reasoning engines, Amazon Bedrock, and ambient web simulation
              </p>
            </CardHeader>
            <CardContent className="p-6 space-y-4">
              {integrations.map((integ, i) => (
                <div
                  key={i}
                  className="p-4 rounded-xl border border-border/80 bg-background/50 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-foreground">{integ.name}</span>
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
                    <p className="text-xs text-muted-foreground">{integ.details}</p>
                    <span className="text-[10px] text-slate-500 font-mono block">
                      Provider ID: {integ.provider} {integ.latency_ms !== undefined && `• Latency: ${integ.latency_ms}ms`}
                    </span>
                  </div>

                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleTestIntegration(integ.provider)}
                    isLoading={testingInteg === integ.provider}
                  >
                    Test Connection
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      )}

      {/* Privacy & Data Management Tab */}
      {activeTab === 'privacy' && (
        <div className="space-y-6 max-w-2xl">
          <Card>
            <CardHeader>
              <CardTitle>Data Sovereignty & Reset</CardTitle>
              <p className="text-xs text-muted-foreground">
                Exercise your data rights: reset demo workflows or permanently delete your account
              </p>
            </CardHeader>
            <CardContent className="p-6 space-y-5">
              <div className="p-4 rounded-xl border border-border bg-background/50 flex items-center justify-between gap-4">
                <div>
                  <h4 className="text-xs font-bold text-foreground">Reset Demo Data</h4>
                  <p className="text-xs text-muted-foreground">
                    Removes all tasks, conversations, memories, and documents for a clean slate.
                  </p>
                </div>
                <Button variant="outline" size="sm" onClick={handleResetData} icon={<RotateCcw className="w-3.5 h-3.5" />}>
                  Reset All Data
                </Button>
              </div>

              <div className="p-4 rounded-xl border border-rose-500/30 bg-rose-500/5 flex items-center justify-between gap-4">
                <div>
                  <h4 className="text-xs font-bold text-rose-400">Delete Account & Data</h4>
                  <p className="text-xs text-muted-foreground">
                    Permanently purges your user identity, credentials, and all database records.
                  </p>
                </div>
                <Button variant="destructive" size="sm" onClick={handleDeleteAccount} icon={<Trash2 className="w-3.5 h-3.5" />}>
                  Delete Account
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
