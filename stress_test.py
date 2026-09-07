import pandas as pd
import numpy as np

from calculations.employee_analysis import build_employee_analysis


# ============================================================
# 1. BUILD EMPLOYEE-LEVEL PERFORMANCE ANALYSIS
# ============================================================

analysis = build_employee_analysis()


# ============================================================
# 2. CALCULATE MAPI
# ============================================================

# Expected performance shock based on MDI
slope, intercept = np.polyfit(
    analysis["MDI"],
    analysis["Performance_Shock"],
    1
)

analysis["Expected_Shock"] = (
    intercept
    + slope * analysis["MDI"]
)

# Positive residual = employee performed better
# than expected given their level of disruption
analysis["Adaptation_Residual"] = (
    analysis["Expected_Shock"]
    - analysis["Performance_Shock"]
)


# ============================================================
# 3. MIN-MAX NORMALIZATION FUNCTION
# ============================================================

def min_max_score(series):

    return (
        (series - series.min())
        / (series.max() - series.min())
        * 100
    )


# ============================================================
# 4. CALCULATE MAPI COMPONENTS
# ============================================================

analysis["Adaptation_Residual_Score"] = (
    min_max_score(
        analysis["Adaptation_Residual"]
    )
)

analysis["Recovery_Score"] = (
    100
    - min_max_score(
        analysis["Recovery_Time"].fillna(
            analysis["Recovery_Time"].max()
        )
    )
)

analysis["Recovery_Velocity_Score"] = (
    min_max_score(
        analysis["Recovery_Velocity"]
    )
)

analysis["Trajectory_Score"] = (
    min_max_score(
        analysis["Performance_Trajectory"]
    )
)


# ============================================================
# 5. CALCULATE FINAL MAPI
# ============================================================

analysis["MAPI"] = (
    0.35 * analysis["Adaptation_Residual_Score"]
    + 0.30 * analysis["Recovery_Score"]
    + 0.15 * analysis["Recovery_Velocity_Score"]
    + 0.20 * analysis["Trajectory_Score"]
)


# ============================================================
# 6. FIND LOWEST AND HIGHEST MDI EMPLOYEES
# ============================================================

low_mdi = analysis.loc[
    analysis["MDI"].idxmin()
]

high_mdi = analysis.loc[
    analysis["MDI"].idxmax()
]


# ============================================================
# 7. DISPLAY EXTREME CASES
# ============================================================

print("\n" + "=" * 70)
print("MAPI STRESS TEST — EXTREME DISRUPTION CASES")
print("=" * 70)


print("\nLOWEST MDI EMPLOYEE")
print("-" * 70)

print(
    low_mdi[
        [
            "Employee_ID",
            "Employee_Type",
            "MDI",
            "Performance_Shock",
            "Recovery_Time",
            "Recovery_Velocity",
            "Performance_Trajectory",
            "MAPI"
        ]
    ]
)


print("\nHIGHEST MDI EMPLOYEE")
print("-" * 70)

print(
    high_mdi[
        [
            "Employee_ID",
            "Employee_Type",
            "MDI",
            "Performance_Shock",
            "Recovery_Time",
            "Recovery_Velocity",
            "Performance_Trajectory",
            "MAPI"
        ]
    ]
)


# ============================================================
# 8. MDI DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("MDI DISTRIBUTION")
print("=" * 70)

print(
    analysis["MDI"].describe()
)


# ============================================================
# 9. DIVIDE EMPLOYEES INTO MDI QUARTILES
# ============================================================

analysis["MDI_Group"] = pd.qcut(
    analysis["MDI"],
    q=4,
    labels=[
        "Low MDI",
        "Moderate-Low MDI",
        "Moderate-High MDI",
        "High MDI"
    ]
)


# ============================================================
# 10. MAPI BY MDI QUARTILE
# ============================================================

print("\n" + "=" * 70)
print("MAPI BY MDI QUARTILE")
print("=" * 70)

print(
    analysis
    .groupby(
        "MDI_Group",
        observed=True
    )["MAPI"]
    .agg(
        [
            "mean",
            "std",
            "min",
            "max"
        ]
    )
)


# ============================================================
# 11. CHECK WHETHER HIGH DISRUPTION AUTOMATICALLY
#     MEANS LOW MAPI
# ============================================================

correlation = (
    analysis[
        [
            "MDI",
            "MAPI"
        ]
    ]
    .corr()
    .iloc[0, 1]
)


print("\n" + "=" * 70)
print("MDI vs MAPI")
print("=" * 70)

print(
    f"Correlation: {correlation:.3f}"
)


print("\nInterpretation:")

print(
    "A strong negative correlation would suggest that "
    "MAPI may simply be penalizing employees for experiencing "
    "greater disruption."
)

print(
    "A weak or moderate relationship is preferable because "
    "MAPI should evaluate adaptation relative to disruption."
)


# ============================================================
# 12. HIGH-DISRUPTION / HIGH-MAPI CASES
# ============================================================

print("\n" + "=" * 70)
print("HIGH DISRUPTION + HIGH ADAPTATION")
print("=" * 70)

high_disruption_adaptive = (
    analysis[
        (analysis["MDI"] >= analysis["MDI"].quantile(0.75))
        & (analysis["MAPI"] >= analysis["MAPI"].quantile(0.75))
    ]
    .sort_values("MAPI", ascending=False)
)

print(
    high_disruption_adaptive[
        [
            "Employee_ID",
            "Employee_Type",
            "MDI",
            "Performance_Shock",
            "MAPI"
        ]
    ]
)


# ============================================================
# 13. LOW-DISRUPTION / LOW-MAPI CASES
# ============================================================

print("\n" + "=" * 70)
print("LOW DISRUPTION + LOW ADAPTATION")
print("=" * 70)

low_disruption_adaptive = (
    analysis[
        (analysis["MDI"] <= analysis["MDI"].quantile(0.25))
        & (analysis["MAPI"] <= analysis["MAPI"].quantile(0.25))
    ]
    .sort_values("MAPI")
)

print(
    low_disruption_adaptive[
        [
            "Employee_ID",
            "Employee_Type",
            "MDI",
            "Performance_Shock",
            "MAPI"
        ]
    ]
)

# ============================================================
# 14. EXTREME ADAPTATION CASES
# ============================================================

print("\n" + "=" * 70)
print("EXTREME ADAPTATION CASES")
print("=" * 70)


# ------------------------------------------------------------
# Top 10 MAPI scores
# ------------------------------------------------------------

print("\nTOP 10 ADAPTATION SCORES")
print("-" * 70)

top_adaptive = (
    analysis
    .sort_values("MAPI", ascending=False)
    .head(10)
)

print(
    top_adaptive[
        [
            "Employee_ID",
            "Employee_Type",
            "MDI",
            "Performance_Shock",
            "Recovery_Time",
            "Recovery_Velocity",
            "Performance_Trajectory",
            "MAPI"
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# Bottom 10 MAPI scores
# ------------------------------------------------------------

print("\nBOTTOM 10 ADAPTATION SCORES")
print("-" * 70)

bottom_adaptive = (
    analysis
    .sort_values("MAPI", ascending=True)
    .head(10)
)

print(
    bottom_adaptive[
        [
            "Employee_ID",
            "Employee_Type",
            "MDI",
            "Performance_Shock",
            "Recovery_Time",
            "Recovery_Velocity",
            "Performance_Trajectory",
            "MAPI"
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# Check relationship between MAPI and employee type
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("EXTREME CASE EMPLOYEE TYPES")
print("=" * 70)

print("\nTop 10 employee types:")

print(
    top_adaptive["Employee_Type"]
    .value_counts()
)

print("\nBottom 10 employee types:")

print(
    bottom_adaptive["Employee_Type"]
    .value_counts()
)

# ============================================================
# 15. DEPARTMENT / FAIRNESS CHECK
# ============================================================

print("\n" + "=" * 70)
print("DEPARTMENT / FAIRNESS CHECK")
print("=" * 70)


# ------------------------------------------------------------
# MAPI by department
# ------------------------------------------------------------

print("\nMAPI BY DEPARTMENT")
print("-" * 70)

department_mapi = (
    analysis
    .groupby("Department")["MAPI"]
    .agg(
        [
            "mean",
            "std",
            "min",
            "max",
            "count"
        ]
    )
    .sort_values("mean", ascending=False)
)

print(department_mapi)


# ------------------------------------------------------------
# MDI by department
# ------------------------------------------------------------

print("\nMDI BY DEPARTMENT")
print("-" * 70)

department_mdi = (
    analysis
    .groupby("Department")["MDI"]
    .agg(
        [
            "mean",
            "std",
            "min",
            "max",
            "count"
        ]
    )
    .sort_values("mean", ascending=False)
)

print(department_mdi)


# ------------------------------------------------------------
# Employee type distribution by department
# ------------------------------------------------------------

print("\nEMPLOYEE TYPE DISTRIBUTION BY DEPARTMENT")
print("-" * 70)

print(
    pd.crosstab(
        analysis["Department"],
        analysis["Employee_Type"]
    )
)