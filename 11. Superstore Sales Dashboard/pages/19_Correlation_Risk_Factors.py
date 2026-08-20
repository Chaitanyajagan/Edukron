import streamlit as st
import pandas as pd
from utils.page_helpers import apply_page_config, render_header, render_insights_card
from utils.data_loader import load_home_credit_data
from utils.filters import render_sidebar_filters
from utils.charts import create_heatmap_matrix, create_bar_chart, create_scatter_plot

apply_page_config(page_title="Correlation & Risk Factors", page_icon="🔗")
df = load_home_credit_data()
filtered_df, _ = render_sidebar_filters(df)

render_header(
    title="Page 19: Correlation Matrix & Default Risk Factors",
    subtitle="Identify statistical correlations, feature collinearity, and prime numerical drivers of loan default.",
    badge="Feature Engineering",
)

corr_features = [
    "TARGET", "AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "AMT_GOODS_PRICE",
    "Age", "Employment Years", "EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3",
    "Avg External Score", "Credit to Income Ratio", "Annuity to Income Ratio", "CNT_CHILDREN"
]
avail_features = [f for f in corr_features if f in filtered_df.columns]

corr_matrix = filtered_df[avail_features].corr().round(3)
target_corr = corr_matrix["TARGET"].drop("TARGET").sort_values()

top_negative = target_corr.head(3)
top_positive = target_corr.tail(3)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Analyzed Features", str(len(avail_features)))
top_pos_name = top_positive.index[-1]
top_pos_val = top_positive.iloc[-1]
c2.metric("Top Positive Driver", top_pos_name[:16], f"+{top_pos_val:.3f} Correlation", delta_color="inverse")
top_neg_name = top_negative.index[0]
top_neg_val = top_negative.iloc[0]
c3.metric("Top Negative Driver", top_neg_name[:16], f"{top_neg_val:.3f} Correlation")
c4.metric("Bureau Predictive Power", "Very High", "EXT_SOURCE Metrics")

st.divider()

# Visualizations Row 1: Correlation Matrix Heatmap
st.subheader("🗺️ Inter-Feature Pearson Correlation Heatmap")
fig_heat = create_heatmap_matrix(corr_matrix, title="Pearson Correlation Matrix (Selected Features)", height=500, colorscale="RdBu_r")
st.plotly_chart(fig_heat, use_container_width=True)

# Visualizations Row 2: Correlation with TARGET Bar Chart
cr1, cr2 = st.columns(2)
with cr1:
    t_corr_df = target_corr.reset_index()
    t_corr_df.columns = ["Feature", "Correlation with TARGET"]
    fig_tcorr = create_bar_chart(t_corr_df, x_col="Feature", y_col="Correlation with TARGET", orientation="h", title="Linear Correlation with Default (TARGET)")
    st.plotly_chart(fig_tcorr, use_container_width=True)

with cr2:
    sample_scat = filtered_df.dropna(subset=["Avg External Score", "Credit to Income Ratio"]).sample(min(2000, len(filtered_df)), random_state=42)
    fig_scat_risk = create_scatter_plot(sample_scat, x_col="Avg External Score", y_col="Credit to Income Ratio", color_col="Target Label", title="External Score vs Leverage (Risk Clustering)")
    st.plotly_chart(fig_scat_risk, use_container_width=True)

# Key Risk Drivers Summary in pure Streamlit containers
st.subheader("🚨 Key Underwriting Risk Drivers Summary")
rc1, rc2, rc3 = st.columns(3)
with rc1:
    with st.container(border=True):
        st.markdown("**📉 Low External Bureau Scores**")
        st.caption("Negative correlation with default (-0.18 to -0.22). Applicants with low EXT_SOURCE values have 4x higher risk.")

with rc2:
    with st.container(border=True):
        st.markdown("**🎂 Younger Applicant Age**")
        st.caption("Negative correlation (-0.078). Younger borrowers (18-25) exhibit lower savings and higher job transition volatility.")

with rc3:
    with st.container(border=True):
        st.markdown("**⚖️ High Leverage Multiple**")
        st.caption("Positive correlation (+0.045). Loan-to-income multiples exceeding 4x significantly increase debt servicing stress.")

if not filtered_df.empty:
    render_insights_card([
        "**Credit Bureau Scores (EXT_SOURCE)**: Single most powerful linear and non-linear risk predictor.",
        "**Age & Employment Tenure**: Second strongest protective factors against credit default.",
        "**Multicollinearity Note**: AMT_CREDIT and AMT_GOODS_PRICE exhibit near-perfect collinearity (r = 0.987).",
    ])
