import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

from calculations.employee_analysis import build_employee_analysis


# ============================================================
# 1. Build employee-level performance analysis
# ============================================================

analysis = build_employee_analysis()


# ============================================================
# 2. Load raw data to obtain hidden ground truth
# ============================================================

raw = pd.read_csv("data/employee_data.csv")

ground_truth = (
    raw[
        [
            "Employee_ID",
            "Adaptability_GroundTruth"
        ]
    ]
    .drop_duplicates("Employee_ID")
)


# ============================================================
# 3. Calculate Expected Shock and Adaptation Residual
# ============================================================

slope, intercept = np.polyfit(
    analysis["MDI"],
    analysis["Performance_Shock"],
    1
)

analysis["Expected_Shock"] = (
    intercept + slope * analysis["MDI"]
)

analysis["Adaptation_Residual"] = (
    analysis["Expected_Shock"]
    - analysis["Performance_Shock"]
)


# ============================================================
# 4. Min-max normalization function
# ============================================================

def min_max_score(series):

    return (
        (series - series.min())
        / (series.max() - series.min())
        * 100
    )


# ============================================================
# 5. Calculate MAPI components
# ============================================================

analysis["Adaptation_Residual_Score"] = (
    min_max_score(
        analysis["Adaptation_Residual"]
    )
)

analysis["Recovery_Score"] = (
    100
    - min_max_score(
        analysis["Recovery_Time"]
        .fillna(analysis["Recovery_Time"].max())
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
# 6. Calculate MAPI using current prototype weights
# ============================================================

analysis["MAPI"] = (
    0.35 * analysis["Adaptation_Residual_Score"]
    + 0.30 * analysis["Recovery_Score"]
    + 0.15 * analysis["Recovery_Velocity_Score"]
    + 0.20 * analysis["Trajectory_Score"]
)


# ============================================================
# 7. Merge with hidden adaptability ground truth
# ============================================================

validation = analysis.merge(
    ground_truth,
    on="Employee_ID",
    how="inner"
)


# ============================================================
# 8. Pearson correlation
# ============================================================

pearson_r, pearson_p = pearsonr(
    validation["MAPI"],
    validation["Adaptability_GroundTruth"]
)


# ============================================================
# 9. Spearman correlation
# ============================================================

spearman_r, spearman_p = spearmanr(
    validation["MAPI"],
    validation["Adaptability_GroundTruth"]
)


# ============================================================
# 10. Print validation results
# ============================================================

print("\n" + "=" * 70)
print("MAPI VALIDATION AGAINST HIDDEN ADAPTABILITY")
print("=" * 70)

print(
    f"\nEmployees validated: "
    f"{len(validation)}"
)

print("\nMAPI vs Adaptability Ground Truth")

print(
    f"Pearson r:    {pearson_r:.3f}"
)

print(
    f"Pearson p:    {pearson_p:.5f}"
)

print(
    f"Spearman rho: {spearman_r:.3f}"
)

print(
    f"Spearman p:   {spearman_p:.5f}"
)


# ============================================================
# 11. MAPI by ground-truth adaptability level
# ============================================================

print("\n" + "=" * 70)
print("MAPI BY ADAPTABILITY GROUND TRUTH")
print("=" * 70)

group_summary = (
    validation
    .groupby("Adaptability_GroundTruth")["MAPI"]
    .agg(["mean", "std", "count"])
    .sort_index()
)

print(group_summary)


# ============================================================
# 12. Additional validation
# ============================================================

print("\n" + "=" * 70)
print("ADDITIONAL VALIDATION")
print("=" * 70)

checks = [
    ("Performance_Shock", "expected NEGATIVE"),
    ("Recovery_Time", "expected NEGATIVE"),
    ("Recovery_Velocity", "expected POSITIVE"),
    ("Performance_Trajectory", "expected POSITIVE")
]

for metric, expected in checks:

    if metric in validation.columns:

        temp = validation[
            [metric, "MAPI"]
        ].dropna()

        r, p = pearsonr(
            temp["MAPI"],
            temp[metric]
        )

        print(
            f"MAPI vs {metric}: "
            f"r = {r:.3f}, "
            f"p = {p:.5f} "
            f"({expected})"
        )