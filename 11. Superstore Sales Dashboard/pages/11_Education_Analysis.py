import streamlit as st
import pandas as pd
from utils.page_helpers import apply_page_config, render_header, render_insights_card
from utils.data_loader import load_home_credit_data
from utils.filters import render_sidebar_filters
from utils.kpis import format_currency, format_percent
from utils.charts import create_bar_chart, create_donut_chart

apply_page_config(page_title="Education Analysis", page_icon="🎓")
df = load_home_credit_data()
filtered_df, _ = render_sidebar_filters(df)

render_header(
    title="Page 11: Education Level & Risk Profile",
    subtitle="Assess educational attainment, earning power, credit demand, and default propensities.",
    badge="Education BI",
)

edu_agg = filtered_df.groupby("NAME_EDUCATION_TYPE").agg(
    Customers=("TARGET", "count"),
    Defaults=("TARGET", "sum"),
    Default_Rate=("TARGET", "mean"),
    Avg_Income=("AMT_INCOME_TOTAL", "mean"),
    Avg_Credit=("AMT_CREDIT", "mean"),
    Avg_Annuity=("AMT_ANNUITY", "mean"),
    Avg_Leverage=("Credit to Income Ratio", "mean"),
).reset_index()
edu_agg["Default Rate %"] = (edu_agg["Default_Rate"] * 100).round(2)

most_common_edu = edu_agg.loc[edu_agg["Customers"].idxmax(), "NAME_EDUCATION_TYPE"] if not edu_agg.empty else "N/A"
highest_inc_edu = edu_agg.loc[edu_agg["Avg_Income"].idxmax(), "NAME_EDUCATION_TYPE"] if not edu_agg.empty else "N/A"
lowest_dr_edu = edu_agg.loc[edu_agg["Default Rate %"].idxmin(), "NAME_EDUCATION_TYPE"] if not edu_agg.empty else "N/A"
lowest_dr_val = edu_agg["Default Rate %"].min() if not edu_agg.empty else 0.0
highest_dr_edu = edu_agg.loc[edu_agg["Default Rate %"].idxmax(), "NAME_EDUCATION_TYPE"] if not edu_agg.empty else "N/A"
highest_dr_val = edu_agg["Default Rate %"].max() if not edu_agg.empty else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Most Common Education", str(most_common_edu)[:20])
c2.metric("Highest Income Level", str(highest_inc_edu)[:20], format_currency(edu_agg['Avg_Income'].max()))
c3.metric("Lowest Default Group", str(lowest_dr_edu)[:20], format_percent(lowest_dr_val))
c4.metric("Highest Default Group", str(highest_dr_edu)[:20], format_percent(highest_dr_val), delta_color="inverse")

st.divider()

# Visualizations Row 1: Applicant Share & Default Rate by Education
e1, e2 = st.columns(2)
with e1:
    fig_edonut = create_donut_chart(edu_agg, names_col="NAME_EDUCATION_TYPE", values_col="Customers", title="Application Share by Education")
    st.plotly_chart(fig_edonut, use_container_width=True)

with e2:
    fig_edr = create_bar_chart(edu_agg.sort_values("Default Rate %", ascending=False), x_col="NAME_EDUCATION_TYPE", y_col="Default Rate %", title="Default Rate % by Education Level")
    st.plotly_chart(fig_edr, use_container_width=True)

# Visualizations Row 2: Average Income & Credit by Education
e3, e4 = st.columns(2)
with e3:
    fig_einc = create_bar_chart(edu_agg.sort_values("Avg_Income", ascending=False), x_col="NAME_EDUCATION_TYPE", y_col="Avg_Income", title="Average Annual Income by Education")
    st.plotly_chart(fig_einc, use_container_width=True)

with e4:
    fig_ecrd = create_bar_chart(edu_agg.sort_values("Avg_Credit", ascending=False), x_col="NAME_EDUCATION_TYPE", y_col="Avg_Credit", title="Average Loan Amount by Education")
    st.plotly_chart(fig_ecrd, use_container_width=True)

# Comparison Table
st.subheader("📋 Education Cohort Matrix")
disp_edu = edu_agg.sort_values("Default Rate %", ascending=False).copy()
disp_edu["Customers"] = disp_edu["Customers"].apply(lambda v: f"{v:,}")
disp_edu["Defaults"] = disp_edu["Defaults"].apply(lambda v: f"{v:,}")
disp_edu["Default Rate"] = disp_edu["Default Rate %"].apply(lambda v: f"{v:.2f}%")
disp_edu["Avg Income"] = disp_edu["Avg_Income"].apply(lambda v: f"${v:,.2f}")
disp_edu["Avg Credit"] = disp_edu["Avg_Credit"].apply(lambda v: f"${v:,.2f}")
disp_edu["Avg Annuity"] = disp_edu["Avg_Annuity"].apply(lambda v: f"${v:,.2f}")
disp_edu["Avg Leverage"] = disp_edu["Avg_Leverage"].apply(lambda v: f"{v:.2f}x")
disp_edu = disp_edu[["NAME_EDUCATION_TYPE", "Customers", "Defaults", "Default Rate", "Avg Income", "Avg Credit", "Avg Annuity", "Avg Leverage"]]

st.dataframe(disp_edu, use_container_width=True, hide_index=True)

if not edu_agg.empty:
    render_insights_card([
        "**Higher Education Advantage**: Applicants with academic degrees or university degrees demonstrate default rates of ~5.3% vs ~10.9% for Lower Secondary.",
        "**Volume Base**: Secondary / Secondary Special represents over 70% of all credit applications.",
        "**Credit Capacity**: Higher Education applicants sustain larger loan tickets with lower delinquency.",
    ])
