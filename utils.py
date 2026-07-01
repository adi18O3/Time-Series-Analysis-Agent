"""
Utility functions for loading and inspecting datasets.
"""

import pandas as pd
from pandas.api.types import is_numeric_dtype


def load_dataset(uploaded_file):
    """
    Load uploaded CSV file into a Pandas DataFrame.
    """
    return pd.read_csv(uploaded_file)


def find_datetime_column(df):
    """
    Detect the datetime column without modifying the dataset.
    """

    possible_names = ["timestamp", "datetime", "date", "time"]

    # Check common datetime column names first
    for column in df.columns:
        if column.lower() in possible_names:
            return column

    # Try parsing remaining columns
    for column in df.columns:
        try:
            pd.to_datetime(df[column], errors="raise")
            return column
        except Exception:
            continue

    return None


def find_numeric_columns(df):
    """
    Return numeric columns.
    """

    return [
        column
        for column in df.columns
        if is_numeric_dtype(df[column])
    ]


def get_actual_column_name(df, column_name):
    """
    Case-insensitive column lookup.
    """

    column_mapping = {
        column.lower(): column
        for column in df.columns
    }

    return column_mapping.get(column_name.lower())


def get_target_columns(df, plan):
    """
    Return planner requested columns.
    If planner doesn't specify columns,
    return all numeric columns.
    """

    if plan.target_signals:

        columns = []

        for signal in plan.target_signals:

            actual = get_actual_column_name(df, signal)

            if actual:
                columns.append(actual)

        return columns

    return find_numeric_columns(df)


def get_dataset_metadata(df):
    """
    Extract dataset metadata.
    """

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "datetime_column": find_datetime_column(df),
        "numeric_columns": find_numeric_columns(df),
        "missing_values": int(df.isnull().sum().sum())
    }