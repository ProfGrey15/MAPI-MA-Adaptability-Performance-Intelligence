import pandas as pd
import numpy as np

from calculations.employee_analysis import (
    build_employee_analysis
)


# =========================================================
# LOAD EMPLOYEE-LEVEL DATA
# =========================================================

df = build_employee_analysis()


# =========================================================
# FIT EXPECTED SHOCK MODEL
# =========================================================

# X = MDI
# Y = Performance Shock

X = df["MDI"].values

Y = df["Performance_Shock"].values


# ---------------------------------------------------------
# Linear regression using numpy
# ---------------------------------------------------------

slope, intercept = np.polyfit(
    X,
    Y,
    1
)


# =========================================================
# EXPECTED SHOCK
# =========================================================

df["Expected_Shock"] = (
    intercept
    + slope * df["MDI"]
)


# =========================================================
# ADAPTATION RESIDUAL
# =========================================================

df["Adaptation_Residual"] = (
    df["Expected_Shock"]
    - df["Performance_Shock"]
)


# =========================================================
# DISPLAY MODEL
# =========================================================

print("\n" + "=" * 60)

print(
    "EXPECTED PERFORMANCE SHOCK MODEL"
)

print("=" * 60)

print(
    f"\nIntercept (β₀): "
    f"{intercept:.3f}"
)

print(
    f"Slope (β₁): "
    f"{slope:.3f}"
)


# =========================================================
# DISPLAY EXAMPLES
# =========================================================

print("\n" + "-" * 60)

print(
    "EMPLOYEE ADAPTATION RESIDUALS"
)

print("-" * 60)


display_columns = [

    "Employee_ID",

    "Employee_Type",

    "MDI",

    "Performance_Shock",

    "Expected_Shock",

    "Adaptation_Residual"

]


print(

    df[
        display_columns
    ]
    .sort_values(
        "Adaptation_Residual",
        ascending=False
    )
    .head(10)
    .round(2)
    .to_string(
        index=False
    )

)


# =========================================================
# MOST CHALLENGED EMPLOYEES
# =========================================================

print("\n" + "-" * 60)

print(
    "EMPLOYEES PERFORMING WORSE THAN EXPECTED"
)

print("-" * 60)


print(

    df[
        display_columns
    ]
    .sort_values(
        "Adaptation_Residual"
    )
    .head(10)
    .round(2)
    .to_string(
        index=False
    )

)


# =========================================================
# SUMMARY
# =========================================================

print("\n" + "=" * 60)

print(
    "RESIDUAL SUMMARY"
)

print("=" * 60)

print(

    df[
        "Adaptation_Residual"
    ]
    .describe()
    .round(2)

)