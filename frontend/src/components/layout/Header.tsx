import React, { useState, useEffect } from 'react';
import {
  Menu,
  Sun,
  Moon,
  Bell,
  Sparkles,
  Cpu,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { api } from '../../services/api';
import { NotificationItem } from '../../types';
import { Button } from '../ui/Button';

interface HeaderProps {
  onToggleSidebar: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onToggleSidebar }) => {
  const { theme, toggleTheme } = useTheme();
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [showNotifications, setShowNotifications] = useState<boolean>(false);
  const [isSeeding, setIsSeeding] = useState<boolean>(false);
  const [seedSuccess, setSeedSuccess] = useState<boolean>(false);

  const fetchNotifications = async () => {
    try {
      const data = await api.get<NotificationItem[]>('/activity/notifications');
      setNotifications(data || []);
    } catch {
      // Ignore
    }
  };

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleSeedDemo = async () => {
    setIsSeeding(true);
    setSeedSuccess(false);
    try {
      await api.post('/demo/seed');
      setSeedSuccess(true);
      fetchNotifications();
      setTimeout(() => setSeedSuccess(false), 3000);
      window.location.reload();
    } catch (e: any) {
      alert(`Error seeding demo data: ${e.message}`);
    } finally {
      setIsSeeding(false);
    }
  };

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return (
    <header className="h-16 bg-card/80 backdrop-blur-md border-b border-border/70 sticky top-0 z-30 px-4 sm:px-6 flex items-center justify-between">
      {/* Left: Mobile Toggle & Simulation Badge */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted lg:hidden"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs">
          <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
          <span className="font-semibold">Alexa+ Simulation Mode</span>
          <span className="text-muted-foreground/60">|</span>
          <span className="text-muted-foreground text-[11px]">Web-Based Assistant</span>
        </div>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-2.5">
        {/* Seed Demo Button */}
        <Button
          variant={seedSuccess ? 'success' : 'outline'}
          size="sm"
          onClick={handleSeedDemo}
          isLoading={isSeeding}
          icon={seedSuccess ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Sparkles className="w-3.5 h-3.5 text-amber-400" />}
        >
          {seedSuccess ? 'Demo Seeded!' : 'Seed Demo Data'}
        </Button>

        {/* Notifications Popover Toggle */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted relative transition-colors"
            title="Notifications"
          >
            <Bell className="w-4 h-4" />
            {unreadCount > 0 && (
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-rose-500 ring-2 ring-card" />
            )}
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 bg-card border border-border rounded-xl shadow-xl z-50 overflow-hidden animate-in fade-in zoom-in-95">
              <div className="p-3 border-b border-border flex items-center justify-between">
                <span className="text-xs font-semibold text-foreground">Workspace Alerts</span>
                <span className="text-[10px] text-muted-foreground">{notifications.length} total</span>
              </div>
              <div className="max-h-64 overflow-y-auto divide-y divide-border/40">
                {notifications.length === 0 ? (
                  <div className="p-4 text-center text-xs text-muted-foreground">
                    No active notifications.
                  </div>
                ) : (
                  notifications.map((n) => (
                    <div key={n.id} className="p-3 hover:bg-muted/40 transition-colors">
                      <p className="text-xs font-semibold text-foreground">{n.title}</p>
                      <p className="text-[11px] text-muted-foreground mt-0.5 line-clamp-2">{n.message}</p>
                      <p className="text-[10px] text-slate-500 mt-1">
                        {new Date(n.created_at).toLocaleTimeString()}
                      </p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-300" /> : <Moon className="w-4 h-4 text-slate-700" />}
        </button>
      </div>
    </header>
  );
};
