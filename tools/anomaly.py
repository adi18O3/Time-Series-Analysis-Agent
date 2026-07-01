"""
Anomaly detection tool using the IQR method.
"""

from models import ToolResult
from utils import get_target_columns


def anomaly_tool(df, plan):
    """
    Detect anomalies using the IQR method.
    """

    columns = get_target_columns(df, plan)

    anomalies = {}

    for column in columns:

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        anomaly_indices = df[
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ].index.tolist()

        anomalies[column] = {
            "count": len(anomaly_indices),
            "lower_bound": round(float(lower_bound), 2),
            "upper_bound": round(float(upper_bound), 2),
            "indices": anomaly_indices
        }

    return ToolResult(
        tool_name="anomaly",
        status="success",
        result=anomalies,
        explanation="Anomaly detection completed successfully."
    )