"""
Statistics tool.

Calculates descriptive statistics for numeric columns.
"""

from models import ToolResult
from utils import find_numeric_columns


def statistics_tool(df, plan):
    """
    Generate descriptive statistics.
    """

    # If planner didn't specify columns, use all numeric columns
    columns = plan.target_signals

    if not columns:
        columns = find_numeric_columns(df)

    statistics = {}

    for column in columns:

        if column not in df.columns:
            continue

        statistics[column] = {
            "count": int(df[column].count()),
            "mean": round(float(df[column].mean()), 2),
            "median": round(float(df[column].median()), 2),
            "min": round(float(df[column].min()), 2),
            "max": round(float(df[column].max()), 2),
            "std": round(float(df[column].std()), 2)
        }

    return ToolResult(
        tool_name="statistics",
        status="success",
        result=statistics,
        explanation="Descriptive statistics calculated successfully."
    )