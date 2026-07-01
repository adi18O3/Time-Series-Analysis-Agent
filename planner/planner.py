"""
Planner module.

Converts a user query into a structured AnalysisPlan.
"""

from llm import llm
from models import AnalysisPlan

planner_llm = llm.with_structured_output(AnalysisPlan)


def create_analysis_plan(query: str, metadata: dict) -> AnalysisPlan:
    """
    Generate an execution plan from the user query.
    """

    prompt = f"""
You are an AI Planner for a Time-Series Analysis Assistant.

Dataset Metadata:
{metadata}

User Query:
{query}

Create an AnalysisPlan.

Rules:

- intent must be one of:
  calculation
  statistics
  trend
  correlation
  anomaly
  visualization

- analysis must contain only:
  calculation
  statistics
  trend
  correlation
  anomaly
  visualization

- execution_steps must contain only:
  calculate_mean
  calculate_sum
  calculate_max
  calculate_min
  calculate_median
  calculate_std
  calculate_var
  detect_trend
  calculate_correlation
  detect_anomaly
  descriptive_statistics
  generate_visualization

Example 1:

User Query:
Show the temperature trend.

AnalysisPlan:
intent="trend"
target_signals=["Temperature"]
time_window=None
analysis=["trend"]
execution_steps=["detect_trend"]
visualization=None
reason="User wants to analyze the trend of Temperature."

Example 2:

User Query:
What is the maximum temperature?

AnalysisPlan:
intent="calculation"
target_signals=["Temperature"]
analysis=["calculation"]
execution_steps=["calculate_max"]
reason="User wants to find the maximum temperature."

Example 3:

User Query:
What is the average temperature?

AnalysisPlan:
intent="calculation"
target_signals=["Temperature"]
analysis=["calculation"]
execution_steps=["calculate_mean"]

Now create the AnalysisPlan.

Return ONLY the AnalysisPlan.
"""

    return planner_llm.invoke(prompt)