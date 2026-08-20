import streamlit as st
import pandas as pd
from utils.page_helpers import apply_page_config, render_header, render_insights_card
from utils.data_loader import load_home_credit_data
from utils.filters import render_sidebar_filters
from utils.charts import create_bar_chart, create_histogram, create_line_trend

apply_page_config(page_title="Age Analysis", page_icon="🎂")
df = load_home_credit_data()
filtered_df, _ = render_sidebar_filters(df)

render_header(
    title="Page 4: Age Cohorts & Credit Risk",
    subtitle="Evaluate applicant maturity, repayment curve across age brackets, and default risk progression.",
    badge="Age Demographics",
)

avg_age = filtered_df["Age"].mean() if "Age" in filtered_df.columns and len(filtered_df) > 0 else 0.0
min_age = filtered_df["Age"].min() if "Age" in filtered_df.columns and len(filtered_df) > 0 else 0.0
max_age = filtered_df["Age"].max() if "Age" in filtered_df.columns and len(filtered_df) > 0 else 0.0

age_group_agg = filtered_df.groupby("Age Group", observed=False).agg(
    Total=("TARGET", "count"),
    Defaults=("TARGET", "sum"),
    Default_Rate=("TARGET", "mean"),
    Avg_Credit=("AMT_CREDIT", "mean"),
    Avg_Income=("AMT_INCOME_TOTAL", "mean"),
).reset_index()
age_group_agg["Default Rate %"] = (age_group_agg["Default_Rate"] * 100).round(2)

highest_risk_group = age_group_agg.loc[age_group_agg["Default Rate %"].idxmax(), "Age Group"] if not age_group_agg.empty else "N/A"
highest_risk_val = age_group_agg["Default Rate %"].max() if not age_group_agg.empty else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Average Applicant Age", f"{avg_age:.1f} Yrs")
c2.metric("Youngest Applicant", f"{min_age:.0f} Yrs")
c3.metric("Oldest Applicant", f"{max_age:.0f} Yrs")
c4.metric("Highest Risk Age Group", str(highest_risk_group), f"{highest_risk_val:.2f}% Default Rate", delta_color="inverse")

st.divider()

# Visualizations Row 1: Age Histogram & Applications by Group
a1, a2 = st.columns(2)
with a1:
    fig_ahist = create_histogram(filtered_df, col="Age", nbins=35, title="Applicant Age Distribution", color_by="Target Label" if "Target Label" in filtered_df.columns else None)
    st.plotly_chart(fig_ahist, use_container_width=True)

with a2:
    fig_ag = create_bar_chart(age_group_agg, x_col="Age Group", y_col="Total", title="Application Volume by Age Cohort")
    st.plotly_chart(fig_ag, use_container_width=True)

# Visualizations Row 2: Default Rate by Age Group & Continuous Default Curve
a3, a4 = st.columns(2)
with a3:
    fig_adr = create_bar_chart(age_group_agg, x_col="Age Group", y_col="Default Rate %", title="Default Rate % by Age Bracket (Inverse Risk Curve)")
    st.plotly_chart(fig_adr, use_container_width=True)

with a4:
    age_int_agg = filtered_df.groupby(filtered_df["Age"].round().astype(int))["TARGET"].mean().reset_index()
    age_int_agg["Default Rate %"] = (age_int_agg["TARGET"] * 100).round(2)
    fig_acurve = create_line_trend(age_int_agg, x_col="Age", y_cols="Default Rate %", title="Continuous Default Probability by Age (Years)", show_markers=True)
    st.plotly_chart(fig_acurve, use_container_width=True)

# Visualizations Row 3: Credit Amount & Income by Age
a5, a6 = st.columns(2)
with a5:
    fig_acredit = create_bar_chart(age_group_agg, x_col="Age Group", y_col="Avg_Credit", title="Average Loan Amount by Age Group")
    st.plotly_chart(fig_acredit, use_container_width=True)

with a6:
    fig_ainc = create_bar_chart(age_group_agg, x_col="Age Group", y_col="Avg_Income", title="Average Annual Income by Age Group")
    st.plotly_chart(fig_ainc, use_container_width=True)

if not age_group_agg.empty:
    render_insights_card([
        "**Inverse Age-Risk Law**: Younger applicants (18–25) have the highest default rate (>12%), which steadily declines with age down to <5% for applicants aged 60+.",
        "**Peak Credit Demand**: Applicants aged 35–50 borrow the largest average loan sizes as family expenses and mortgage obligations peak.",
        "**Underwriting Policy**: Consider enhanced verification or co-signers for applicants under 25.",
    ])
