from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.all_models import User, Task, TaskStep, ApprovalRequest, ToolExecution
from app.schemas.analytics import AnalyticsSummaryResponse, ToolUsageStat, StatusDistributionStat, DailyTaskStat
from app.security.deps import get_current_user

router = APIRouter()


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.status == "COMPLETED")
    failed_tasks = sum(1 for t in tasks if t.status == "FAILED")
    
    pending_approvals = db.query(ApprovalRequest).filter(
        ApprovalRequest.user_id == current_user.id,
        ApprovalRequest.status == "PENDING"
    ).count()

    finished = completed_tasks + failed_tasks
    success_rate = round((completed_tasks / finished) * 100, 1) if finished > 0 else 100.0

    # Tool executions
    tool_execs = db.query(ToolExecution).filter(ToolExecution.user_id == current_user.id).all()
    total_tool_executions = len(tool_execs)
    avg_exec_time = (
        round(sum(e.duration_ms for e in tool_execs) / total_tool_executions, 1)
        if total_tool_executions > 0 else 0.0
    )

    # Status distribution
    status_counts: Dict[str, int] = {}
    for t in tasks:
        st = t.status
        status_counts[st] = status_counts.get(st, 0) + 1

    status_dist = [
        StatusDistributionStat(status=k, count=v)
        for k, v in status_counts.items()
    ]
    if not status_dist:
        status_dist = [StatusDistributionStat(status="EMPTY", count=0)]

    # Tool usage counts
    tool_map: Dict[str, Dict[str, int]] = {}
    for te in tool_execs:
        tname = te.tool_name
        if tname not in tool_map:
            tool_map[tname] = {"total": 0, "success": 0, "failure": 0}
        tool_map[tname]["total"] += 1
        if te.status == "SUCCESS":
            tool_map[tname]["success"] += 1
        else:
            tool_map[tname]["failure"] += 1

    tool_usage = [
        ToolUsageStat(
            tool_name=k,
            invocations=v["total"],
            success_count=v["success"],
            failure_count=v["failure"]
        )
        for k, v in tool_map.items()
    ]
    if not tool_usage:
        tool_usage = [ToolUsageStat(tool_name="None", invocations=0, success_count=0, failure_count=0)]

    # 7-day trend
    today = datetime.now(timezone.utc).date()
    daily_stats = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_str = day.strftime("%b %d")
        created_count = sum(1 for t in tasks if t.created_at and t.created_at.date() == day)
        comp_count = sum(1 for t in tasks if t.completed_at and t.completed_at.date() == day)
        fail_count = sum(1 for t in tasks if t.status == "FAILED" and t.updated_at and t.updated_at.date() == day)
        daily_stats.append(DailyTaskStat(
            date=day_str,
            completed=comp_count,
            failed=fail_count,
            created=created_count
        ))

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "failed_tasks": failed_tasks,
        "pending_approvals": pending_approvals,
        "success_rate_percentage": success_rate,
        "total_tool_executions": total_tool_executions,
        "average_execution_time_ms": avg_exec_time,
        "status_distribution": status_dist,
        "tool_usage": tool_usage,
        "recent_trend": daily_stats
    }
