import pandas as pd
import numpy as np

from calculations.employee_analysis import (
    build_employee_analysis
)


# =========================================================
# LOAD EMPLOYEE DATA
# =========================================================

df = build_employee_analysis()


# =========================================================
# EXPECTED SHOCK MODEL
# =========================================================

X = df["MDI"].values
Y = df["Performance_Shock"].values

slope, intercept = np.polyfit(
    X,
    Y,
    1
)

# Expected performance shock
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
# NORMALIZATION FUNCTION
# =========================================================

def min_max_score(series):

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(
            50,
            index=series.index
        )

    return (
        (series - minimum)
        / (maximum - minimum)
    ) * 100


# =========================================================
# 1. ADAPTATION RESIDUAL SCORE
# =========================================================

# Higher residual = better adaptation.

df["Adaptation_Residual_Score"] = (
    min_max_score(
        df["Adaptation_Residual"]
    )
)


# =========================================================
# 2. RECOVERY SCORE
# =========================================================

# Shorter recovery time = better.
#
# Employees who do not recover within the
# observation window receive 0.

recovered = df[
    df["Recovery_Status"] == "Recovered"
]

if len(recovered) > 0:

    min_recovery = recovered[
        "Recovery_Time"
    ].min()

    max_recovery = recovered[
        "Recovery_Time"
    ].max()

    if max_recovery == min_recovery:

        df["Recovery_Score"] = 100

    else:

        df["Recovery_Score"] = (
            1
            -
            (
                (
                    df["Recovery_Time"]
                    - min_recovery
                )
                /
                (
                    max_recovery
                    - min_recovery
                )
            )
        ) * 100

else:

    df["Recovery_Score"] = 0


# Explicitly penalize employees who
# did not recover.

df.loc[
    df["Recovery_Status"] != "Recovered",
    "Recovery_Score"
] = 0


# Keep within 0–100

df["Recovery_Score"] = (
    df["Recovery_Score"]
    .clip(0, 100)
)


# =========================================================
# 3. RECOVERY VELOCITY SCORE
# =========================================================

# Higher velocity = better.

df["Recovery_Velocity_Score"] = (
    min_max_score(
        df["Recovery_Velocity"]
    )
)


# =========================================================
# 4. TRAJECTORY SCORE
# =========================================================

# Higher trajectory = better.

df["Trajectory_Score"] = (
    min_max_score(
        df["Performance_Trajectory"]
    )
)


# =========================================================
# ROUND SCORES
# =========================================================

score_columns = [

    "Adaptation_Residual_Score",

    "Recovery_Score",

    "Recovery_Velocity_Score",

    "Trajectory_Score"

]

for column in score_columns:

    df[column] = (
        df[column]
        .round(2)
    )


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n" + "=" * 70)

print(
    "NORMALIZED ADAPTATION COMPONENTS"
)

print("=" * 70)


display_columns = [

    "Employee_ID",

    "Employee_Type",

    "MDI",

    "Performance_Shock",

    "Adaptation_Residual",

    "Adaptation_Residual_Score",

    "Recovery_Score",

    "Recovery_Velocity_Score",

    "Trajectory_Score"

]


print(

    df[
        display_columns
    ]
    .head(20)
    .to_string(
        index=False
    )

)


# =========================================================
# COMPONENT SUMMARY
# =========================================================

print("\n" + "=" * 70)

print(
    "COMPONENT SCORE SUMMARY"
)

print("=" * 70)


print(

    df[
        score_columns
    ]
    .describe()
    .round(2)

)


# =========================================================
# EMPLOYEE TYPE SUMMARY
# =========================================================

print("\n" + "=" * 70)

print(
    "COMPONENTS BY EMPLOYEE TYPE"
)

print("=" * 70)


type_summary = df.groupby(
    "Employee_Type"
)[
    score_columns
].mean().round(2)


print(
    type_summary
)


# =========================================================
# COMPONENT CORRELATIONS
# =========================================================

print("\n" + "=" * 70)

print(
    "CORRELATION BETWEEN COMPONENTS"
)

print("=" * 70)


print(
    df[
        score_columns
    ]
    .corr()
    .round(2)
)