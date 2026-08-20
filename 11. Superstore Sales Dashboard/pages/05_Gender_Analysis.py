import streamlit as st
import pandas as pd
from utils.page_helpers import apply_page_config, render_header, render_insights_card
from utils.data_loader import load_home_credit_data
from utils.filters import render_sidebar_filters
from utils.kpis import format_percent, format_number
from utils.charts import create_bar_chart, create_donut_chart

apply_page_config(page_title="Gender Analysis", page_icon="👤")
df = load_home_credit_data()
filtered_df, _ = render_sidebar_filters(df)

render_header(
    title="Page 5: Gender-Wise Credit Analysis",
    subtitle="Comparative evaluation of application volume, default propensities, income levels, and loan sizes by gender.",
    badge="Gender Demographics",
)

gender_df = filtered_df[filtered_df["CODE_GENDER"] != "XNA"]
gender_agg = gender_df.groupby("CODE_GENDER").agg(
    Customers=("TARGET", "count"),
    Defaults=("TARGET", "sum"),
    Default_Rate=("TARGET", "mean"),
    Avg_Income=("AMT_INCOME_TOTAL", "mean"),
    Avg_Credit=("AMT_CREDIT", "mean"),
    Avg_Annuity=("AMT_ANNUITY", "mean"),
).reset_index()
gender_agg["Default Rate %"] = (gender_agg["Default_Rate"] * 100).round(2)

male_row = gender_agg[gender_agg["CODE_GENDER"] == "M"]
female_row = gender_agg[gender_agg["CODE_GENDER"] == "F"]

male_count = male_row["Customers"].iloc[0] if not male_row.empty else 0
female_count = female_row["Customers"].iloc[0] if not female_row.empty else 0
male_dr = male_row["Default Rate %"].iloc[0] if not male_row.empty else 0.0
female_dr = female_row["Default Rate %"].iloc[0] if not female_row.empty else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Male Applicants", format_number(male_count), f"{(male_count/len(gender_df)*100):.1f}% of Total" if len(gender_df)>0 else "")
c2.metric("Female Applicants", format_number(female_count), f"{(female_count/len(gender_df)*100):.1f}% of Total" if len(gender_df)>0 else "")
c3.metric("Male Default Rate", format_percent(male_dr), "Higher Default Risk", delta_color="inverse")
c4.metric("Female Default Rate", format_percent(female_dr), "Lower Default Risk")

st.divider()

# Visualizations Row 1: Applicants & Defaults Count
g1, g2 = st.columns(2)
with g1:
    fig_gapp = create_donut_chart(gender_agg, names_col="CODE_GENDER", values_col="Customers", title="Application Share by Gender")
    st.plotly_chart(fig_gapp, use_container_width=True)

with g2:
    fig_gdef = create_bar_chart(gender_agg, x_col="CODE_GENDER", y_col="Defaults", title="Default Volume by Gender", color_col="CODE_GENDER")
    st.plotly_chart(fig_gdef, use_container_width=True)

# Visualizations Row 2: Default Rate & Income
g3, g4 = st.columns(2)
with g3:
    fig_gdr = create_bar_chart(gender_agg, x_col="CODE_GENDER", y_col="Default Rate %", title="Default Rate % by Gender", color_col="CODE_GENDER")
    st.plotly_chart(fig_gdr, use_container_width=True)

with g4:
    fig_ginc = create_bar_chart(gender_agg, x_col="CODE_GENDER", y_col="Avg_Income", title="Average Annual Income by Gender", color_col="CODE_GENDER")
    st.plotly_chart(fig_ginc, use_container_width=True)

# Visualizations Row 3: Credit & Annuity
g5, g6 = st.columns(2)
with g5:
    fig_gcrd = create_bar_chart(gender_agg, x_col="CODE_GENDER", y_col="Avg_Credit", title="Average Loan Amount by Gender", color_col="CODE_GENDER")
    st.plotly_chart(fig_gcrd, use_container_width=True)

with g6:
    fig_gann = create_bar_chart(gender_agg, x_col="CODE_GENDER", y_col="Avg_Annuity", title="Average Annuity Obligation by Gender", color_col="CODE_GENDER")
    st.plotly_chart(fig_gann, use_container_width=True)

# Comparison Table
st.subheader("📋 Gender Comparison Benchmark Table")
disp_gender = gender_agg.copy()
disp_gender["Gender"] = disp_gender["CODE_GENDER"].map({"M": "Male", "F": "Female"})
disp_gender["Customers"] = disp_gender["Customers"].apply(lambda v: f"{v:,}")
disp_gender["Defaults"] = disp_gender["Defaults"].apply(lambda v: f"{v:,}")
disp_gender["Default Rate"] = disp_gender["Default Rate %"].apply(lambda v: f"{v:.2f}%")
disp_gender["Avg Income"] = disp_gender["Avg_Income"].apply(lambda v: f"${v:,.2f}")
disp_gender["Avg Credit"] = disp_gender["Avg_Credit"].apply(lambda v: f"${v:,.2f}")
disp_gender["Avg Annuity"] = disp_gender["Avg_Annuity"].apply(lambda v: f"${v:,.2f}")
disp_gender = disp_gender[["Gender", "Customers", "Defaults", "Default Rate", "Avg Income", "Avg Credit", "Avg Annuity"]]

st.dataframe(disp_gender, use_container_width=True, hide_index=True)

if not gender_agg.empty:
    render_insights_card([
        "**Volume vs Risk Paradox**: Females submit ~66% of all applications, yet have a significantly lower default rate (~7.0% vs ~10.1% for males).",
        "**Income Disparity**: Male applicants declare ~20-25% higher average income and borrow slightly higher loan tickets.",
        "**Credit Stability**: Female borrowers demonstrate superior loan repayment consistency across all age cohorts.",
    ])
