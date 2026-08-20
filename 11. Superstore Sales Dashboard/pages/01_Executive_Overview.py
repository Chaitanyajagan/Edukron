import streamlit as st
import pandas as pd
from utils.page_helpers import apply_page_config, render_header, render_insights_card
from utils.data_loader import load_home_credit_data
from utils.filters import render_sidebar_filters
from utils.kpis import calculate_home_credit_kpis, format_currency, format_percent, format_number
from utils.charts import create_donut_chart, create_bar_chart, create_histogram

apply_page_config(page_title="Executive Overview", page_icon="📈")
df = load_home_credit_data()
filtered_df, _ = render_sidebar_filters(df)

render_header(
    title="Page 1: Executive Overview",
    subtitle="High-level executive picture of credit applicants, loan default rates, and capital exposure.",
    badge="Executive View",
)

kpis = calculate_home_credit_kpis(filtered_df)

# Pure Streamlit Metrics
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Applications", format_number(kpis["total_applications"]))
c2.metric("Default Customers", format_number(kpis["default_customers"]), f"{format_percent(kpis['default_rate'])} Default Rate", delta_color="inverse")
c3.metric("Total Credit Exposure", format_currency(kpis["total_credit"]))
c4.metric("Avg Customer Income", format_currency(kpis["avg_income"]))
c5.metric("Avg Client Age", f"{kpis['avg_age']:.1f} Yrs")

st.divider()

# Visualizations Row 1: Default vs Non-Default & Gender
r1, r2 = st.columns([3, 2])
with r1:
    target_counts = filtered_df["Target Label"].value_counts().reset_index()
    target_counts.columns = ["Status", "Count"]
    fig_target = create_donut_chart(target_counts, names_col="Status", values_col="Count", title="Default vs Non-Default Applicants")
    st.plotly_chart(fig_target, use_container_width=True)

with r2:
    gender_agg = filtered_df[filtered_df["CODE_GENDER"] != "XNA"].groupby("CODE_GENDER")["TARGET"].count().reset_index()
    gender_agg.columns = ["Gender", "Applications"]
    fig_gender = create_bar_chart(gender_agg, x_col="Gender", y_col="Applications", title="Applications by Gender", color_col="Gender")
    st.plotly_chart(fig_gender, use_container_width=True)

# Visualizations Row 2: Contract Type & Income Type
r3, r4 = st.columns(2)
with r3:
    contract_agg = filtered_df.groupby("NAME_CONTRACT_TYPE")["TARGET"].agg(Total="count", Default_Rate="mean").reset_index()
    contract_agg["Default Rate %"] = (contract_agg["Default_Rate"] * 100).round(2)
    fig_contract = create_bar_chart(contract_agg, x_col="NAME_CONTRACT_TYPE", y_col="Default Rate %", title="Default Rate by Contract Type")
    st.plotly_chart(fig_contract, use_container_width=True)

with r4:
    inc_agg = filtered_df.groupby("NAME_INCOME_TYPE")["TARGET"].agg(Total="count", Default_Rate="mean").reset_index()
    inc_agg["Default Rate %"] = (inc_agg["Default_Rate"] * 100).round(2)
    top_inc = inc_agg.sort_values("Total", ascending=False).head(5)
    fig_inc = create_bar_chart(top_inc, x_col="NAME_INCOME_TYPE", y_col="Default Rate %", title="Default Rate by Top Income Types")
    st.plotly_chart(fig_inc, use_container_width=True)

# Visualizations Row 3: Credit Amount Distribution
st.subheader("💳 Credit Amount Distribution")
fig_credit_hist = create_histogram(filtered_df[filtered_df["AMT_CREDIT"] < 2000000], col="AMT_CREDIT", nbins=40, title="Credit Amount Distribution (Under $2M)")
st.plotly_chart(fig_credit_hist, use_container_width=True)

if not filtered_df.empty:
    common_inc = filtered_df["NAME_INCOME_TYPE"].mode().iloc[0] if "NAME_INCOME_TYPE" in filtered_df.columns else "N/A"
    common_edu = filtered_df["NAME_EDUCATION_TYPE"].mode().iloc[0] if "NAME_EDUCATION_TYPE" in filtered_df.columns else "N/A"
    render_insights_card([
        f"**Baseline Default Rate**: **{format_percent(kpis['default_rate'])}** of applicants encounter significant repayment difficulties.",
        f"**Average Loan vs Income**: Applicants borrow an average of **{format_currency(kpis['avg_credit'])}** against an average income of **{format_currency(kpis['avg_income'])}**.",
        f"**Most Common Applicant Profile**: **{common_inc}** with **{common_edu}** background.",
    ])
