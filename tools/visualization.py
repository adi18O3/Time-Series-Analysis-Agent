"""
Visualization tool.

Creates Plotly visualizations based on the analysis intent.
"""

import plotly.express as px

from models import ToolResult
from utils import (
    get_actual_column_name,
    get_target_columns,
    find_datetime_column
)


def visualization_tool(df, plan):
    """
    Generate Plotly visualizations.
    """

    figures = []

    datetime_column = find_datetime_column(df)
    columns = get_target_columns(df, plan)

    if datetime_column is None:
        return ToolResult(
            tool_name="visualization",
            status="failed",
            result={},
            chart=[],
            explanation="Datetime column not found."
        )

    intent = plan.intent.lower()

    # -------------------------------
    # Trend Visualization
    # -------------------------------
    if "trend" in intent:

        for column in columns:

            fig = px.line(
                df,
                x=datetime_column,
                y=column,
                title=f"{column} Trend"
            )

            figures.append(fig)

    # -------------------------------
    # Statistics Visualization
    # -------------------------------
    elif "statistics" in intent:

        means = []

        for column in columns:
            means.append({
                "Column": column,
                "Mean": df[column].mean()
            })

        fig = px.bar(
            means,
            x="Column",
            y="Mean",
            title="Mean Value Comparison"
        )

        figures.append(fig)

    # -------------------------------
    # Correlation Visualization
    # -------------------------------
    elif "correlation" in intent:

        if len(columns) >= 2:

            fig = px.scatter(
                    df,
                    x=columns[0],
                    y=columns[1],
                    title=f"{columns[0]} vs {columns[1]}"
                )

            figures.append(fig)

    # -------------------------------
    # Anomaly Visualization
    # -------------------------------
    elif "anomaly" in intent:

        for column in columns:

            fig = px.box(
                df,
                y=column,
                title=f"Anomaly Detection - {column}"
            )

            figures.append(fig)

    return ToolResult(
        tool_name="visualization",
        status="success",
        result={
            "total_charts": len(figures)
        },
        chart=figures,
        explanation="Visualization generated successfully."
    )