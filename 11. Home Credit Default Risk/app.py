import streamlit as st
import pandas as pd
from utils.page_helpers import apply_page_config, render_header, render_insights_card, render_metric_card
from utils.data_loader import load_home_credit_data
from utils.kpis import calculate_home_credit_kpis, format_currency, format_percent, format_number
from utils.charts import create_bar_chart, create_donut_chart, create_scatter_plot

apply_page_config(page_title="Home Credit Analytics Hub", page_icon="🏦")

try:
    df = load_home_credit_data()
except Exception as e:
    st.error(f"Error loading Home Credit dataset: {e}")
    st.stop()

# Header with Enterprise Badge
render_header(
    title="Home Credit Default Risk Intelligence Platform",
    subtitle="Enterprise Credit Risk Analytics & Default Prediction Platform • 20 Interactive Analytical Perspectives",
    badge="v2.5 Production Portfolio Suite",
)

kpis = calculate_home_credit_kpis(df)

# Top KPI Metric Row
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    render_metric_card(
        label="Total Applicants",
        value=format_number(kpis["total_applications"]),
        subtext="Analyzed Loan Requests",
        accent_color="#3B82F6"
    )
with c2:
    render_metric_card(
        label="Default Rate",
        value=format_percent(kpis["default_rate"]),
        subtext=f"{format_number(kpis['default_customers'])} Delinquencies",
        delta="Target = 1",
        delta_type="negative",
        accent_color="#EF4444"
    )
with c3:
    render_metric_card(
        label="Total Credit Issued",
        value=format_currency(kpis["total_credit"]),
        subtext="Cumulative Exposure",
        accent_color="#10B981"
    )
with c4:
    render_metric_card(
        label="Avg Client Income",
        value=format_currency(kpis["avg_income"]),
        subtext="Annual Salary Basis",
        accent_color="#F59E0B"
    )
with c5:
    render_metric_card(
        label="Avg External Score",
        value=f"{kpis['avg_ext_score']:.3f}",
        subtext=f"Mean Age: {kpis['avg_age']:.1f} Yrs",
        delta="Bureau Index",
        delta_type="positive",
        accent_color="#8B5CF6"
    )

st.write("")
st.divider()

# Executive Visualizations
st.markdown("### 📊 Executive Portfolio Snapshot")
r1, r2, r3 = st.columns([1.2, 1.2, 1.6])

with r1:
    target_counts = df["Target Label"].value_counts().reset_index()
    target_counts.columns = ["Status", "Count"]
    fig_target = create_donut_chart(target_counts, names_col="Status", values_col="Count", title="Portfolio Default vs Repaid Share")
    st.plotly_chart(fig_target, use_container_width=True)

with r2:
    if "NAME_INCOME_TYPE" in df.columns:
        inc_agg = df.groupby("NAME_INCOME_TYPE")["TARGET"].agg(Default_Rate="mean", Count="count").reset_index()
        inc_agg["Default Rate %"] = (inc_agg["Default_Rate"] * 100).round(2)
        fig_inc = create_bar_chart(
            inc_agg.sort_values("Count", ascending=False).head(5),
            x_col="NAME_INCOME_TYPE",
            y_col="Default Rate %",
            title="Default Rate % by Top Income Types"
        )
        st.plotly_chart(fig_inc, use_container_width=True)

with r3:
    sample_df = df.sample(min(1500, len(df)), random_state=42)
    fig_scat = create_scatter_plot(
        sample_df,
        x_col="AMT_INCOME_TOTAL",
        y_col="AMT_CREDIT",
        color_col="Target Label",
        title="Credit Requested vs Income (Sample View)"
    )
    st.plotly_chart(fig_scat, use_container_width=True)

st.divider()

# 20 Analytical Perspectives Matrix with Category Tabs
st.markdown("### 🗂️ 20 Comprehensive Analytical Perspectives")
st.caption("Select any perspective from the **Sidebar Navigation** or browse the curated categories below:")

categories = {
    "🏢 Core Portfolio & Dossier": [
        ("Executive Portfolio Overview", "📈", "Portfolio overview, default rates, volume, income and credit metrics.", "Overview"),
        ("Default Propensity & Target", "🎯", "In-depth TARGET variable distribution across contract, income, and education.", "Target"),
        ("Loan Contract Structuring", "📄", "Cash Loans vs Revolving Loans risk profiling and credit terms.", "Products"),
        ("Customer Risk Explorer", "👤", "Search applicant by SK_ID_CURR, risk dossier card, and CSV downloads.", "Dossier"),
    ],
    "👥 Borrower Demographics": [
        ("Demographic Risk Profiling", "👥", "Gender, age, marital status, and housing demographic risk profiles.", "Demographics"),
        ("Age Cohorts & Credit Risk", "🎂", "Age cohorts (18–25 to 61+) and their direct correlation with repayment risk.", "Age Risk"),
        ("Gender Underwriting Spread", "👤", "Comparative benchmark between male and female credit applicants.", "Gender"),
        ("Education Risk Stratification", "🎓", "Education levels (Academic Degree to Lower Secondary) and default risk.", "Education"),
        ("Family & Dependent Risk", "👨‍👩‍👧", "Household size, number of dependents, and family status risk factors.", "Family"),
    ],
    "💰 Income, Credit & Debt Burden": [
        ("Income Distribution & Tiers", "💰", "Income distribution (<50K to >500K) and default rates across salary tiers.", "Income"),
        ("Credit Exposure & Sizing", "💳", "Loan sizes requested, credit brackets, and default rates by loan size.", "Credit"),
        ("Annuity Payment Sizing", "💵", "Annual loan payment obligations, annuity distribution, and repayment risk.", "Installments"),
        ("Income vs. Credit Leverage", "⚖️", "Credit-to-Income leverage scatter plots and risk tiers (<2x to >6x).", "Leverage"),
        ("Debt-to-Income Annuity Burden", "📊", "Debt-to-Income burden ratio and repayment stress indicators.", "DTI Ratio"),
    ],
    "💼 Employment, Assets & Geography": [
        ("Employment & Occupational Risk", "💼", "Work tenure, high-risk occupations, and organization categories.", "Employment"),
        ("Housing & Collateral Assets", "🏠", "Car and real estate collateral ownership impact on default rates.", "Collateral"),
        ("Regional Density & Spatial Risk", "🌍", "Regional population densities, city risk ratings, and address mismatches.", "Geography"),
    ],
    "🔬 Bureau Scores & Risk Factors": [
        ("External Bureau Scores", "🌟", "EXT_SOURCE_1/2/3 predictive credit bureau score analysis.", "Bureau Scores"),
        ("Data Quality & Missing Auditor", "🔍", "Data quality auditor, missing data heatmaps, and imputation strategy.", "Data Quality"),
        ("Correlation & Risk Drivers", "🔗", "Feature correlation heatmap against TARGET and key default drivers.", "Collinearity"),
    ]
}

tab_names = list(categories.keys())
tabs = st.tabs(tab_names)

for tab_idx, tab_name in enumerate(tab_names):
    with tabs[tab_idx]:
        pages = categories[tab_name]
        cols = st.columns(len(pages))
        for col_idx, (title, icon, desc, tag) in enumerate(pages):
            with cols[col_idx]:
                card_html = f"""<div style="background: linear-gradient(145deg, rgba(19, 28, 46, 0.7) 0%, rgba(10, 15, 26, 0.85) 100%); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 12px; padding: 16px; height: 100%; min-height: 155px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);"><div><div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;"><span style="font-size: 1.3rem;">{icon}</span><span style="font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 9999px; padding: 2px 8px;">{tag}</span></div><div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.95rem; font-weight: 700; color: #F1F5F9; margin-bottom: 6px;">{title}</div><div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.4;">{desc}</div></div></div>"""
                st.markdown(card_html, unsafe_allow_html=True)

st.divider()

# Executive Insights
render_insights_card([
    f"**Portfolio Default Rate**: Overall baseline default rate is **{format_percent(kpis['default_rate'])}** across **{format_number(kpis['total_applications'])}** total applicants.",
    f"**Capital Deployment**: Cumulative credit issued stands at **{format_currency(kpis['total_credit'])}** with average ticket size of **{format_currency(kpis['avg_credit'])}**.",
    f"**External Credit Bureau**: Average composite external score is **{kpis['avg_ext_score']:.3f}**, serving as the prime statistical predictor of default propensity.",
    "Navigate to individual pages from the sidebar to inspect granular breakdowns and download custom applicant cohorts.",
])
