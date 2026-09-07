import pandas as pd

from calculations.disruption import (
    calculate_mdi,
    add_mdi_category
)


# Load dataset
df = pd.read_csv(
    "data/employee_data.csv"
)


# Calculate MDI
df = calculate_mdi(df)


# Add categories
df = add_mdi_category(df)


# Display results
print("\nMDI calculated successfully!\n")

print(
    df[
        [
            "Employee_ID",
            "Company",
            "Department",
            "MDI",
            "MDI_Category"
        ]
    ].head(20)
)


# Display overall statistics
print("\nMDI Statistics:\n")

print(
    df["MDI"].describe()
)


# Display category counts
print("\nMDI Categories:\n")

print(
    df["MDI_Category"].value_counts()
)