"""
LLM-based guardrails for validating user queries.
"""

from llm import llm
from models import GuardrailResult


# Create a structured LLM
guardrail_llm = llm.with_structured_output(GuardrailResult)


def validate_query(query: str, metadata: dict) -> GuardrailResult:
    """
    Validate whether the user's query should be processed.
    """

    if metadata is None:
        return GuardrailResult(
            allowed=False,
            reason="no_dataset",
            message="Please upload a dataset before asking questions."
        )

    prompt = f"""
You are a guardrail for a Time-Series Analysis Assistant.

Dataset Metadata:
{metadata}

User Query:
{query}

A query is ALLOWED if it:

- asks about any column in the uploaded dataset
- requests calculations
- requests statistics
- requests trends
- requests anomaly detection
- requests correlation
- requests visualization
- refers to dataset columns such as:
  {metadata["columns"]}

Examples of allowed queries:

- Show temperature trend
- Detect anomalies in Temperature
- Average Humidity
- Maximum Pressure
- Correlation between Temperature and Humidity
- Plot Temperature

Examples of blocked queries:

- What is the capital of India?
- Tell me a joke.
- Write Python code.
- Who is Virat Kohli?
- Explain machine learning.

Return:

allowed=True if the query is dataset related.

allowed=False otherwise.

If allowed=False:

message="I can only answer questions related to the uploaded time-series dataset."

If allowed=True:

message=""

Return only GuardrailResult.
"""

    return guardrail_llm.invoke(prompt)