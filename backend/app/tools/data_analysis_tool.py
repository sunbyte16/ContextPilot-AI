import statistics
from typing import Dict, Any, Optional, List
from app.tools.base import BaseTool


class DataAnalysisTool(BaseTool):
    tool_id = "data_analysis"
    name = "Tabular Data & Statistical Analyzer"
    description = "Calculates descriptive statistics (mean, median, sum, min, max, variance) and grouped aggregations on tabular records."
    version = "1.0.0"
    risk_level = "LOW"
    requires_approval = False
    implementation_type = "local"

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "records": {
                    "type": "array",
                    "description": "List of dictionary records to analyze, e.g. [{'item': 'A', 'val': 10}, ...]"
                },
                "value_field": {
                    "type": "string",
                    "description": "The numeric key in the records to compute statistics for"
                },
                "group_by_field": {
                    "type": "string",
                    "description": "Optional categorical key to group summaries by"
                }
            },
            "required": ["records", "value_field"]
        }

    def get_output_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "metrics": {"type": "object"},
                "grouped_metrics": {"type": "object"},
                "sample_count": {"type": "integer"}
            }
        }

    def execute(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        records = params.get("records", [])
        value_field = params.get("value_field")
        group_by_field = params.get("group_by_field")

        if not records or not isinstance(records, list):
            raise ValueError("Parameter 'records' must be a non-empty list of items.")
        if not value_field:
            raise ValueError("Parameter 'value_field' is required.")

        # Extract numeric values
        values: List[float] = []
        for r in records:
            if isinstance(r, dict) and value_field in r:
                try:
                    val = float(r[value_field])
                    values.append(val)
                except (ValueError, TypeError):
                    continue

        if not values:
            raise ValueError(f"No numeric values could be extracted for key '{value_field}'.")

        n = len(values)
        total_sum = sum(values)
        mean_val = total_sum / n
        median_val = statistics.median(values)
        min_val = min(values)
        max_val = max(values)
        variance_val = statistics.variance(values) if n > 1 else 0.0
        std_dev = statistics.stdev(values) if n > 1 else 0.0

        metrics = {
            "count": n,
            "sum": round(total_sum, 4),
            "mean": round(mean_val, 4),
            "median": round(median_val, 4),
            "min": round(min_val, 4),
            "max": round(max_val, 4),
            "variance": round(variance_val, 4),
            "std_deviation": round(std_dev, 4)
        }

        # Optional group by
        grouped = {}
        if group_by_field:
            group_buckets: Dict[str, List[float]] = {}
            for r in records:
                if isinstance(r, dict) and group_by_field in r and value_field in r:
                    grp_key = str(r[group_by_field])
                    try:
                        v = float(r[value_field])
                        group_buckets.setdefault(grp_key, []).append(v)
                    except (ValueError, TypeError):
                        continue
            
            for k, grp_vals in group_buckets.items():
                grouped[k] = {
                    "count": len(grp_vals),
                    "sum": round(sum(grp_vals), 4),
                    "mean": round(statistics.mean(grp_vals), 4),
                    "min": round(min(grp_vals), 4),
                    "max": round(max(grp_vals), 4)
                }

        return {
            "success": True,
            "sample_count": n,
            "metrics": metrics,
            "grouped_metrics": grouped if grouped else None
        }
