import pandas as pd

from calculations.performance import (
    calculate_performance_metrics
)


# -----------------------------------------
# LOAD DATA
# -----------------------------------------

df = pd.read_csv(
    "data/employee_data.csv"
)


# -----------------------------------------
# SELECT ONE EMPLOYEE
# -----------------------------------------

employee_id = "E001"

employee = df[
    df["Employee_ID"] == employee_id
]


# -----------------------------------------
# CALCULATE METRICS
# -----------------------------------------

metrics = calculate_performance_metrics(
    employee
)


# -----------------------------------------
# DISPLAY RESULTS
# -----------------------------------------

print("\nEmployee:", employee_id)

print("\nPerformance trajectory:")

print(
    employee[
        ["Month", "Performance"]
    ].to_string(index=False)
)

print("\nPerformance Metrics:")

for metric, value in metrics.items():

    print(
        f"{metric}: {value}"
    )