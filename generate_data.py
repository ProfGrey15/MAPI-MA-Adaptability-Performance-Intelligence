import pandas as pd
import numpy as np

# =========================================================
# M&A INTEGRATION INTELLIGENCE
# SYNTHETIC LONGITUDINAL DATA GENERATOR
# =========================================================

# Reproducibility
np.random.seed(42)

# ---------------------------------------------------------
# BASIC SETTINGS
# ---------------------------------------------------------

n_employees = 200

# Six months before merger
# Merger at Month 0
# Six months after merger
months = list(range(-6, 7))


# ---------------------------------------------------------
# EMPLOYEE ADAPTABILITY PROFILES
# ---------------------------------------------------------

adaptability_profiles = {

    "Resilient": 0.90,

    "Rapid Adaptor": 0.80,

    "Stable Specialist": 0.60,

    "Delayed Adaptor": 0.50,

    "Vulnerable": 0.25,

    "Declining": 0.10
}


# ---------------------------------------------------------
# CREATE EMPLOYEE DATA
# ---------------------------------------------------------

employees = []


for i in range(1, n_employees + 1):

    # ---------------------------------------------
    # ORGANIZATIONAL INFORMATION
    # ---------------------------------------------

    company = (
        "Company A"
        if i <= 100
        else "Company B"
    )

    department = np.random.choice([
        "Finance",
        "HR",
        "Marketing",
        "IT",
        "Operations",
        "Sales"
    ])


    # ---------------------------------------------
    # BASELINE PERFORMANCE
    # ---------------------------------------------

    baseline = np.random.normal(
        80,
        7
    )

    baseline = np.clip(
        baseline,
        55,
        98
    )


    # ---------------------------------------------
    # EMPLOYEE ADAPTABILITY TYPE
    # ---------------------------------------------

    employee_type = np.random.choice(
        list(adaptability_profiles.keys())
    )

    adaptability = adaptability_profiles[
        employee_type
    ]


    # =================================================
    # M&A DISRUPTION DIMENSIONS
    # =================================================

    role_change = np.random.randint(
        0,
        101
    )

    team_change = np.random.randint(
        0,
        101
    )

    leadership_change = np.random.randint(
        0,
        101
    )

    technology_change = np.random.randint(
        0,
        101
    )

    process_change = np.random.randint(
        0,
        101
    )

    culture_change = np.random.randint(
        0,
        101
    )

    location_environment_change = np.random.randint(
        0,
        101
    )


    # =================================================
    # MDI
    # =================================================

    mdi = np.mean([

        role_change,

        team_change,

        leadership_change,

        technology_change,

        process_change,

        culture_change,

        location_environment_change

    ])


    # =================================================
    # PERFORMANCE SHOCK
    # =================================================

    # Base effect of disruption
    disruption_effect = (
        0.30 * mdi
    )

    # Protective effect of adaptability
    adaptability_effect = (
        15 * adaptability
    )

    # Individual-level randomness
    random_effect = np.random.normal(
        0,
        3
    )

    # Final shock
    shock = (
        8
        + disruption_effect
        - adaptability_effect
        + random_effect
    )

    # Keep shock within sensible bounds
    shock = np.clip(
        shock,
        3,
        35
    )


    # =================================================
    # RECOVERY RATE
    # =================================================

    # More adaptable employees recover faster.
    #
    # Higher disruption slightly slows recovery.

    recovery_rate = (
        1.5
        + 5 * adaptability
        - 0.025 * mdi
        + np.random.normal(0, 0.4)
    )

    recovery_rate = max(
        recovery_rate,
        0
    )


    # =================================================
    # CREATE MONTHLY PERFORMANCE
    # =================================================

    for month in months:

        noise = np.random.normal(
            0,
            2
        )


        # ---------------------------------------------
        # PRE-MERGER
        # ---------------------------------------------

        if month < 0:

            performance = (
                baseline
                + noise
            )


        # ---------------------------------------------
        # MERGER MONTH
        # ---------------------------------------------

        elif month == 0:

            performance = (
                baseline
                - shock
                + noise
            )


        # ---------------------------------------------
        # POST-MERGER
        # ---------------------------------------------

        else:

            performance = (
                baseline
                - shock
                + recovery_rate * month
                + noise
            )


            # -----------------------------------------
            # DECLINING EMPLOYEES
            # -----------------------------------------

            if employee_type == "Declining":

                performance -= (
                    0.8 * month
                )


        # ---------------------------------------------
        # KEEP PERFORMANCE IN RANGE
        # ---------------------------------------------

        performance = np.clip(
            performance,
            30,
            100
        )


        # ---------------------------------------------
        # STORE RECORD
        # ---------------------------------------------

        employees.append({

            "Employee_ID":
                f"E{i:03d}",

            "Company":
                company,

            "Department":
                department,

            "Employee_Type":
                employee_type,

            "Month":
                month,

            "Performance":
                round(
                    performance,
                    2
                ),

            # M&A dimensions

            "Role_Change":
                role_change,

            "Team_Change":
                team_change,

            "Leadership_Change":
                leadership_change,

            "Technology_Change":
                technology_change,

            "Process_Change":
                process_change,

            "Culture_Change":
                culture_change,

            "Location_Environment_Change":
                location_environment_change,

            # Hidden simulation variable
            #
            # We use this to generate the data.
            # We will NOT use this directly in MAPI.

            "Adaptability_GroundTruth":
                adaptability
        })


# =========================================================
# CREATE DATAFRAME
# =========================================================

df = pd.DataFrame(
    employees
)


# =========================================================
# SAVE DATA
# =========================================================

df.to_csv(
    "data/employee_data.csv",
    index=False
)


# =========================================================
# CONFIRMATION
# =========================================================

print(
    "\nDataset created successfully!"
)

print(
    f"Employees: "
    f"{df['Employee_ID'].nunique()}"
)

print(
    f"Rows: "
    f"{len(df)}"
)

print(
    "\nColumns:"
)

print(
    df.columns.tolist()
)

print(
    "\nFirst 5 rows:"
)

print(
    df.head()
)