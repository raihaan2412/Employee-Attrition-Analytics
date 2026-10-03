import pandas as pd
df = pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")

columns_to_remove = [
    "EmployeeCount",
    "EmployeeNumber",
    "Over18",
    "StandardHours"
]

df = df.drop(columns=columns_to_remove)

df = df.drop_duplicates()

df["AttritionFlag"] = df["Attrition"].map({
    "Yes": 1,
    "No": 0
})

df["TenureBand"] = pd.cut(
    df["YearsAtCompany"],
    bins=[-1, 2, 5, 10, float("inf")],
    labels=[
        "0-2 Years",
        "3-5 Years",
        "6-10 Years",
        "10+ Years"
    ]
)

df["IncomeBand"] = pd.qcut(
    df["MonthlyIncome"],
    q=4,
    labels=[
        "Low",
        "Medium",
        "High",
        "Very High"
    ]
)

def analyze_attrition(column):

    result = (
        df.groupby(column, observed=True)
        .agg(
            Employees=("AttritionFlag", "count"),
            Employees_Left=("AttritionFlag", "sum"),
            Attrition_Rate=("AttritionFlag", "mean")
        )
        .reset_index()
    )

    result["Attrition_Rate"] *= 100

    return result.sort_values(
        "Attrition_Rate",
        ascending=False
    )

satisfaction_analysis = analyze_attrition(
    "JobSatisfaction"
)

print("\n========== ATTRITION BY JOB SATISFACTION ==========")
print(satisfaction_analysis)
worklife_analysis = analyze_attrition(
    "WorkLifeBalance"
)

print("\n========== ATTRITION BY WORK LIFE BALANCE ==========")
print(worklife_analysis)


involvement_analysis = analyze_attrition(
    "JobInvolvement"
)

print("\n========== ATTRITION BY JOB INVOLVEMENT ==========")
print(involvement_analysis)


travel_analysis = analyze_attrition(
    "BusinessTravel"
)

print("\n========== ATTRITION BY BUSINESS TRAVEL ==========")
print(travel_analysis)
# ==========================================
# STATISTICAL ANALYSIS
# CHI-SQUARE TEST
# ==========================================

from scipy.stats import chi2_contingency


def chi_square_test(column):

    table = pd.crosstab(
        df[column],
        df["Attrition"]
    )

    chi2, p_value, degrees_of_freedom, expected = chi2_contingency(table)

    result = "Significant" if p_value < 0.05 else "Not Significant"

    print(f"\n========== {column} vs ATTRITION ==========")
    print(f"Chi-Square Statistic : {chi2:.4f}")
    print(f"P-Value              : {p_value:.6f}")
    print(f"Degrees of Freedom   : {degrees_of_freedom}")
    print(f"Result               : {result}")
chi_square_test("OverTime")
chi_square_test("JobSatisfaction")
chi_square_test("WorkLifeBalance")
chi_square_test("JobInvolvement")
chi_square_test("BusinessTravel")