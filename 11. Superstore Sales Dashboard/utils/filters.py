import streamlit as st
import pandas as pd
from typing import Tuple, Dict, Any


def render_sidebar_filters(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Renders dynamic sidebar filters based on the active dataset schema.
    Supports both Home Credit Default Risk and Superstore Sales datasets.
    """
    st.sidebar.markdown("### 🎛️ Filter Controls")
    filtered_df = df.copy()
    filters_applied = {}

    if "TARGET" in df.columns or "SK_ID_CURR" in df.columns:
        if "TARGET" in df.columns:
            target_opt = st.sidebar.radio("🎯 Loan Status (TARGET)", ["All Applicants", "Non-Default (0)", "Default / Difficulties (1)"])
            if target_opt != "All Applicants":
                val = 0 if "0" in target_opt else 1
                filtered_df = filtered_df[filtered_df["TARGET"] == val]
                filters_applied["target"] = val
        st.sidebar.markdown("---")
        if "CODE_GENDER" in df.columns:
            genders = [g for g in sorted(df["CODE_GENDER"].dropna().unique().tolist()) if g != "XNA"]
            if sel := st.sidebar.multiselect("👤 Gender", options=genders):
                filtered_df = filtered_df[filtered_df["CODE_GENDER"].isin(sel)]
                filters_applied["gender"] = sel
        if "Age" in df.columns:
            mi, ma = int(df["Age"].min()), int(df["Age"].max())
            age_rng = st.sidebar.slider("🎂 Age Range (Years)", min_value=mi, max_value=ma, value=(mi, ma))
            filtered_df = filtered_df[(filtered_df["Age"] >= age_rng[0]) & (filtered_df["Age"] <= age_rng[1])]
            filters_applied["age_range"] = age_rng
        for col, label, key in [
            ("NAME_CONTRACT_TYPE", "📄 Contract Type", "contract_type"),
            ("NAME_INCOME_TYPE", "💼 Income Type", "income_type"),
            ("NAME_EDUCATION_TYPE", "🎓 Education Level", "education"),
            ("NAME_HOUSING_TYPE", "🏠 Housing Type", "housing"),
        ]:
            if col in df.columns and (sel := st.sidebar.multiselect(label, options=sorted(df[col].dropna().unique().tolist()))):
                filtered_df = filtered_df[filtered_df[col].isin(sel)]
                filters_applied[key] = sel
    else:
        if "Order Date" in df.columns:
            d_min, d_max = df["Order Date"].min().date(), df["Order Date"].max().date()
            dr = st.sidebar.date_input("📅 Date Range", value=(d_min, d_max), min_value=d_min, max_value=d_max)
            if isinstance(dr, (tuple, list)) and len(dr) == 2:
                filtered_df = filtered_df[(filtered_df["Order Date"].dt.date >= dr[0]) & (filtered_df["Order Date"].dt.date <= dr[1])]
        st.sidebar.markdown("---")
        for col, label in [("Region", "🌍 Region"), ("State", "📍 State"), ("Category", "📦 Category"), ("Sub-Category", "🏷️ Sub-Category"), ("Segment", "👥 Segment")]:
            if col in df.columns and (sel := st.sidebar.multiselect(label, options=sorted(filtered_df[col].dropna().unique().tolist()))):
                filtered_df = filtered_df[filtered_df[col].isin(sel)]

    st.sidebar.markdown("---")
    total_recs, filtered_recs = len(df), len(filtered_df)
    pct = (filtered_recs / total_recs * 100) if total_recs > 0 else 0
    st.sidebar.caption(f"Showing **{filtered_recs:,}** of **{total_recs:,}** records ({pct:.1f}%)")
    return filtered_df, filters_applied
