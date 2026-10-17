import pytest
from app.tools.registry import tool_registry


def test_date_time_tool():
    tool = tool_registry.get_tool("date_time")
    assert tool is not None

    # Current time
    res = tool.execute({"operation": "current_time"})
    assert res["success"] is True
    assert "utc_iso" in res["result"]
    assert "weekday" in res["result"]

    # Difference
    diff = tool.execute({
        "operation": "calculate_difference",
        "start_date": "2026-10-01T00:00:00Z",
        "end_date": "2026-10-15T12:00:00Z"
    })
    assert diff["success"] is True
    assert diff["result"]["days"] == 14
    assert diff["result"]["is_past"] is False


def test_safe_calculator_tool():
    tool = tool_registry.get_tool("safe_calculator")
    assert tool is not None

    # Normal math
    res = tool.execute({"expression": "(12 * 8) + sqrt(144)"})
    assert res["success"] is True
    assert res["result"] == 108.0

    # Complex expression
    res2 = tool.execute({"expression": "2 ** 10 - 24"})
    assert res2["result"] == 1000

    # Disallowed syntax: __import__
    with pytest.raises(Exception):
        tool.execute({"expression": "__import__('os').system('ls')"})

    # Division by zero
    with pytest.raises(ZeroDivisionError):
        tool.execute({"expression": "100 / 0"})


def test_data_analysis_tool():
    tool = tool_registry.get_tool("data_analysis")
    assert tool is not None

    records = [
        {"department": "Engineering", "salary": 10000},
        {"department": "Engineering", "salary": 12000},
        {"department": "Design", "salary": 8000},
        {"department": "Marketing", "salary": 9000}
    ]
    res = tool.execute({
        "records": records,
        "value_field": "salary",
        "group_by_field": "department"
    })
    assert res["success"] is True
    metrics = res["metrics"]
    assert metrics["count"] == 4
    assert metrics["sum"] == 39000.0
    assert metrics["mean"] == 9750.0
    assert metrics["min"] == 8000.0
    assert metrics["max"] == 12000.0

    grouped = res["grouped_metrics"]
    assert "Engineering" in grouped
    assert grouped["Engineering"]["count"] == 2
    assert grouped["Engineering"]["sum"] == 22000.0
