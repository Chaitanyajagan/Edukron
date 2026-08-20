import streamlit as st
import pandas as pd
from utils.page_helpers import apply_page_config, render_header, render_insights_card
from utils.data_loader import load_home_credit_data
from utils.filters import render_sidebar_filters
from utils.kpis import format_percent
from utils.charts import create_bar_chart, create_histogram, create_scatter_plot

apply_page_config(page_title="Income vs Credit", page_icon="⚖️")
df = load_home_credit_data()
filtered_df, _ = render_sidebar_filters(df)

render_header(
    title="Page 9: Credit-to-Income Leverage Analysis",
    subtitle="Evaluate borrowing leverage, debt-to-income multiples, and over-indebtedness risk.",
    badge="Leverage Ratios",
)

avg_ratio = filtered_df["Credit to Income Ratio"].mean() if "Credit to Income Ratio" in filtered_df.columns else 0.0
max_ratio = filtered_df["Credit to Income Ratio"].max() if "Credit to Income Ratio" in filtered_df.columns else 0.0

high_ratio_df = filtered_df[filtered_df["Credit to Income Ratio"] > 4.0] if "Credit to Income Ratio" in filtered_df.columns else pd.DataFrame()
high_ratio_dr = high_ratio_df["TARGET"].mean() * 100 if not high_ratio_df.empty else 0.0

c1, c2, c3 = st.columns(3)
c1.metric("Average Leverage Multiple", f"{avg_ratio:.2f}x", "Credit / Income")
c2.metric("Max Leverage Multiple", f"{max_ratio:.1f}x", "Peak Ratio")
c3.metric("High Leverage Default Rate", format_percent(high_ratio_dr), "For Ratio > 4.0x", delta_color="inverse")

st.divider()

# Risk Groups Aggregation
if "Credit Leverage Group" in filtered_df.columns:
    lev_agg = filtered_df.groupby("Credit Leverage Group", observed=False).agg(
        Customers=("TARGET", "count"),
        Default_Rate=("TARGET", "mean"),
    ).reset_index()
    lev_agg["Default Rate %"] = (lev_agg["Default_Rate"] * 100).round(2)

# Visualizations Row 1: Leverage Multiple Distribution & Volume by Bracket
lv1, lv2 = st.columns(2)
with lv1:
    fig_rhist = create_histogram(filtered_df[filtered_df["Credit to Income Ratio"] <= 12], col="Credit to Income Ratio", nbins=40, title="Credit-to-Income Multiple Distribution", color_by="Target Label")
    st.plotly_chart(fig_rhist, use_container_width=True)

with lv2:
    fig_lg = create_bar_chart(lev_agg, x_col="Credit Leverage Group", y_col="Customers", title="Applicants by Leverage Tier")
    st.plotly_chart(fig_lg, use_container_width=True)

# Visualizations Row 2: Default Rate by Leverage Group & Scatter Plot
lv3, lv4 = st.columns(2)
with lv3:
    fig_ldr = create_bar_chart(lev_agg, x_col="Credit Leverage Group", y_col="Default Rate %", title="Default Rate % by Credit Leverage Tier")
    st.plotly_chart(fig_ldr, use_container_width=True)

with lv4:
    sample_ci = filtered_df[(filtered_df["AMT_INCOME_TOTAL"] <= 500000) & (filtered_df["AMT_CREDIT"] <= 1500000)].sample(min(2000, len(filtered_df)), random_state=42)
    fig_ciscat = create_scatter_plot(sample_ci, x_col="AMT_INCOME_TOTAL", y_col="AMT_CREDIT", color_col="Credit Leverage Group", title="Income vs Credit by Leverage Tier")
    st.plotly_chart(fig_ciscat, use_container_width=True)

# Visualizations Row 3: Gender & Education Leverage
lv5, lv6 = st.columns(2)
with lv5:
    g_lev = filtered_df[filtered_df["CODE_GENDER"] != "XNA"].groupby("CODE_GENDER")["Credit to Income Ratio"].mean().reset_index()
    fig_glev = create_bar_chart(g_lev, x_col="CODE_GENDER", y_col="Credit to Income Ratio", title="Average Leverage Multiple by Gender", color_col="CODE_GENDER")
    st.plotly_chart(fig_glev, use_container_width=True)

with lv6:
    e_lev = filtered_df.groupby("NAME_EDUCATION_TYPE")["Credit to Income Ratio"].mean().reset_index().sort_values("Credit to Income Ratio", ascending=False)
    fig_elev = create_bar_chart(e_lev, x_col="NAME_EDUCATION_TYPE", y_col="Credit to Income Ratio", title="Average Leverage Multiple by Education")
    st.plotly_chart(fig_elev, use_container_width=True)

if not filtered_df.empty:
    render_insights_card([
        "**Prudent Leverage Zone (< 2x)**: Loans under 2x annual income maintain lower default rates (~5.8%).",
        "**High Risk Threshold (> 6x)**: When requested credit exceeds 6x annual income, default probability spikes dramatically.",
        "**Underwriting Cap**: Recommend capping unsecured cash credit at 4x verified annual income.",
    ])
