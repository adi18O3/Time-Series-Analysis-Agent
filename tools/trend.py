"""
Trend analysis tool.
"""

from models import ToolResult
from utils import find_numeric_columns


def trend_tool(df, plan):
    """
    Identify trends for numeric signals.
    """

    columns = plan.target_signals

    if not columns:
        columns = find_numeric_columns(df)

    column_mapping = {
        column.lower(): column
        for column in df.columns
    }

    trends = {}

    for signal in columns:

        actual_column = column_mapping.get(signal.lower())

        if actual_column is None:
            continue

        first = df[actual_column].iloc[0]
        last = df[actual_column].iloc[-1]

        if last > first:
            trend = "Increasing"

        elif last < first:
            trend = "Decreasing"

        else:
            trend = "Stable"

        trends[actual_column] = {
            "first_value": float(first),
            "last_value": float(last),
            "trend": trend
        }

    return ToolResult(
        tool_name="trend",
        status="success",
        result=trends,
        explanation="Trend analysis completed successfully."
    )