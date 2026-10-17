export interface User {
  id: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserPreference {
  preferred_model: string;
  response_style: string;
  memory_enabled: boolean;
  default_approval_behavior: string;
  execution_timeout_seconds: number;
  theme: string;
  updated_at: string;
}

export interface Citation {
  document_id: string;
  filename: string;
  page_number: number;
  snippet: string;
  relevance_score: number;
}

export type SourceCitation = Citation;
export type GroundedQueryResult = any;

export interface Message {
  id: string;
  conversation_id: string;
  sender: 'user' | 'assistant' | 'system';
  content: string;
  msg_metadata?: {
    task_id?: string;
    citations?: Citation[];
    intent?: string;
    suggested_followups?: string[];
  };
  created_at: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
  message_count?: number;
  messages?: Message[];
}

export interface TaskStep {
  id: string;
  task_id: string;
  step_order: number;
  description: string;
  tool_name?: string;
  tool_input?: Record<string, any>;
  expected_output?: string;
  actual_output?: Record<string, any>;
  status: 'PENDING' | 'AWAITING_APPROVAL' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'SKIPPED';
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  requires_approval: boolean;
  retry_count: number;
  max_retries: number;
  execution_time_ms: number;
  error_message?: string;
  started_at?: string;
  completed_at?: string;
}

export interface ApprovalRequest {
  id: string;
  task_id: string;
  step_id?: string;
  action_name: string;
  action_purpose: string;
  target_resource?: string;
  parameters_summary?: Record<string, any>;
  risk_level: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'EXPIRED';
  decision_notes?: string;
  requested_at: string;
  decided_at?: string;
}

export interface Task {
  id: string;
  user_id: string;
  conversation_id?: string;
  objective: string;
  description?: string;
  status: 'DRAFT' | 'AWAITING_APPROVAL' | 'APPROVED' | 'QUEUED' | 'RUNNING' | 'PAUSED' | 'COMPLETED' | 'PARTIALLY_COMPLETED' | 'FAILED' | 'CANCELLED';
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';
  progress: number;
  estimated_complexity: string;
  result_summary?: string;
  error_message?: string;
  created_at: string;
  updated_at: string;
  completed_at?: string;
  step_count?: number;
  steps?: TaskStep[];
  approvals?: ApprovalRequest[];
}

export interface ToolDefinition {
  tool_id: string;
  name: string;
  description: string;
  version: string;
  input_schema: Record<string, any>;
  output_schema: Record<string, any>;
  permission_level: string;
  risk_level: string;
  requires_approval: boolean;
  is_available: boolean;
  implementation_type: 'local' | 'external' | 'simulated';
  last_executed_at?: string;
}

export interface MemoryItem {
  id: string;
  user_id: string;
  category: 'FACT' | 'PREFERENCE' | 'PROJECT_CONTEXT' | 'NOTE' | 'TASK_OUTCOME';
  title: string;
  content: string;
  confidence_score: number;
  source_reference?: string;
  is_pinned: boolean;
  created_at: string;
  updated_at: string;
}

export interface KnowledgeDocument {
  id: string;
  user_id: string;
  filename: string;
  file_type: string;
  file_size_bytes: number;
  processing_status: 'PENDING' | 'PROCESSING' | 'INDEXED' | 'FAILED';
  error_message?: string;
  chunk_count: number;
  created_at: string;
  updated_at: string;
}

export interface DocumentChunk {
  id: string;
  document_id: string;
  chunk_index: number;
  page_number: number;
  content: string;
  metadata?: Record<string, any>;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  notification_type: 'INFO' | 'APPROVAL_REQUIRED' | 'TASK_COMPLETED' | 'TASK_FAILED';
  link_url?: string;
  is_read: boolean;
  created_at: string;
}

export interface AuditEvent {
  id: string;
  user_id: string;
  event_type: string;
  resource_type?: string;
  resource_id?: string;
  action: string;
  details?: Record<string, any>;
  ip_address?: string;
  created_at: string;
}

export interface ExecutionEvent {
  id: string;
  task_id: string;
  step_id?: string;
  event_type: string;
  message: string;
  payload?: Record<string, any>;
  created_at: string;
}

export interface AnalyticsSummary {
  total_tasks: number;
  completed_tasks: number;
  failed_tasks: number;
  pending_approvals: number;
  success_rate_percentage: number;
  total_tool_executions: number;
  average_execution_time_ms: number;
  status_distribution: { status: string; count: number }[];
  tool_usage: { tool_name: string; invocations: number; success_count: number; failure_count: number }[];
  recent_trend: { date: string; completed: number; failed: number; created: number }[];
}

export interface IntegrationStatus {
  name: string;
  provider: string;
  status: 'CONNECTED' | 'SIMULATED' | 'NOT_CONFIGURED' | 'ERROR';
  is_real: boolean;
  details: string;
  latency_ms?: number;
  last_checked: string;
}
