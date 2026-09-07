import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from calculations.employee_analysis import build_employee_analysis


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="M&A Integration Intelligence",
    page_icon="📊",
    layout="wide"
)

DATA_PATH = "data/employee_data.csv"
INPUT_PATH = "data/employee_inputs.csv"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1.5rem;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.20);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }

    .section-header {
        font-size: 1.25rem;
        font-weight: 650;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .employee-id {
        font-size: 2.2rem;
        font-weight: 750;
        margin-bottom: 0;
    }

    .employee-subtitle {
        font-size: 1rem;
        opacity: 0.7;
        margin-top: 0.2rem;
    }

    .mapi-score {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1;
    }

    .mapi-label {
        font-size: 0.85rem;
        opacity: 0.65;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .status-badge {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 20px;
        font-weight: 650;
        font-size: 0.9rem;
        margin-top: 8px;
    }

    .explanation-box {
        padding: 18px;
        border-radius: 12px;
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.20);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ROBUST CSV READER
# ============================================================

def read_csv_robust(path):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin1"
    ]

    last_error = None

    for encoding in encodings:

        try:

            return pd.read_csv(
                path,
                encoding=encoding
            )

        except UnicodeDecodeError as error:

            last_error = error

    raise last_error


# ============================================================
# LOAD + ANALYZE DATA
# ============================================================

@st.cache_data
def load_analysis():

    # --------------------------------------------------------
    # Build Employee Analysis
    # --------------------------------------------------------

    analysis = build_employee_analysis()

    # --------------------------------------------------------
    # Make Important Columns Numeric
    # --------------------------------------------------------

    numeric_columns = [
        "MDI",
        "Performance_Shock",
        "Recovery_Time",
        "Recovery_Velocity",
        "Performance_Trajectory"
    ]

    for column in numeric_columns:

        if column in analysis.columns:

            analysis[column] = pd.to_numeric(
                analysis[column],
                errors="coerce"
            )

    # --------------------------------------------------------
    # Expected Performance Shock
    # --------------------------------------------------------

    regression_data = analysis[
        [
            "MDI",
            "Performance_Shock"
        ]
    ].copy()

    regression_data["MDI"] = pd.to_numeric(
        regression_data["MDI"],
        errors="coerce"
    )

    regression_data["Performance_Shock"] = pd.to_numeric(
        regression_data["Performance_Shock"],
        errors="coerce"
    )

    regression_data = regression_data.dropna()

    # Need at least two valid observations
    if len(regression_data) >= 2:

        X = regression_data["MDI"].values
        Y = regression_data["Performance_Shock"].values

        slope, intercept = np.polyfit(
            X,
            Y,
            1
        )

    else:

        slope = 0
        intercept = regression_data["Performance_Shock"].mean()

        if pd.isna(intercept):
            intercept = 0

    analysis["Expected_Shock"] = (
        intercept +
        slope * analysis["MDI"]
    )

    # --------------------------------------------------------
    # Adaptation Residual
    # --------------------------------------------------------

    analysis["Adaptation_Residual"] = (
        analysis["Expected_Shock"]
        -
        analysis["Performance_Shock"]
    )

    # --------------------------------------------------------
    # Min-Max Normalization
    # --------------------------------------------------------

    def min_max_score(series):

        min_value = series.min()
        max_value = series.max()

        if pd.isna(min_value) or pd.isna(max_value):

            return pd.Series(
                50,
                index=series.index
            )

        if max_value == min_value:

            return pd.Series(
                50,
                index=series.index
            )

        return (
            (
                series - min_value
            )
            /
            (
                max_value - min_value
            )
        ) * 100

    # --------------------------------------------------------
    # MAPI COMPONENTS
    # --------------------------------------------------------

    analysis["Adaptation_Residual_Score"] = (
        min_max_score(
            analysis["Adaptation_Residual"]
        )
    )

    analysis["Recovery_Score"] = (
        analysis["Recovery_Time"]
        .apply(
            lambda x:
            0
            if pd.isna(x)
            else max(
                0,
                100 - (x / 12) * 100
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

    # --------------------------------------------------------
    # MAPI
    # --------------------------------------------------------

    analysis["MAPI"] = (
        0.35 *
        analysis["Adaptation_Residual_Score"]

        +

        0.30 *
        analysis["Recovery_Score"]

        +

        0.15 *
        analysis["Recovery_Velocity_Score"]

        +

        0.20 *
        analysis["Trajectory_Score"]
    )

    # --------------------------------------------------------
    # MAPI CATEGORY
    # --------------------------------------------------------

    def get_category(score):

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

    analysis["MAPI_Category"] = (
        analysis["MAPI"]
        .apply(get_category)
    )

    return analysis


analysis = load_analysis()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title(
    "M&A Integration Intelligence"
)

page = st.sidebar.radio(
    "Navigate",
    [
        "🏢 Workforce Overview",
        "👤 Employee Intelligence",
        "➕ Add Employee"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "MAPI v1 · Analytical Prototype"
)


# ################################################################
# ################################################################
#
#                    WORKFORCE OVERVIEW
#
# ################################################################
# ################################################################

if page == "🏢 Workforce Overview":

    st.title(
        "Workforce Adaptation Overview"
    )

    st.markdown(
        """
        **Organizational-level analysis of employee adaptation
        during M&A integration.**
        """
    )

    st.divider()

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    total_employees = len(analysis)

    average_mapi = analysis["MAPI"].mean()

    average_mdi = analysis["MDI"].mean()

    risk_count = (
        analysis["MAPI"] < 40
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Employees",
            total_employees
        )

    with col2:

        st.metric(
            "Average MAPI",
            f"{average_mapi:.1f}"
        )

    with col3:

        st.metric(
            "Average M&A Disruption",
            f"{average_mdi:.1f}"
        )

    with col4:

        st.metric(
            "Adaptation Risk",
            risk_count
        )

    st.divider()

    # --------------------------------------------------------
    # ADAPTATION DISTRIBUTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-header">'
        'Adaptation Distribution'
        '</div>',
        unsafe_allow_html=True
    )

    category_counts = (
        analysis["MAPI_Category"]
        .value_counts()
        .reindex(
            [
                "Highly Adaptive",
                "Adaptive",
                "Moderately Adaptive",
                "Low Adaptation",
                "Critical Adaptation Risk"
            ],
            fill_value=0
        )
    )

    st.bar_chart(
        category_counts
    )

    st.divider()

    # --------------------------------------------------------
    # DEPARTMENT ANALYSIS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-header">'
        'Department Adaptation'
        '</div>',
        unsafe_allow_html=True
    )

    department_data = (
        analysis
        .groupby("Department")
        .agg(
            MAPI=("MAPI", "mean"),
            MDI=("MDI", "mean"),
            Employees=("Employee_ID", "count")
        )
        .sort_values(
            "MAPI",
            ascending=False
        )
    )

    st.bar_chart(
        department_data[["MAPI"]]
    )

    st.dataframe(
        department_data.round(2),
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------------
    # EMPLOYEES REQUIRING ATTENTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-header">'
        'Employees Requiring Attention'
        '</div>',
        unsafe_allow_html=True
    )

    risk_employees = (
        analysis[
            analysis["MAPI"] < 40
        ]
        .sort_values(
            "MAPI"
        )
        [
            [
                "Employee_ID",
                "Department",
                "Employee_Type",
                "MDI",
                "Performance_Shock",
                "Recovery_Time",
                "MAPI",
                "MAPI_Category"
            ]
        ]
        .head(15)
    )

    st.dataframe(
        risk_employees.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Prototype risk grouping: employees with MAPI < 40."
    )

    st.divider()

    # --------------------------------------------------------
    # HIGH DISRUPTION + HIGH ADAPTATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-header">'
        'High Disruption + High Adaptation'
        '</div>',
        unsafe_allow_html=True
    )

    high_disruption = analysis[
        analysis["MDI"] >=
        analysis["MDI"].quantile(0.75)
    ]

    high_adaptation = (
        high_disruption
        .sort_values(
            "MAPI",
            ascending=False
        )
        [
            [
                "Employee_ID",
                "Department",
                "Employee_Type",
                "MDI",
                "Performance_Shock",
                "MAPI"
            ]
        ]
        .head(10)
    )

    st.dataframe(
        high_adaptation.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.info(
        """
        These employees experienced relatively high levels of
        M&A disruption while maintaining strong adaptation scores.
        They may provide useful examples of successful adaptation
        during integration.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # INTERVENTION MATRIX
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-header">'
        'M&A Adaptation Intervention Matrix'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Combines disruption exposure (MDI) with adaptation "
        "performance (MAPI) to identify potential HR responses."
    )

    mdi_threshold = analysis["MDI"].median()

    mapi_threshold = 40

    matrix_data = analysis.copy()

    def classify_employee(row):

        high_mdi = (
            row["MDI"] >= mdi_threshold
        )

        high_mapi = (
            row["MAPI"] >= mapi_threshold
        )

        if high_mdi and high_mapi:

            return "Resilient Under Pressure"

        elif high_mdi and not high_mapi:

            return "High-Priority Intervention"

        elif not high_mdi and high_mapi:

            return "Strong Adaptor"

        else:

            return "Monitor"

    matrix_data["Intervention_Group"] = (
        matrix_data.apply(
            classify_employee,
            axis=1
        )
    )

    group_order = [
        "High-Priority Intervention",
        "Resilient Under Pressure",
        "Monitor",
        "Strong Adaptor"
    ]

    group_counts = (
        matrix_data["Intervention_Group"]
        .value_counts()
        .reindex(
            group_order,
            fill_value=0
        )
    )

    matrix_col1, matrix_col2 = st.columns(2)

    with matrix_col1:

        st.markdown(
            "### Employee Groups"
        )

        st.dataframe(
            group_counts.rename(
                "Employees"
            ),
            use_container_width=True
        )

    with matrix_col2:

        st.markdown(
            "### HR Interpretation"
        )

        st.markdown(
            """
            **🔴 High-Priority Intervention**  
            High disruption + low adaptation.

            **🟢 Resilient Under Pressure**  
            High disruption + high adaptation.

            **🔵 Strong Adaptor**  
            Lower disruption + high adaptation.

            **🟡 Monitor**  
            Lower disruption + lower adaptation.
            """
        )

    # --------------------------------------------------------
    # HIGH PRIORITY
    # --------------------------------------------------------

    st.markdown(
        "### 🔴 High-Priority Intervention"
    )

    priority_employees = (
        matrix_data[
            matrix_data["Intervention_Group"]
            == "High-Priority Intervention"
        ]
        .sort_values(
            "MAPI"
        )
        [
            [
                "Employee_ID",
                "Department",
                "Employee_Type",
                "MDI",
                "MAPI",
                "Performance_Shock",
                "Recovery_Time"
            ]
        ]
        .head(15)
    )

    if len(priority_employees) > 0:

        st.dataframe(
            priority_employees.round(2),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No employees currently fall into the "
            "high-priority intervention group."
        )

    # --------------------------------------------------------
    # RESILIENT
    # --------------------------------------------------------

    st.markdown(
        "### 🟢 Resilient Under Pressure"
    )

    resilient_employees = (
        matrix_data[
            matrix_data["Intervention_Group"]
            == "Resilient Under Pressure"
        ]
        .sort_values(
            "MAPI",
            ascending=False
        )
        [
            [
                "Employee_ID",
                "Department",
                "Employee_Type",
                "MDI",
                "MAPI"
            ]
        ]
        .head(10)
    )

    if len(resilient_employees) > 0:

        st.dataframe(
            resilient_employees.round(2),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No employees currently fall into this group."
        )


# ################################################################
# ################################################################
#
#                    EMPLOYEE INTELLIGENCE
#
# ################################################################
# ################################################################

elif page == "👤 Employee Intelligence":

    st.title(
        "Employee Adaptation Intelligence"
    )

    st.markdown(
        """
        **Individual-level analysis of performance response
        during M&A integration.**
        """
    )

    employee_ids = (
        analysis["Employee_ID"]
        .sort_values()
        .tolist()
    )

    selected_employee = st.sidebar.selectbox(
        "Select Employee",
        employee_ids
    )

    employee = analysis[
        analysis["Employee_ID"]
        == selected_employee
    ].iloc[0]

    st.divider()

    # --------------------------------------------------------
    # EMPLOYEE IDENTITY
    # --------------------------------------------------------

    identity_col1, identity_col2 = st.columns(
        [2, 1]
    )

    with identity_col1:

        st.markdown(
            f"""
            <div class="employee-id">
            {employee['Employee_ID']}
            </div>

            <div class="employee-subtitle">
            {employee['Department']} ·
            {employee['Employee_Type']}
            </div>
            """,
            unsafe_allow_html=True
        )

    with identity_col2:

        st.markdown(
            f"""
            <div class="mapi-label">
            Adaptation Status
            </div>

            <div class="status-badge">
            {employee['MAPI_Category']}
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # MAPI
    # --------------------------------------------------------

    st.markdown(
        "### MAPI"
    )

    mapi_col1, mapi_col2 = st.columns(
        [1, 2]
    )

    with mapi_col1:

        st.markdown(
            f"""
            <div class="mapi-score">
            {employee['MAPI']:.1f}
            </div>

            <div class="mapi-label">
            out of 100
            </div>
            """,
            unsafe_allow_html=True
        )

    with mapi_col2:

        st.progress(
            int(
                np.clip(
                    employee["MAPI"],
                    0,
                    100
                )
            )
        )

        st.caption(
            "M&A-specific adaptation performance"
        )

    # --------------------------------------------------------
    # CORE INDICATORS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-header">'
        'Core Indicators'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "M&A Disruption",
            f"{employee['MDI']:.1f}"
        )

    with col2:

        st.metric(
            "Performance Shock",
            f"{employee['Performance_Shock']:.1f}"
        )

    with col3:

        recovery_time = employee["Recovery_Time"]

        if pd.isna(recovery_time):

            recovery_display = "Not recovered"

        else:

            recovery_display = (
                f"{recovery_time:.0f} mo"
            )

        st.metric(
            "Recovery Time",
            recovery_display
        )

    with col4:

        st.metric(
            "Performance Trajectory",
            f"{employee['Performance_Trajectory']:.2f}"
        )

    # --------------------------------------------------------
    # PERFORMANCE TRAJECTORY
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-header">'
        'Performance Trajectory'
        '</div>',
        unsafe_allow_html=True
    )

    raw_data = read_csv_robust(
        DATA_PATH
    )

    employee_history = raw_data[
        raw_data["Employee_ID"]
        == selected_employee
    ].copy()

    employee_history["Month"] = pd.to_numeric(
        employee_history["Month"],
        errors="coerce"
    )

    employee_history["Performance"] = pd.to_numeric(
        employee_history["Performance"],
        errors="coerce"
    )

    employee_history = (
        employee_history
        .dropna(
            subset=[
                "Month",
                "Performance"
            ]
        )
        .sort_values(
            "Month"
        )
    )

    fig, ax = plt.subplots(
        figsize=(10, 4)
    )

    ax.plot(
        employee_history["Month"],
        employee_history["Performance"],
        marker="o"
    )

    ax.axvline(
        x=0,
        linestyle="--"
    )

    ax.set_xlabel(
        "Months Relative to M&A"
    )

    ax.set_ylabel(
        "Performance"
    )

    ax.set_title(
        "Performance Before and After M&A"
    )

    ax.grid(
        alpha=0.25
    )

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)

    st.caption(
        "Month 0 represents the M&A event."
    )

    # --------------------------------------------------------
    # PERFORMANCE SHOCK
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-header">'
        'Performance Shock Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    shock_col1, shock_col2 = st.columns(
        [2, 1]
    )

    with shock_col1:

        observed = employee[
            "Performance_Shock"
        ]

        expected = employee[
            "Expected_Shock"
        ]

        shock_data = pd.DataFrame(
            {
                "Measure": [
                    "Expected Shock",
                    "Observed Shock"
                ],

                "Value": [
                    expected,
                    observed
                ]
            }
        )

        st.bar_chart(
            shock_data.set_index(
                "Measure"
            )
        )

    with shock_col2:

        residual = employee[
            "Adaptation_Residual"
        ]

        st.metric(
            "Adaptation Residual",
            f"{residual:+.2f}"
        )

        if residual > 5:

            st.success(
                "Better response than expected "
                "for this disruption level."
            )

        elif residual < -5:

            st.error(
                "Worse response than expected "
                "for this disruption level."
            )

        else:

            st.info(
                "Response is broadly consistent "
                "with expected disruption."
            )

    # --------------------------------------------------------
    # RECOVERY
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-header">'
        'Recovery & Sustained Adaptation'
        '</div>',
        unsafe_allow_html=True
    )

    recovery_col1, recovery_col2 = st.columns(2)

    with recovery_col1:

        st.metric(
            "Recovery Velocity",
            f"{employee['Recovery_Velocity']:.2f}"
        )

    with recovery_col2:

        st.metric(
            "Trajectory Score",
            f"{employee['Trajectory_Score']:.1f}/100"
        )

    # --------------------------------------------------------
    # COMPONENT BREAKDOWN
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-header">'
        'MAPI Component Breakdown'
        '</div>',
        unsafe_allow_html=True
    )

    component_data = pd.DataFrame(
        {
            "Component": [
                "Adaptation Response",
                "Recovery",
                "Recovery Velocity",
                "Performance Trajectory"
            ],

            "Score": [
                employee[
                    "Adaptation_Residual_Score"
                ],

                employee[
                    "Recovery_Score"
                ],

                employee[
                    "Recovery_Velocity_Score"
                ],

                employee[
                    "Trajectory_Score"
                ]
            ],

            "Weight": [
                "35%",
                "30%",
                "15%",
                "20%"
            ]
        }
    )

    component_col1, component_col2 = st.columns(
        [2, 1]
    )

    with component_col1:

        component_chart = (
            component_data
            .set_index(
                "Component"
            )["Score"]
        )

        st.bar_chart(
            component_chart
        )

    with component_col2:

        st.dataframe(
            component_data,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # HR INTERPRETATION
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-header">'
        'What HR Should Know'
        '</div>',
        unsafe_allow_html=True
    )

    mdi = employee["MDI"]

    shock = employee["Performance_Shock"]

    expected = employee["Expected_Shock"]

    residual = employee["Adaptation_Residual"]

    category = employee["MAPI_Category"]

    if residual > 5:

        response_text = (
            "The employee experienced less performance "
            "disruption than expected given the level of "
            "M&A disruption."
        )

    elif residual < -5:

        response_text = (
            "The employee experienced greater performance "
            "disruption than expected given the level of "
            "M&A disruption."
        )

    else:

        response_text = (
            "The employee's performance response was "
            "broadly consistent with the disruption "
            "experienced."
        )

    st.markdown(
        f"""
        <div class="explanation-box">

        <strong>{category}</strong>

        <br><br>

        This employee experienced an M&A disruption score of
        <strong>{mdi:.1f}/100</strong>.

        Their observed performance shock was
        <strong>{shock:.1f}</strong>, compared with an expected
        shock of approximately <strong>{expected:.1f}</strong>.

        <br><br>

        {response_text}

        <br><br>

        Overall MAPI:
        <strong>{employee['MAPI']:.1f}/100</strong>.

        </div>
        """,
        unsafe_allow_html=True
    )


# ################################################################
# ################################################################
#
#                         ADD EMPLOYEE
#
# ################################################################
# ################################################################

elif page == "➕ Add Employee":

    st.title(
        "Add Employee Data"
    )

    st.markdown(
        """
        **Enter employee information to add a new employee
        record to the M&A integration dataset.**
        """
    )

    st.divider()

    # ============================================================
    # EMPLOYEE INFORMATION
    # ============================================================

    st.markdown(
        '<div class="section-header">'
        'Employee Information'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        employee_id = st.text_input(
            "Employee ID",
            placeholder="e.g. E201"
        )

    with col2:

        department = st.selectbox(
            "Department",
            [
                "Finance",
                "HR",
                "IT",
                "Marketing",
                "Operations",
                "Sales"
            ]
        )

    with col3:

        employee_type = st.selectbox(
            "Employee Type",
            [
                "Resilient",
                "Rapid Adaptor",
                "Stable Specialist",
                "Delayed Adaptor",
                "Vulnerable",
                "Declining"
            ]
        )

    # ============================================================
    # M&A DISRUPTION
    # ============================================================

    st.divider()

    st.markdown(
        '<div class="section-header">'
        'M&A Disruption Profile'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Rate the degree of disruption experienced by the employee "
        "from 0 (no change) to 100 (extreme change)."
    )

    col1, col2 = st.columns(2)

    with col1:

        role_change = st.slider(
            "Role Change",
            0,
            100,
            50
        )

        team_change = st.slider(
            "Team Change",
            0,
            100,
            50
        )

        leadership_change = st.slider(
            "Leadership Change",
            0,
            100,
            50
        )

        technology_change = st.slider(
            "Technology Change",
            0,
            100,
            50
        )

    with col2:

        process_change = st.slider(
            "Process Change",
            0,
            100,
            50
        )

        culture_change = st.slider(
            "Culture Change",
            0,
            100,
            50
        )

        location_change = st.slider(
            "Location / Environment Change",
            0,
            100,
            50
        )

    # ============================================================
    # AUTOMATIC MDI
    # ============================================================

    disruption_values = [
        role_change,
        team_change,
        leadership_change,
        technology_change,
        process_change,
        culture_change,
        location_change
    ]

    calculated_mdi = np.mean(
        disruption_values
    )

    st.metric(
        "Calculated M&A Disruption Index",
        f"{calculated_mdi:.1f}/100"
    )

    # ============================================================
    # PERFORMANCE DATA
    # ============================================================

    st.divider()

    st.markdown(
        '<div class="section-header">'
        'Performance Data'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Enter the employee's baseline performance and "
        "performance during the M&A period."
    )

    col1, col2 = st.columns(2)

    with col1:

        baseline_performance = st.number_input(
            "Baseline Performance",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=0.1
        )

    with col2:

        merger_performance = st.number_input(
            "M&A Month Performance",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=0.1
        )

    # ============================================================
    # POST-M&A PERFORMANCE
    # ============================================================

    st.markdown(
        "### Post-M&A Performance"
    )

    st.caption(
        "Enter performance for each month after the M&A event."
    )

    post_m1 = st.number_input(
        "Month +1",
        min_value=0.0,
        max_value=100.0,
        value=float(merger_performance),
        step=0.1
    )

    post_m2 = st.number_input(
        "Month +2",
        min_value=0.0,
        max_value=100.0,
        value=float(merger_performance),
        step=0.1
    )

    post_m3 = st.number_input(
        "Month +3",
        min_value=0.0,
        max_value=100.0,
        value=float(merger_performance),
        step=0.1
    )

    post_m4 = st.number_input(
        "Month +4",
        min_value=0.0,
        max_value=100.0,
        value=float(merger_performance),
        step=0.1
    )

    post_m5 = st.number_input(
        "Month +5",
        min_value=0.0,
        max_value=100.0,
        value=float(merger_performance),
        step=0.1
    )

    post_m6 = st.number_input(
        "Month +6",
        min_value=0.0,
        max_value=100.0,
        value=float(merger_performance),
        step=0.1
    )

    # ============================================================
    # SUBMIT
    # ============================================================

    st.divider()

    submit = st.button(
        "➕ Add Employee",
        type="primary",
        use_container_width=True
    )

    if submit:

        # --------------------------------------------------------
        # Basic Validation
        # --------------------------------------------------------

        clean_employee_id = employee_id.strip()

        if clean_employee_id == "":

            st.error(
                "Please enter an Employee ID."
            )

        elif clean_employee_id in analysis[
            "Employee_ID"
        ].values:

            st.error(
                "This Employee ID already exists."
            )

        else:

            # ----------------------------------------------------
            # Build New Employee Rows
            # ----------------------------------------------------

            months = [
                -6,
                -5,
                -4,
                -3,
                -2,
                -1,
                0,
                1,
                2,
                3,
                4,
                5,
                6
            ]

            performance_values = [

                baseline_performance,
                baseline_performance,
                baseline_performance,
                baseline_performance,
                baseline_performance,
                baseline_performance,

                merger_performance,

                post_m1,
                post_m2,
                post_m3,
                post_m4,
                post_m5,
                post_m6
            ]

            new_rows = []

            for month, performance in zip(
                months,
                performance_values
            ):

                new_rows.append(
                    {
                        "Employee_ID":
                            clean_employee_id,

                        "Department":
                            department,

                        "Employee_Type":
                            employee_type,

                        "Month":
                            month,

                        "Performance":
                            performance,

                        "role_change":
                            role_change,

                        "team_change":
                            team_change,

                        "leadership_change":
                            leadership_change,

                        "technology_change":
                            technology_change,

                        "process_change":
                            process_change,

                        "culture_change":
                            culture_change,

                        "location_environment_change":
                            location_change
                    }
                )

            new_data = pd.DataFrame(
                new_rows
            )

            # ----------------------------------------------------
            # Save Input Data
            # ----------------------------------------------------

            if os.path.exists(INPUT_PATH):

                existing_inputs = read_csv_robust(
                    INPUT_PATH
                )

                combined_inputs = pd.concat(
                    [
                        existing_inputs,
                        new_data
                    ],
                    ignore_index=True
                )

            else:

                combined_inputs = new_data

            combined_inputs.to_csv(
                INPUT_PATH,
                index=False,
                encoding="utf-8"
            )

            # ----------------------------------------------------
            # Append to Working Dataset
            # ----------------------------------------------------

            existing_data = read_csv_robust(
                DATA_PATH
            )

            updated_data = pd.concat(
                [
                    existing_data,
                    new_data
                ],
                ignore_index=True
            )

            updated_data.to_csv(
                DATA_PATH,
                index=False,
                encoding="utf-8"
            )

            # ----------------------------------------------------
            # Clear Cached Analysis
            # ----------------------------------------------------

            st.cache_data.clear()

            st.success(
                f"Employee {clean_employee_id} "
                "has been successfully added."
            )

            st.info(
                """
                The employee has been added to the working
                dataset. Refresh or navigate to Employee
                Intelligence to view the updated analysis.
                """
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "M&A Integration Intelligence · Analytical Prototype · MAPI v1"
)