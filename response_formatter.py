"""
Formats ToolResult objects into user-friendly responses.
"""


def format_response(tool_results, plan):

    responses = []

    # -----------------------------
    # Calculation
    # -----------------------------
    if plan.intent == "calculation":

        operation = ""

        for step in plan.execution_steps:

            if step.startswith("calculate_"):
                operation = step.replace("calculate_", "")
                break

        operation_names = {
            "mean": "average",
            "sum": "sum",
            "max": "maximum",
            "min": "minimum",
            "median": "median",
            "std": "standard deviation",
            "var": "variance"
        }

        operation = operation_names.get(operation, operation)

        for tool in tool_results:

            if tool.tool_name != "calculation":
                continue

            for column, value in tool.result.items():

                responses.append(
                    f"✅ The {operation} of '{column}' is {value}."
                )

    # -----------------------------
    # Statistics
    # -----------------------------
    elif plan.intent == "statistics":

        responses.append(
            "📊 Statistical summary generated successfully."
        )

    # -----------------------------
    # Trend
    # -----------------------------
    elif plan.intent == "trend":

        for tool in tool_results:

            if tool.tool_name != "trend":
                continue

            for column, data in tool.result.items():

                responses.append(
                    f"📈 '{column}' shows a **{data['trend']}** trend."
                )

    # -----------------------------
    # Correlation
    # -----------------------------
    elif plan.intent == "correlation":

        for tool in tool_results:

            if tool.tool_name != "correlation":
                continue

            responses.append(
                f"📈 The correlation between "
                f"'{tool.result['signal_1']}' and "
                f"'{tool.result['signal_2']}' "
                f"is {tool.result['correlation']}."
            )

    # -----------------------------
    # Anomaly
    # -----------------------------
    elif plan.intent == "anomaly":

        for tool in tool_results:

            if tool.tool_name != "anomaly":
                continue

            for column, data in tool.result.items():

                if data["count"] == 0:

                    responses.append(
                        f"✅ No anomalies were detected in '{column}'."
                    )

                else:

                    responses.append(
                        f"⚠️ {data['count']} anomalies were detected in '{column}'."
                    )

    else:

        responses.append(
            "Analysis completed successfully."
        )

    return responses