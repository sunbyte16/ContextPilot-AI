import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import {
  Bot,
  Send,
  Plus,
  Trash2,
  Edit2,
  Sparkles,
  BookOpen,
  ArrowRight,
  ShieldAlert,
  Copy,
  Check,
  Cpu,
  Layers,
  ExternalLink,
} from 'lucide-react';
import { api } from '../services/api';
import { Conversation, Message, Citation } from '../types';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';

export const AssistantPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConvId, setCurrentConvId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedMsgId, setCopiedMsgId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      const data = await api.get<Conversation[]>('/conversations/');
      setConversations(data || []);
      if (!currentConvId && data && data.length > 0) {
        setCurrentConvId(data[0].id);
      }
    } catch {
      // Handled
    }
  };

  const loadMessages = async (convId: string) => {
    try {
      const data = await api.get<{ messages: Message[] }>(`/conversations/${convId}`);
      setMessages(data.messages || []);
      setTimeout(scrollToBottom, 100);
    } catch {
      // Handled
    }
  };

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    if (currentConvId) {
      loadMessages(currentConvId);
    }
  }, [currentConvId]);

  // Handle initial prompt passed from Dashboard
  useEffect(() => {
    const initialPrompt = (location.state as any)?.initialPrompt;
    if (initialPrompt && !isLoading) {
      handleSendMessage(initialPrompt);
      // Clear location state
      window.history.replaceState({}, document.title);
    }
  }, [location.state]);

  const handleCreateNewConversation = async () => {
    try {
      const newConv = await api.post<Conversation>('/conversations/', {
        title: 'New Conversation',
      });
      setConversations([newConv, ...conversations]);
      setCurrentConvId(newConv.id);
      setMessages([]);
    } catch {
      // Handled
    }
  };

  const handleDeleteConversation = async (convId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await api.delete(`/conversations/${convId}`);
      const remaining = conversations.filter((c) => c.id !== convId);
      setConversations(remaining);
      if (currentConvId === convId) {
        setCurrentConvId(remaining.length > 0 ? remaining[0].id : null);
        setMessages([]);
      }
    } catch {
      // Handled
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend || inputText;
    if (!text.trim() || isLoading) return;

    setInputText('');
    setIsLoading(true);

    // Optimistic user message
    const tempId = 'temp-' + Date.now();
    const optimisticUserMsg: Message = {
      id: tempId,
      conversation_id: currentConvId || '',
      sender: 'user',
      content: text,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, optimisticUserMsg]);
    setTimeout(scrollToBottom, 50);

    try {
      let targetConvId = currentConvId;
      if (!targetConvId) {
        const newConv = await api.post<Conversation>('/conversations/', {
          title: text.slice(0, 30),
        });
        targetConvId = newConv.id;
        setCurrentConvId(newConv.id);
        setConversations([newConv, ...conversations]);
      }

      const res = await api.post<any>(`/conversations/${targetConvId}/messages`, {
        content: text,
      });

      // Reload full conversation history to ensure verified message persistence
      await loadMessages(targetConvId);
      await loadConversations();
    } catch (e: any) {
      alert(`Message dispatch failed: ${e.message}`);
    } finally {
      setIsLoading(false);
      setTimeout(scrollToBottom, 100);
    }
  };

  const handleCopyMessage = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedMsgId(id);
    setTimeout(() => setCopiedMsgId(null), 2000);
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex gap-4 overflow-hidden">
      {/* Left Conversations Sidebar */}
      <div className="w-64 bg-card border border-border rounded-2xl flex flex-col overflow-hidden hidden md:flex flex-shrink-0">
        <div className="p-3 border-b border-border flex items-center justify-between">
          <span className="text-xs font-semibold text-foreground">Conversations</span>
          <Button
            size="sm"
            variant="ghost"
            onClick={handleCreateNewConversation}
            icon={<Plus className="w-3.5 h-3.5" />}
          >
            New
          </Button>
        </div>

        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {conversations.length === 0 ? (
            <div className="p-4 text-center text-xs text-muted-foreground">
              No conversations. Click "New" to start.
            </div>
          ) : (
            conversations.map((c) => (
              <div
                key={c.id}
                onClick={() => setCurrentConvId(c.id)}
                className={`group flex items-center justify-between p-2.5 rounded-lg text-xs cursor-pointer transition-colors ${
                  currentConvId === c.id
                    ? 'bg-primary/10 text-primary font-medium border border-primary/20'
                    : 'text-muted-foreground hover:bg-muted/60 hover:text-foreground'
                }`}
              >
                <span className="truncate flex-1">{c.title}</span>
                <button
                  onClick={(e) => handleDeleteConversation(c.id, e)}
                  className="opacity-0 group-hover:opacity-100 p-1 text-muted-foreground hover:text-rose-400 transition-opacity"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 bg-card border border-border rounded-2xl flex flex-col overflow-hidden">
        {/* Chat Header */}
        <div className="h-14 px-5 border-b border-border/70 flex items-center justify-between bg-card/60 backdrop-blur-sm">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
              <Bot className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-xs font-bold text-foreground">ContextPilot AI Agent</h2>
              <p className="text-[10px] text-muted-foreground">Autonomous Multi-Step Orchestration</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-[11px] text-muted-foreground hidden sm:inline">Active Provider:</span>
            <Badge variant="purple" size="sm" className="font-mono">
              Local Demo Engine
            </Badge>
          </div>
        </div>

        {/* Message Stream */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center max-w-md mx-auto p-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-4 border border-indigo-500/20">
                <Sparkles className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-foreground">How can I assist your workflow today?</h3>
              <p className="text-xs text-muted-foreground mt-1 mb-6 leading-relaxed">
                I can break down complex objectives into verifiable steps, query your uploaded knowledge documents, evaluate safe mathematical expressions, and execute approved tools.
              </p>

              <div className="w-full space-y-2">
                {[
                  'Prepare a study plan for my machine learning exam',
                  'Analyze quarterly cloud spend data and export report',
                  'What does the architecture guide say about human approvals?',
                ].map((prompt, i) => (
                  <button
                    key={i}
                    onClick={() => handleSendMessage(prompt)}
                    className="w-full text-left p-2.5 rounded-lg border border-border/70 bg-background/50 hover:bg-muted text-xs text-muted-foreground hover:text-foreground transition-all flex items-center justify-between"
                  >
                    <span>{prompt}</span>
                    <ArrowRight className="w-3.5 h-3.5 text-primary" />
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((m) => {
              const isAssistant = m.sender === 'assistant';
              const taskId = m.msg_metadata?.task_id;
              const citations = m.msg_metadata?.citations || [];
              const followups = m.msg_metadata?.suggested_followups || [];

              return (
                <div
                  key={m.id}
                  className={`flex gap-3 max-w-3xl ${isAssistant ? '' : 'ml-auto justify-end'}`}
                >
                  {isAssistant && (
                    <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20 flex-shrink-0 mt-0.5">
                      <Bot className="w-4 h-4" />
                    </div>
                  )}

                  <div className="space-y-3 max-w-2xl">
                    <div
                      className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed relative group ${
                        isAssistant
                          ? 'bg-muted/40 border border-border/70 text-foreground'
                          : 'bg-primary text-primary-foreground font-medium'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{m.content}</p>

                      <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
                        <button
                          onClick={() => handleCopyMessage(m.id, m.content)}
                          className="p-1 rounded bg-background/80 text-muted-foreground hover:text-foreground"
                          title="Copy response"
                        >
                          {copiedMsgId === m.id ? (
                            <Check className="w-3 h-3 text-emerald-400" />
                          ) : (
                            <Copy className="w-3 h-3" />
                          )}
                        </button>
                      </div>
                    </div>

                    {/* Plan Generated Card Callout */}
                    {taskId && (
                      <div className="p-3.5 rounded-xl border border-indigo-500/30 bg-indigo-500/5 flex items-center justify-between gap-3 animate-in fade-in">
                        <div className="flex items-center gap-2.5">
                          <div className="w-7 h-7 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
                            <Layers className="w-4 h-4" />
                          </div>
                          <div>
                            <p className="text-xs font-semibold text-foreground">Multi-Step Plan Generated</p>
                            <p className="text-[10px] text-muted-foreground">Ready for step inspection & tool execution</p>
                          </div>
                        </div>
                        <Link to={`/app/tasks/${taskId}`}>
                          <Button size="sm" variant="primary" icon={<ArrowRight className="w-3.5 h-3.5" />}>
                            View in Task Monitor
                          </Button>
                        </Link>
                      </div>
                    )}

                    {/* Grounded RAG Citations */}
                    {citations.length > 0 && (
                      <div className="p-3 rounded-xl border border-sky-500/30 bg-sky-500/5 space-y-2">
                        <div className="flex items-center gap-1.5 text-sky-400 text-[11px] font-semibold">
                          <BookOpen className="w-3.5 h-3.5" />
                          <span>Verified Knowledge Base Citations ({citations.length}):</span>
                        </div>
                        <div className="space-y-1.5">
                          {citations.map((c, i) => (
                            <div
                              key={i}
                              className="p-2 rounded bg-background/80 border border-border/40 text-[11px] text-muted-foreground"
                            >
                              <div className="flex items-center justify-between font-semibold text-foreground text-[10px] mb-0.5">
                                <span>📄 {c.filename} (Page {c.page_number})</span>
                                <span className="text-sky-400 font-mono">Score: {c.relevance_score}</span>
                              </div>
                              <p className="italic">"{c.snippet}"</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Follow-up Suggestions */}
                    {followups.length > 0 && (
                      <div className="flex flex-wrap gap-1.5 pt-1">
                        {followups.map((f, i) => (
                          <button
                            key={i}
                            onClick={() => handleSendMessage(f)}
                            className="text-[11px] px-2.5 py-1 rounded-full bg-muted/60 hover:bg-muted border border-border/40 text-muted-foreground hover:text-foreground transition-colors"
                          >
                            + {f}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              );
            })
          )}
          {isLoading && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20 flex-shrink-0">
                <Bot className="w-4 h-4 animate-pulse" />
              </div>
              <div className="p-3 rounded-2xl bg-muted/30 border border-border/40 text-xs text-muted-foreground flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-indigo-400 animate-ping" />
                <span>Evaluating context and formulating execution plan...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Message Input Box */}
        <div className="p-3 sm:p-4 border-t border-border/70 bg-card/60">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              placeholder="Ask a question or enter a task objective..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="flex-1 px-4 py-2.5 rounded-xl border border-border bg-background text-xs sm:text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary placeholder:text-muted-foreground"
            />
            <Button
              type="submit"
              size="md"
              variant="primary"
              disabled={!inputText.trim() || isLoading}
              icon={<Send className="w-4 h-4" />}
            >
              Send
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};
