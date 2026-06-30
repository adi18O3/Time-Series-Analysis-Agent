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
        You are an AI planning agent for a Time-Series Analysis Assistant.

        Dataset Metadata:
        {metadata}

        User Query:
        {query}

        Your task is to create an execution plan.

        Guidelines:
        - Understand what the user wants.
        - Identify the target signals.
        - Decide which analyses are required.
        - Decide the execution steps.
        - Choose the most appropriate visualization.
        - Do NOT answer the user's question.
        - Return only an AnalysisPlan.
        """

    return planner_llm.invoke(prompt)