"""
Utility functions for loading and inspecting datasets.
"""

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype


def load_dataset(uploaded_file):
    """
    Load uploaded CSV file into a Pandas DataFrame.
    """
    return pd.read_csv(uploaded_file)


def find_datetime_column(df):
    """
    Detect the datetime column in the dataset.
    """

    # Common datetime column names
    possible_names = ["timestamp", "datetime", "date", "time"]

    # Check column names first
    for column in df.columns:
        if column.lower() in possible_names:
            df[column] = pd.to_datetime(df[column], errors="coerce")
            return column

    # Otherwise try detecting automatically
    for column in df.columns:
        try:
            converted = pd.to_datetime(df[column], errors="raise")
            df[column] = converted
            return column
        except Exception:
            continue

    return None


def find_numeric_columns(df):
    """
    Return all numeric columns.
    """

    numeric_columns = []

    for column in df.columns:
        if is_numeric_dtype(df[column]):
            numeric_columns.append(column)

    return numeric_columns


def get_dataset_metadata(df):
    """
    Extract metadata required by the Planner and Guardrails.
    """

    datetime_column = find_datetime_column(df)
    numeric_columns = find_numeric_columns(df)

    metadata = {
        "rows": len(df),
        "columns": list(df.columns),
        "datetime_column": datetime_column,
        "numeric_columns": numeric_columns,
        "missing_values": int(df.isnull().sum().sum())
    }

    return metadata