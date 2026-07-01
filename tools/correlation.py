"""
Correlation analysis tool.
"""

from models import ToolResult


def correlation_tool(df, plan):
    """
    Calculate correlation between two signals.
    """

    if len(plan.target_signals) < 2:
        return ToolResult(
            tool_name="correlation",
            status="failed",
            result={},
            explanation="Correlation requires two signals."
        )

    # Case-insensitive mapping
    column_mapping = {
        column.lower(): column
        for column in df.columns
    }

    signal_1 = column_mapping.get(plan.target_signals[0].lower())
    signal_2 = column_mapping.get(plan.target_signals[1].lower())

    if signal_1 is None or signal_2 is None:
        return ToolResult(
            tool_name="correlation",
            status="failed",
            result={},
            explanation="One or more signals were not found."
        )

    correlation = df[signal_1].corr(df[signal_2])

    return ToolResult(
        tool_name="correlation",
        status="success",
        result={
            "signal_1": signal_1,
            "signal_2": signal_2,
            "correlation": round(float(correlation), 3)
        },
        explanation="Correlation calculated successfully."
    )