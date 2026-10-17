import React, { useState, useEffect } from 'react';
import {
  Activity,
  Bell,
  Shield,
  Clock,
  CheckCircle2,
  AlertTriangle,
  Layers,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import { api } from '../services/api';
import { AuditEvent, NotificationItem } from '../types';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';

export const ActivityPage: React.FC = () => {
  const [tab, setTab] = useState<'audit' | 'notifications'>('audit');
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([]);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedAuditId, setExpandedAuditId] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [auditRes, notifRes] = await Promise.all([
        api.get<AuditEvent[]>('/activity/audit'),
        api.get<NotificationItem[]>('/activity/notifications'),
      ]);
      setAuditEvents(auditRes || []);
      setNotifications(notifRes || []);
    } catch {
      // Handled
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleMarkAllRead = async () => {
    try {
      await api.post('/activity/notifications/read-all');
      setNotifications(notifications.map((n) => ({ ...n, is_read: true })));
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    }
  };

  const toggleAuditExpand = (id: string) => {
    setExpandedAuditId(expandedAuditId === id ? null : id);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
            <Activity className="w-6 h-6 text-primary" />
            Activity, Audit & Notification Stream
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Immutable audit records and real-time execution alerts
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center gap-1.5 p-1 bg-card border border-border rounded-xl">
          <button
            onClick={() => setTab('audit')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              tab === 'audit'
                ? 'bg-primary text-primary-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            Audit Trail ({auditEvents.length})
          </button>
          <button
            onClick={() => setTab('notifications')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              tab === 'notifications'
                ? 'bg-primary text-primary-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            Notifications ({notifications.filter((n) => !n.is_read).length} unread)
          </button>
        </div>
      </div>

      {/* Content */}
      {tab === 'audit' ? (
        <Card>
          <CardHeader className="py-4 flex flex-row items-center justify-between">
            <div>
              <CardTitle>System & Agent Audit Events</CardTitle>
              <p className="text-xs text-muted-foreground mt-0.5">
                Every tool execution, approval decision, and security change is logged
              </p>
            </div>
            <Badge variant="outline" size="sm">
              Tamper-Evident DB Log
            </Badge>
          </CardHeader>
          <CardContent className="p-0 divide-y divide-border/40">
            {auditEvents.length === 0 ? (
              <div className="p-12 text-center text-xs text-muted-foreground">
                No audit events recorded yet.
              </div>
            ) : (
              auditEvents.map((ev) => (
                <div key={ev.id} className="p-4 hover:bg-muted/30 transition-colors">
                  <div className="flex items-start justify-between gap-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <Badge
                          variant={
                            ev.event_type.includes('APPROVED')
                              ? 'success'
                              : ev.event_type.includes('REJECTED')
                              ? 'danger'
                              : ev.event_type.includes('TOOL')
                              ? 'purple'
                              : 'default'
                          }
                          size="sm"
                        >
                          {ev.event_type}
                        </Badge>
                        <span className="text-xs font-semibold text-foreground font-mono">
                          {ev.action}
                        </span>
                      </div>
                      <p className="text-[11px] text-muted-foreground">
                        Resource: <span className="font-mono text-foreground">{ev.resource_type || 'system'}</span>
                      </p>
                    </div>

                    <div className="flex items-center gap-3">
                      <span className="text-[10px] text-muted-foreground font-mono whitespace-nowrap">
                        {new Date(ev.created_at).toLocaleString()}
                      </span>
                      {ev.details && Object.keys(ev.details).length > 0 && (
                        <button
                          onClick={() => toggleAuditExpand(ev.id)}
                          className="p-1 rounded text-muted-foreground hover:text-foreground"
                        >
                          {expandedAuditId === ev.id ? (
                            <ChevronUp className="w-4 h-4" />
                          ) : (
                            <ChevronDown className="w-4 h-4" />
                          )}
                        </button>
                      )}
                    </div>
                  </div>

                  {expandedAuditId === ev.id && ev.details && (
                    <div className="mt-3 p-3 rounded-lg bg-background border border-border/70 text-xs font-mono text-sky-400 overflow-x-auto">
                      <pre>{JSON.stringify(ev.details, null, 2)}</pre>
                    </div>
                  )}
                </div>
              ))
            )}
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader className="py-4 flex flex-row items-center justify-between">
            <div>
              <CardTitle>In-App Workspace Notifications</CardTitle>
              <p className="text-xs text-muted-foreground mt-0.5">Alerts dispatched from agent workflows</p>
            </div>
            {notifications.some((n) => !n.is_read) && (
              <Button size="sm" variant="outline" onClick={handleMarkAllRead}>
                Mark All as Read
              </Button>
            )}
          </CardHeader>
          <CardContent className="p-0 divide-y divide-border/40">
            {notifications.length === 0 ? (
              <div className="p-12 text-center text-xs text-muted-foreground">
                No notifications recorded.
              </div>
            ) : (
              notifications.map((n) => (
                <div
                  key={n.id}
                  className={`p-4 flex items-start justify-between gap-4 transition-colors ${
                    n.is_read ? 'bg-card' : 'bg-primary/5'
                  }`}
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <Badge
                        variant={
                          n.notification_type === 'APPROVAL_REQUIRED'
                            ? 'warning'
                            : n.notification_type === 'TASK_COMPLETED'
                            ? 'success'
                            : 'info'
                        }
                        size="sm"
                      >
                        {n.notification_type}
                      </Badge>
                      <h4 className="text-xs font-bold text-foreground">{n.title}</h4>
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed">{n.message}</p>
                    <span className="text-[10px] text-slate-500 font-mono block pt-1">
                      {new Date(n.created_at).toLocaleString()}
                    </span>
                  </div>

                  {!n.is_read && (
                    <span className="w-2 h-2 rounded-full bg-primary flex-shrink-0 mt-1" />
                  )}
                </div>
              ))
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};
