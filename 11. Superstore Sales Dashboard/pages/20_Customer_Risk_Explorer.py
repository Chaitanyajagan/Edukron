import streamlit as st
import pandas as pd
from utils.page_helpers import apply_page_config, render_header, render_insights_card
from utils.data_loader import load_home_credit_data
from utils.filters import render_sidebar_filters
from utils.kpis import format_currency, format_percent, format_number

apply_page_config(page_title="Customer Risk Explorer", page_icon="👤")
df = load_home_credit_data()
filtered_df, _ = render_sidebar_filters(df)

render_header(
    title="Page 20: Applicant Risk Profile Explorer & Export Engine",
    subtitle="Search individual applicant dossiers by SK_ID_CURR, inspect risk indicators, and export custom borrower segments.",
    badge="Underwriting Dossier",
)

# Search Box
search_id = st.text_input("🔍 Search Applicant by SK_ID_CURR (e.g. 100002):", "")

if search_id:
    matched = df[df["SK_ID_CURR"].astype(str) == search_id.strip()]
    if not matched.empty:
        client = matched.iloc[0]
        st.subheader("📋 Applicant Risk Dossier Card")
        is_default = client["TARGET"] == 1
        badge_text = "🚨 High Default Risk (TARGET=1)" if is_default else "✅ Low Default Risk (TARGET=0)"
        
        with st.container(border=True):
            st.markdown(f"### Applicant ID: #{client['SK_ID_CURR']} — **{badge_text}**")
            st.divider()
            
            p1, p2, p3, p4 = st.columns(4)
            p1.metric("Age", f"{client.get('Age', 'N/A')} Yrs")
            p2.metric("Gender", f"{client.get('CODE_GENDER', 'N/A')}")
            p3.metric("Annual Income", f"${client.get('AMT_INCOME_TOTAL', 0):,.2f}")
            p4.metric("Credit Requested", f"${client.get('AMT_CREDIT', 0):,.2f}")

            p5, p6, p7, p8 = st.columns(4)
            p5.metric("Scheduled Annuity", f"${client.get('AMT_ANNUITY', 0):,.2f}")
            p6.metric("Education", f"{client.get('NAME_EDUCATION_TYPE', 'N/A')}")
            p7.metric("Occupation", f"{client.get('OCCUPATION_TYPE', 'N/A')}")
            p8.metric("Family Status", f"{client.get('NAME_FAMILY_STATUS', 'N/A')}")

            p9, p10, p11, p12 = st.columns(4)
            p9.metric("Children Count", f"{client.get('CNT_CHILDREN', 0)}")
            p10.metric("Housing Type", f"{client.get('NAME_HOUSING_TYPE', 'N/A')}")
            p11.metric("Owns Car / Realty", f"{client.get('FLAG_OWN_CAR', 'N')} / {client.get('FLAG_OWN_REALTY', 'N')}")
            p12.metric("Employment Tenure", f"{client.get('Employment Years', 'N/A')} Yrs")

            st.divider()
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Credit/Income Ratio", f"{client.get('Credit to Income Ratio', 'N/A')}x")
            r2.metric("Annuity Burden %", f"{client.get('Annuity Burden %', 'N/A')}%")
            r3.metric("Avg External Score", f"{client.get('Avg External Score', 'N/A')}")
            r4.metric("Credit/Goods Ratio", f"{client.get('Credit to Goods Ratio', 'N/A')}x")
    else:
        st.warning(f"Applicant ID #{search_id} not found.")

st.subheader("📊 Filtered Applicant Cohort Explorer")
default_cols = [
    "SK_ID_CURR", "TARGET", "Target Label", "CODE_GENDER", "Age", "NAME_EDUCATION_TYPE",
    "NAME_INCOME_TYPE", "OCCUPATION_TYPE", "AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY",
    "Credit to Income Ratio", "Annuity Burden %", "Avg External Score"
]
avail_cols = [c for c in default_cols if c in filtered_df.columns]
sel_cols = st.multiselect("Select columns to view:", options=filtered_df.columns.tolist(), default=avail_cols)
st.dataframe(filtered_df[sel_cols].head(1000).copy(), use_container_width=True, hide_index=True)

st.divider()
st.subheader("📥 Underwriting Export Center")
d1, d2, d3 = st.columns(3)
with d1:
    st.download_button("📄 Download Filtered Cohort (CSV)", filtered_df.head(20000).to_csv(index=False).encode("utf-8"), "home_credit_filtered_applicants.csv", "text/csv", use_container_width=True)
with d2:
    st.download_button("🚨 Download Default Cohort (CSV)", filtered_df[filtered_df["TARGET"] == 1].head(15000).to_csv(index=False).encode("utf-8"), "home_credit_defaults_only.csv", "text/csv", use_container_width=True)
with d3:
    high_risk = filtered_df[(filtered_df["Credit to Income Ratio"] > 4.0) | (filtered_df["Avg External Score"] < 0.3)].head(15000)
    st.download_button("⚠️ Download High-Risk Cohort (CSV)", high_risk.to_csv(index=False).encode("utf-8"), "home_credit_high_risk_watchlist.csv", "text/csv", use_container_width=True)

render_insights_card([
    f"**Population in View**: **{format_number(len(filtered_df))}** total records matching active sidebar filters.",
    "**Underwriting Search**: Type any SK_ID_CURR in the search box above to render the instant 360-degree applicant profile card.",
    "**Export Engine**: Download cohorts directly for risk committee review or scoring model ingestion.",
])
