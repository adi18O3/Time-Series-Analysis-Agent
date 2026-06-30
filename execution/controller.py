"""
Execution Controller.

Executes the AnalysisPlan using the appropriate analytical tools.
"""

from tools.statistics import statistics_tool
from tools.trend import trend_tool
from tools.correlation import correlation_tool
from tools.anomaly import anomaly_tool
from tools.visualization import visualization_tool


TOOLS = {
    "statistics": statistics_tool,
    "trend": trend_tool,
    "correlation": correlation_tool,
    "anomaly": anomaly_tool,
    "visualization": visualization_tool,
}


def execute_plan(plan, df):
    """
    Execute all analyses requested by the planner.
    """

    results = []

    for analysis in plan.analysis:

        tool = TOOLS.get(analysis)

        if tool is None:
            continue

        result = tool(df, plan)

        results.append(result)

    return results