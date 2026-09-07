import pandas as pd
import numpy as np

from calculations.employee_analysis import (
    build_employee_analysis
)


# =========================================================
# LOAD DATA
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
# COMPONENT 1
# ADAPTATION RESIDUAL SCORE
# =========================================================

df["Adaptation_Residual_Score"] = (
    min_max_score(
        df["Adaptation_Residual"]
    )
)


# =========================================================
# COMPONENT 2
# RECOVERY SCORE
# =========================================================

df["Recovery_Score"] = 0.0

recovered = (
    df["Recovery_Status"]
    == "Recovered"
)

recovered_df = df[
    recovered
]

if len(recovered_df) > 0:

    minimum = recovered_df[
        "Recovery_Time"
    ].min()

    maximum = recovered_df[
        "Recovery_Time"
    ].max()

    if maximum == minimum:

        df.loc[
            recovered,
            "Recovery_Score"
        ] = 100

    else:

        df.loc[
            recovered,
            "Recovery_Score"
        ] = (

            1
            -
            (
                (
                    df.loc[
                        recovered,
                        "Recovery_Time"
                    ]
                    - minimum
                )
                /
                (
                    maximum
                    - minimum
                )
            )

        ) * 100


# =========================================================
# COMPONENT 3
# RECOVERY VELOCITY SCORE
# =========================================================

df["Recovery_Velocity_Score"] = (
    min_max_score(
        df["Recovery_Velocity"]
    )
)


# =========================================================
# COMPONENT 4
# TRAJECTORY SCORE
# =========================================================

df["Trajectory_Score"] = (
    min_max_score(
        df["Performance_Trajectory"]
    )
)


# =========================================================
# MAPI WEIGHTS
# =========================================================

W_RESIDUAL = 0.35

W_RECOVERY = 0.30

W_VELOCITY = 0.15

W_TRAJECTORY = 0.20


# =========================================================
# MAPI
# =========================================================

df["MAPI"] = (

    W_RESIDUAL
    * df["Adaptation_Residual_Score"]

    +

    W_RECOVERY
    * df["Recovery_Score"]

    +

    W_VELOCITY
    * df["Recovery_Velocity_Score"]

    +

    W_TRAJECTORY
    * df["Trajectory_Score"]

)


df["MAPI"] = (
    df["MAPI"]
    .clip(0, 100)
    .round(2)
)


# =========================================================
# MAPI CATEGORIES
# =========================================================

def classify_mapi(score):

    if score >= 80:
        return "Highly Adaptive"

    elif score >= 60:
        return "Adaptive"

    elif score >= 40:
        return "Moderately Adaptive"

    elif score >= 20:
        return "Low Adaptation"

    else:
        return "Critical Adaptation Risk"


df["MAPI_Category"] = (
    df["MAPI"]
    .apply(classify_mapi)
)


# =========================================================
# DISPLAY INDIVIDUAL RESULTS
# =========================================================

print("\n" + "=" * 70)

print(
    "M&A ADAPTABILITY PERFORMANCE INDEX (MAPI)"
)

print("=" * 70)


display_columns = [

    "Employee_ID",

    "Employee_Type",

    "MDI",

    "Performance_Shock",

    "Adaptation_Residual_Score",

    "Recovery_Score",

    "Recovery_Velocity_Score",

    "Trajectory_Score",

    "MAPI",

    "MAPI_Category"

]


print(

    df[
        display_columns
    ]
    .sort_values(
        "MAPI",
        ascending=False
    )
    .head(20)
    .to_string(
        index=False
    )

)


# =========================================================
# SUMMARY
# =========================================================

print("\n" + "=" * 70)

print(
    "MAPI SUMMARY"
)

print("=" * 70)


print(

    df["MAPI"]
    .describe()
    .round(2)

)


# =========================================================
# CATEGORY DISTRIBUTION
# =========================================================

print("\n" + "=" * 70)

print(
    "MAPI CATEGORY DISTRIBUTION"
)

print("=" * 70)


print(

    df["MAPI_Category"]
    .value_counts()
    .sort_index()

)


# =========================================================
# EMPLOYEE TYPE COMPARISON
# =========================================================

print("\n" + "=" * 70)

print(
    "MAPI BY EMPLOYEE TYPE"
)

print("=" * 70)


type_summary = (

    df.groupby(
        "Employee_Type"
    )["MAPI"]
    .agg(
        [
            "mean",
            "std",
            "min",
            "max"
        ]
    )
    .round(2)

)


print(
    type_summary
)


# =========================================================
# MDI VS MAPI
# =========================================================

print("\n" + "=" * 70)

print(
    "MDI vs MAPI"
)

print("=" * 70)


correlation = df[
    ["MDI", "MAPI"]
].corr().iloc[0, 1]


print(
    f"Correlation: "
    f"{correlation:.3f}"
)
