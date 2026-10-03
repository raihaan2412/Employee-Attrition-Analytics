import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Employee Attrition Analytics",
    page_icon="👥",
    layout="wide"
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #0F172A;
            color: #FFFFFF;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3 {
            color: #FFFFFF;
        }

        .subtitle {
            color: #CBD5E1;
            font-size: 16px;
            margin-top: -10px;
            margin-bottom: 25px;
        }

        .kpi-card {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 20px;
            text-align: center;
            margin-bottom: 10px;
        }

        .kpi-title {
            color: #CBD5E1;
            font-size: 14px;
            margin-bottom: 8px;
        }

        .kpi-value {
            color: #22D3EE;
            font-size: 28px;
            font-weight: 700;
        }

        .section-card {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 20px;
            margin-top: 20px;
        }

        .insight-box {
            background-color: #1E293B;
            border-left: 4px solid #22D3EE;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
        }

        .recommendation-box {
            background-color: #1E293B;
            border-left: 4px solid #22C55E;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
        }

        div[data-testid="stMetric"] {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_data():
    df = pd.read_csv("data/employee_attrition_cleaned.csv")
    return df


df = load_data()


st.title("👥 Employee Attrition Analytics")

st.markdown(
    """
    <div class="subtitle">
        Workforce Retention • Attrition Patterns • Employee Experience • Data-Driven Insights
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("🔎 Dashboard Filters")

# Department
department_options = sorted(df["Department"].dropna().unique())

selected_departments = st.sidebar.multiselect(
    "Department",
    department_options,
    default=department_options
)


job_role_options = sorted(df["JobRole"].dropna().unique())

selected_job_roles = st.sidebar.multiselect(
    "Job Role",
    job_role_options,
    default=job_role_options
)

overtime_options = sorted(df["OverTime"].dropna().unique())

selected_overtime = st.sidebar.multiselect(
    "Overtime",
    overtime_options,
    default=overtime_options
)


tenure_options = [
    "0-2 Years",
    "3-5 Years",
    "6-10 Years",
    "10+ Years"
]

selected_tenure = st.sidebar.multiselect(
    "Tenure",
    tenure_options,
    default=tenure_options
)

filtered_df = df[
    df["Department"].isin(selected_departments)
    & df["JobRole"].isin(selected_job_roles)
    & df["OverTime"].isin(selected_overtime)
    & df["TenureBand"].isin(selected_tenure)
].copy()

total_employees = len(filtered_df)

employees_left = filtered_df["AttritionFlag"].sum()

attrition_rate = (
    employees_left / total_employees * 100
    if total_employees > 0
    else 0
)

avg_years_company = (
    filtered_df["YearsAtCompany"].mean()
    if total_employees > 0
    else 0
)

avg_monthly_income = (
    filtered_df["MonthlyIncome"].mean()
    if total_employees > 0
    else 0
)

st.subheader("📊 Workforce Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Employees</div>
            <div class="kpi-value">{total_employees:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Employees Left</div>
            <div class="kpi-value">{employees_left:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Attrition Rate</div>
            <div class="kpi-value">{attrition_rate:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Avg Monthly Income</div>
            <div class="kpi-value">${avg_monthly_income:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


if filtered_df.empty:

    st.warning(
        "⚠️ No employees match the selected filters. "
        "Please change the filters."
    )

    st.stop()

department_data = (
    filtered_df
    .groupby("Department")
    .agg(
        Employees=("AttritionFlag", "count"),
        Employees_Left=("AttritionFlag", "sum")
    )
    .reset_index()
)

department_data["Attrition Rate"] = (
    department_data["Employees_Left"]
    / department_data["Employees"]
    * 100
)

fig_department = px.bar(
    department_data,
    x="Department",
    y="Attrition Rate",
    text="Attrition Rate",
    title="Attrition Rate by Department"
)

fig_department.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_department.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="#FFFFFF",
    yaxis_title="Attrition Rate (%)",
    xaxis_title="Department"
)

role_data = (
    filtered_df
    .groupby("JobRole")
    .agg(
        Employees=("AttritionFlag", "count"),
        Employees_Left=("AttritionFlag", "sum")
    )
    .reset_index()
)

role_data["Attrition Rate"] = (
    role_data["Employees_Left"]
    / role_data["Employees"]
    * 100
)

role_data = role_data.sort_values(
    "Attrition Rate",
    ascending=True
)

fig_role = px.bar(
    role_data,
    x="Attrition Rate",
    y="JobRole",
    orientation="h",
    text="Attrition Rate",
    title="Attrition Rate by Job Role"
)

fig_role.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_role.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="#FFFFFF",
    xaxis_title="Attrition Rate (%)",
    yaxis_title="Job Role"
)

tenure_data = (
    filtered_df
    .groupby("TenureBand")
    .agg(
        Employees=("AttritionFlag", "count"),
        Employees_Left=("AttritionFlag", "sum")
    )
    .reset_index()
)

tenure_data["Attrition Rate"] = (
    tenure_data["Employees_Left"]
    / tenure_data["Employees"]
    * 100
)

tenure_data["TenureBand"] = pd.Categorical(
    tenure_data["TenureBand"],
    categories=tenure_options,
    ordered=True
)

tenure_data = tenure_data.sort_values("TenureBand")

fig_tenure = px.bar(
    tenure_data,
    x="TenureBand",
    y="Attrition Rate",
    text="Attrition Rate",
    title="Attrition Rate by Tenure"
)

fig_tenure.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_tenure.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="#FFFFFF",
    yaxis_title="Attrition Rate (%)",
    xaxis_title="Tenure"
)

income_data = (
    filtered_df
    .groupby("IncomeBand")
    .agg(
        Employees=("AttritionFlag", "count"),
        Employees_Left=("AttritionFlag", "sum")
    )
    .reset_index()
)

income_data["Attrition Rate"] = (
    income_data["Employees_Left"]
    / income_data["Employees"]
    * 100
)

income_order = [
    "Low",
    "Medium",
    "High",
    "Very High"
]

income_data["IncomeBand"] = pd.Categorical(
    income_data["IncomeBand"],
    categories=income_order,
    ordered=True
)

income_data = income_data.sort_values("IncomeBand")

fig_income = px.bar(
    income_data,
    x="IncomeBand",
    y="Attrition Rate",
    text="Attrition Rate",
    title="Attrition Rate by Income Band"
)

fig_income.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_income.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="#FFFFFF",
    yaxis_title="Attrition Rate (%)",
    xaxis_title="Income Band"
)

overtime_data = (
    filtered_df
    .groupby("OverTime")
    .agg(
        Employees=("AttritionFlag", "count"),
        Employees_Left=("AttritionFlag", "sum")
    )
    .reset_index()
)

overtime_data["Attrition Rate"] = (
    overtime_data["Employees_Left"]
    / overtime_data["Employees"]
    * 100
)

fig_overtime = px.bar(
    overtime_data,
    x="OverTime",
    y="Attrition Rate",
    text="Attrition Rate",
    title="Attrition Rate by Overtime"
)

fig_overtime.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_overtime.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="#FFFFFF",
    yaxis_title="Attrition Rate (%)",
    xaxis_title="Overtime"
)

satisfaction_data = (
    filtered_df
    .groupby("JobSatisfaction")
    .agg(
        Employees=("AttritionFlag", "count"),
        Employees_Left=("AttritionFlag", "sum")
    )
    .reset_index()
)

satisfaction_data["Attrition Rate"] = (
    satisfaction_data["Employees_Left"]
    / satisfaction_data["Employees"]
    * 100
)

fig_satisfaction = px.bar(
    satisfaction_data,
    x="JobSatisfaction",
    y="Attrition Rate",
    text="Attrition Rate",
    title="Attrition Rate by Job Satisfaction"
)

fig_satisfaction.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_satisfaction.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="#FFFFFF",
    xaxis_title="Job Satisfaction Level",
    yaxis_title="Attrition Rate (%)"
)


st.subheader("📈 Attrition Analysis")

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.plotly_chart(
        fig_department,
        width="stretch"
    )

with row1_col2:
    st.plotly_chart(
        fig_role,
        width="stretch"
    )


row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.plotly_chart(
        fig_tenure,
        width="stretch"
    )

with row2_col2:
    st.plotly_chart(
        fig_income,
        width="stretch"
    )


row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.plotly_chart(
        fig_overtime,
        width="stretch"
    )

with row3_col2:
    st.plotly_chart(
        fig_satisfaction,
        width="stretch"
    )

st.subheader("💡 Key Insights")

department_rates = (
    filtered_df
    .groupby("Department")["AttritionFlag"]
    .mean()
    * 100
)

if not department_rates.empty:
    highest_department = department_rates.idxmax()
    highest_department_rate = department_rates.max()

    lowest_department = department_rates.idxmin()
    lowest_department_rate = department_rates.min()

else:
    highest_department = "N/A"
    highest_department_rate = 0
    lowest_department = "N/A"
    lowest_department_rate = 0



tenure_rates = (
    filtered_df
    .groupby("TenureBand")["AttritionFlag"]
    .mean()
    * 100
)

if not tenure_rates.empty:
    highest_tenure = tenure_rates.idxmax()
    highest_tenure_rate = tenure_rates.max()
else:
    highest_tenure = "N/A"
    highest_tenure_rate = 0

overtime_rates = (
    filtered_df
    .groupby("OverTime")["AttritionFlag"]
    .mean()
    * 100
)

if not overtime_rates.empty:
    highest_overtime = overtime_rates.idxmax()
    highest_overtime_rate = overtime_rates.max()
else:
    highest_overtime = "N/A"
    highest_overtime_rate = 0

income_rates = (
    filtered_df
    .groupby("IncomeBand")["AttritionFlag"]
    .mean()
    * 100
)

if not income_rates.empty:
    highest_income_band = income_rates.idxmax()
    highest_income_rate = income_rates.max()
else:
    highest_income_band = "N/A"
    highest_income_rate = 0


insight1, insight2 = st.columns(2)

with insight1:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>🏢 Department Pattern</b><br>
            {highest_department} has the highest attrition rate
            at <b>{highest_department_rate:.1f}%</b> among the
            selected employees.
        </div>
        """,
        unsafe_allow_html=True
    )

with insight2:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>⏳ Tenure Pattern</b><br>
            The <b>{highest_tenure}</b> group has the highest
            attrition rate at <b>{highest_tenure_rate:.1f}%</b>.
        </div>
        """,
        unsafe_allow_html=True
    )


insight3, insight4 = st.columns(2)

with insight3:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>⏰ Overtime Pattern</b><br>
            Employees with <b>{highest_overtime}</b> overtime status
            show the highest attrition rate at
            <b>{highest_overtime_rate:.1f}%</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

with insight4:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>💰 Income Pattern</b><br>
            The <b>{highest_income_band}</b> income band has the
            highest attrition rate at
            <b>{highest_income_rate:.1f}%</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

st.subheader("🎯 Recommendations")

recommendation1, recommendation2 = st.columns(2)

with recommendation1:

    st.markdown(
        """
        <div class="recommendation-box">
            <b>1. ⏰ Manage Excessive Overtime</b><br>
            Review workload distribution, overtime frequency and
            staffing requirements to reduce employee burnout.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="recommendation-box">
            <b>2. 🌱 Strengthen Early-Tenure Support</b><br>
            Improve onboarding, mentoring and employee support
            during the first few years of employment.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="recommendation-box">
            <b>3. 🧑‍💼 Focus on High-Risk Roles</b><br>
            Investigate roles with consistently high attrition
            and identify workload, career-growth or compensation
            concerns.
        </div>
        """,
        unsafe_allow_html=True
    )


with recommendation2:

    st.markdown(
        """
        <div class="recommendation-box">
            <b>4. 😊 Improve Employee Experience</b><br>
            Strengthen job satisfaction, work-life balance and
            employee engagement initiatives.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="recommendation-box">
            <b>5. 💰 Review Compensation & Growth</b><br>
            Review compensation and career progression opportunities,
            particularly for employees in lower income bands.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="recommendation-box">
            <b>6. 📊 Use Data for Retention Planning</b><br>
            Monitor high-risk groups regularly and use attrition
            patterns to guide targeted retention strategies.
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#CBD5E1; font-size:13px;">
        📌 Note: This dataset does not contain employee hire or exit dates,
        so true monthly or annual attrition trends cannot be calculated.
        Observed relationships indicate association, not causation.
    </div>
    """,
    unsafe_allow_html=True
)