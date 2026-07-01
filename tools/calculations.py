"""
Calculation tool.

Performs mathematical calculations requested by the planner.
"""

from models import ToolResult
from utils import get_target_columns


OPERATIONS = {
    "mean": lambda s: s.mean(),
    "sum": lambda s: s.sum(),
    "max": lambda s: s.max(),
    "min": lambda s: s.min(),
    "median": lambda s: s.median(),
    "std": lambda s: s.std(),
    "var": lambda s: s.var()
}


def calculation_tool(df, plan):
    """
    Perform a mathematical calculation.
    """

    columns = get_target_columns(df, plan)

    operation = None

    for step in plan.execution_steps:

        if step.startswith("calculate_"):
            operation = step.replace("calculate_", "")
            break

    if operation is None:

        return ToolResult(
            tool_name="calculation",
            status="failed",
            result={},
            explanation="No calculation requested."
        )

    if operation not in OPERATIONS:

        return ToolResult(
            tool_name="calculation",
            status="failed",
            result={},
            explanation=f"Unsupported calculation: {operation}"
        )

    results = {}

    for column in columns:

        results[column] = round(
            float(OPERATIONS[operation](df[column])),
            2
        )

    return ToolResult(
        tool_name="calculation",
        status="success",
        result=results,
        explanation=f"{operation.capitalize()} calculated successfully."
    )