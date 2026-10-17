from typing import List, Dict, Any
from pydantic import BaseModel


class StatusDistributionStat(BaseModel):
    status: str
    count: int


class ToolUsageStat(BaseModel):
    tool_name: str
    invocations: int
    success_count: int
    failure_count: int


class DailyTaskStat(BaseModel):
    date: str
    completed: int
    failed: int
    created: int


class AnalyticsSummaryResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    pending_approvals: int
    success_rate_percentage: float
    total_tool_executions: int
    average_execution_time_ms: float
    status_distribution: List[StatusDistributionStat]
    tool_usage: List[ToolUsageStat]
    recent_trend: List[DailyTaskStat]
