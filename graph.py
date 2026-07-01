"""
LangGraph workflow for the Time-Series Analysis Agent.
"""

from typing import TypedDict

import pandas as pd
from langgraph.graph import StateGraph, END

from guardrails.guardrails import validate_query
from planner.planner import create_analysis_plan
from execution.controller import execute_plan
from memory.memory_manager import save_conversation


class AgentState(TypedDict):
    query: str
    metadata: dict
    dataframe: pd.DataFrame

    guardrail_result: object
    plan: object
    tool_results: list


# --------------------------
# Guardrail Node
# --------------------------

def guardrail_node(state):

    result = validate_query(
        state["query"],
        state["metadata"]
    )

    state["guardrail_result"] = result

    return state


# --------------------------
# Planner Node
# --------------------------

def planner_node(state):

    plan = create_analysis_plan(
        state["query"],
        state["metadata"]
    )

    state["plan"] = plan

    return state


# --------------------------
# Execution Node
# --------------------------

def execution_node(state):

    results = execute_plan(
        state["plan"],
        state["dataframe"]
    )

    state["tool_results"] = results

    # Save successful conversation
    save_conversation(
        state["query"],
        state["plan"]
    )

    return state


# --------------------------
# Routing
# --------------------------

def should_continue(state):

    if state["guardrail_result"].allowed:
        return "planner"

    return END


# --------------------------
# Build Graph
# --------------------------

graph = StateGraph(AgentState)

graph.add_node("guardrail", guardrail_node)
graph.add_node("planner", planner_node)
graph.add_node("execution", execution_node)

graph.set_entry_point("guardrail")

graph.add_conditional_edges(
    "guardrail",
    should_continue,
    {
        "planner": "planner",
        END: END
    }
)

graph.add_edge("planner", "execution")

graph.add_edge("execution", END)

agent = graph.compile()