import pandas as pd
import matplotlib.pyplot as plt

from calculations.employee_analysis import (
    build_employee_analysis
)


# -----------------------------------------
# LOAD EMPLOYEE-LEVEL ANALYSIS
# -----------------------------------------

df = build_employee_analysis()


# -----------------------------------------
# BASIC INFORMATION
# -----------------------------------------

print("\n" + "=" * 60)
print("M&A EMPLOYEE ANALYSIS")
print("=" * 60)

print(
    f"\nNumber of employees: "
    f"{len(df)}"
)

print(
    f"Number of departments: "
    f"{df['Department'].nunique()}"
)


# -----------------------------------------
# CORRELATION 1
# MDI vs PERFORMANCE SHOCK
# -----------------------------------------

correlation_shock = df[
    ["MDI", "Performance_Shock"]
].corr().iloc[0, 1]

print("\n" + "-" * 60)

print(
    "MDI vs Performance Shock"
)

print(
    f"Correlation: "
    f"{correlation_shock:.3f}"
)


# -----------------------------------------
# CORRELATION 2
# MDI vs RECOVERY TIME
# -----------------------------------------

correlation_recovery = df[
    ["MDI", "Recovery_Time"]
].corr().iloc[0, 1]

print("\n" + "-" * 60)

print(
    "MDI vs Recovery Time"
)

print(
    f"Correlation: "
    f"{correlation_recovery:.3f}"
)


# -----------------------------------------
# EMPLOYEE TYPE ANALYSIS
# -----------------------------------------

print("\n" + "=" * 60)

print("EMPLOYEE TYPE ANALYSIS")

print("=" * 60)

type_summary = df.groupby(
    "Employee_Type"
).agg({

    "MDI": "mean",

    "Performance_Shock": "mean",

    "Performance_Volatility": "mean",

    "Recovery_Time": "mean",

    "Recovery_Velocity": "mean",

    "Performance_Trajectory": "mean"

}).round(2)

print(
    type_summary
)


# -----------------------------------------
# DEPARTMENT ANALYSIS
# -----------------------------------------

print("\n" + "=" * 60)

print("DEPARTMENT ANALYSIS")

print("=" * 60)

department_summary = df.groupby(
    "Department"
).agg({

    "MDI": "mean",

    "Performance_Shock": "mean",

    "Recovery_Time": "mean",

    "Performance_Trajectory": "mean"

}).round(2)

print(
    department_summary
)


# -----------------------------------------
# PLOT 1
# MDI VS PERFORMANCE SHOCK
# -----------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    df["MDI"],
    df["Performance_Shock"]
)

plt.xlabel(
    "Merger Disruption Index (MDI)"
)

plt.ylabel(
    "Performance Shock (%)"
)

plt.title(
    "MDI vs Performance Shock"
)

plt.tight_layout()

plt.show()


# -----------------------------------------
# PLOT 2
# MDI VS RECOVERY TIME
# -----------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    df["MDI"],
    df["Recovery_Time"]
)

plt.xlabel(
    "Merger Disruption Index (MDI)"
)

plt.ylabel(
    "Recovery Time (Months)"
)

plt.title(
    "MDI vs Recovery Time"
)

plt.tight_layout()

plt.show()