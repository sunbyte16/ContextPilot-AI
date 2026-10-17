import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  TrendingUp,
  Activity,
  CheckCircle2,
  Clock,
  Layers,
  Wrench,
  ShieldAlert,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';
import { api } from '../services/api';
import { AnalyticsSummary } from '../types';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

export const AnalyticsPage: React.FC = () => {
  const [data, setData] = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const res = await api.get<AnalyticsSummary>('/analytics/summary');
        setData(res);
      } catch {
        // Handled
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  const COLORS = ['#10b981', '#f59e0b', '#6366f1', '#f43f5e', '#64748b'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-primary" />
            Execution Metrics & Analytics
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Measured runtime metrics computed from persistent database records
          </p>
        </div>

        <Badge variant="purple" size="md">
          {data?.success_rate_percentage ?? 100}% Verification Rate
        </Badge>
      </div>

      {/* Stats Cards Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 space-y-1">
            <span className="text-[11px] text-muted-foreground font-medium flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Verified Success Rate
            </span>
            <p className="text-2xl font-extrabold text-foreground">{data?.success_rate_percentage ?? 100}%</p>
            <p className="text-[10px] text-slate-500">
              {data?.completed_tasks ?? 0} completed / {data?.total_tasks ?? 0} total
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 space-y-1">
            <span className="text-[11px] text-muted-foreground font-medium flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-sky-400" />
              Avg Tool Latency
            </span>
            <p className="text-2xl font-extrabold text-foreground">{data?.average_execution_time_ms ?? 0} ms</p>
            <p className="text-[10px] text-slate-500">Across sandboxed dispatchers</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 space-y-1">
            <span className="text-[11px] text-muted-foreground font-medium flex items-center gap-1.5">
              <Wrench className="w-4 h-4 text-indigo-400" />
              Tool Invocations
            </span>
            <p className="text-2xl font-extrabold text-foreground">{data?.total_tool_executions ?? 0}</p>
            <p className="text-[10px] text-slate-500">Registered tool executions</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 space-y-1">
            <span className="text-[11px] text-muted-foreground font-medium flex items-center gap-1.5">
              <ShieldAlert className="w-4 h-4 text-amber-400" />
              Pending Approvals
            </span>
            <p className="text-2xl font-extrabold text-foreground">{data?.pending_approvals ?? 0}</p>
            <p className="text-[10px] text-slate-500">Awaiting human sign-off</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Daily Workflow Trends */}
        <Card>
          <CardHeader className="py-4">
            <CardTitle className="text-sm font-semibold">7-Day Task Completion Trend</CardTitle>
            <p className="text-xs text-muted-foreground">Workflows created and completed per day</p>
          </CardHeader>
          <CardContent className="p-4 h-64">
            {data?.recent_trend && data.recent_trend.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.recent_trend}>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                  <XAxis dataKey="date" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} allowDecimals={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      borderColor: '#1e293b',
                      borderRadius: '8px',
                      fontSize: '12px',
                    }}
                  />
                  <Bar dataKey="completed" fill="#10b981" name="Completed" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="created" fill="#6366f1" name="Created" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-muted-foreground">
                No trend data available.
              </div>
            )}
          </CardContent>
        </Card>

        {/* Tool Usage Frequency */}
        <Card>
          <CardHeader className="py-4">
            <CardTitle className="text-sm font-semibold">Tool Usage Frequency</CardTitle>
            <p className="text-xs text-muted-foreground">Invocations per registered tool</p>
          </CardHeader>
          <CardContent className="p-4 h-64">
            {data?.tool_usage && data.tool_usage.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.tool_usage} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                  <XAxis type="number" stroke="#94a3b8" fontSize={11} allowDecimals={false} />
                  <YAxis dataKey="tool_name" type="category" stroke="#94a3b8" fontSize={10} width={90} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      borderColor: '#1e293b',
                      borderRadius: '8px',
                      fontSize: '12px',
                    }}
                  />
                  <Bar dataKey="invocations" fill="#818cf8" name="Invocations" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-muted-foreground">
                No tool invocation data.
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Status Distribution */}
      <Card>
        <CardHeader className="py-4">
          <CardTitle className="text-sm font-semibold">Workflow Status Breakdown</CardTitle>
          <p className="text-xs text-muted-foreground">Current state distribution across all pipeline tasks</p>
        </CardHeader>
        <CardContent className="p-4 flex flex-wrap gap-4 items-center justify-around">
          {data?.status_distribution.map((st, i) => (
            <div key={st.status} className="p-4 rounded-xl border border-border/70 bg-card min-w-[140px] text-center">
              <span className="text-[11px] font-bold text-muted-foreground font-mono block mb-1">
                {st.status.replace('_', ' ')}
              </span>
              <span className="text-2xl font-extrabold text-foreground">{st.count}</span>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
};
