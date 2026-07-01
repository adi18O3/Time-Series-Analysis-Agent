"""
Execution Controller.

Executes the AnalysisPlan using the appropriate analytical tools.
"""

from tools.statistics import statistics_tool
from tools.calculations import calculation_tool
from tools.trend import trend_tool
from tools.correlation import correlation_tool
from tools.anomaly import anomaly_tool
from tools.visualization import visualization_tool


TOOLS = {
    "statistics": statistics_tool,
    "calculation": calculation_tool,
    "trend": trend_tool,
    "correlation": correlation_tool,
    "anomaly": anomaly_tool,
}


def execute_plan(plan, df):
    """
    Execute the analysis plan.
    """

    results = []

    normalized_analysis = []

    for analysis in plan.analysis:

        if analysis.startswith("calculate_"):
            normalized_analysis.append("calculation")
        else:
            normalized_analysis.append(analysis)

    # Execute analysis tools
    for analysis in normalized_analysis:

        tool = TOOLS.get(analysis)

        if tool:

            results.append(
                tool(df, plan)
            )

    # Always generate visualization
    visualization = visualization_tool(df, plan)

    if visualization.chart:
        results.append(visualization)

    return results