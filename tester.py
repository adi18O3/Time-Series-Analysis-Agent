from planner.planner import create_analysis_plan

metadata = {
    "rows": 1000,
    "columns": [
        "Timestamp",
        "Temperature",
        "Humidity",
        "Pressure"
    ],
    "datetime_column": "Timestamp",
    "numeric_columns": [
        "Temperature",
        "Humidity",
        "Pressure"
    ]
}

plan = create_analysis_plan(
    "Compare temperature and humidity after 2 PM.",
    metadata
)

print(plan)