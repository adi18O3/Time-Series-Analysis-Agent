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

        Return:
        - allowed = True if the query is about analyzing the uploaded dataset.
        - allowed = False otherwise.

        Do not answer the query.
        Return only the GuardrailResult.
        """

    return guardrail_llm.invoke(prompt)