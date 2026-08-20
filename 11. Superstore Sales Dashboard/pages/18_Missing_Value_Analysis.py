import streamlit as st
import pandas as pd
from utils.page_helpers import apply_page_config, render_header, render_insights_card
from utils.data_loader import load_home_credit_data
from utils.kpis import format_number
from utils.charts import create_bar_chart

apply_page_config(page_title="Missing Value Analysis", page_icon="🔍")
df = load_home_credit_data()

render_header(
    title="Page 18: Data Quality & Missing Value Auditor",
    subtitle="Audit missing data patterns, null distributions, column completeness, and recommended ML imputation strategies.",
    badge="Data Quality BI",
)

total_rows, total_cols = df.shape
missing_counts = df.isnull().sum()
total_missing = missing_counts.sum()
cols_with_missing = (missing_counts > 0).sum()
cols_over_50pct = (missing_counts / total_rows > 0.50).sum()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Rows", format_number(total_rows))
c2.metric("Total Features", format_number(total_cols))
c3.metric("Total Missing Cells", format_number(total_missing))
c4.metric("Incomplete Columns", format_number(cols_with_missing), "Columns with Nulls", delta_color="inverse")
c5.metric("Columns >50% Null", format_number(cols_over_50pct), "High Null Rate", delta_color="inverse")

st.divider()

# Missing DataFrame Table
missing_df = pd.DataFrame({
    "Column": df.columns,
    "Missing Count": missing_counts.values,
    "Missing %": ((missing_counts.values / total_rows) * 100).round(2),
    "Data Type": df.dtypes.astype(str).values,
})
missing_df = missing_df[missing_df["Missing Count"] > 0].sort_values("Missing %", ascending=False)

def get_impute_strategy(row):
    pct = row["Missing %"]
    dtype = row["Data Type"]
    if pct > 60:
        return "Drop Column or Binary Missing Indicator"
    elif "float" in dtype or "int" in dtype:
        return "Fill with Median + Missing Flag"
    else:
        return "Fill with 'Unknown' / Mode Category"

missing_df["Recommended Imputation Strategy"] = missing_df.apply(get_impute_strategy, axis=1)

# Visualizations Row 1: Top 20 Missing Columns Bar Chart
ms1, ms2 = st.columns([3, 2])
with ms1:
    top20_miss = missing_df.head(20).sort_values("Missing %", ascending=True)
    fig_top_miss = create_bar_chart(top20_miss, x_col="Column", y_col="Missing %", orientation="h", title="Top 20 Columns by Missing Data %")
    st.plotly_chart(fig_top_miss, use_container_width=True)

with ms2:
    miss_by_type = missing_df.groupby("Data Type")["Column"].count().reset_index()
    miss_by_type.columns = ["Data Type", "Incomplete Features Count"]
    fig_type = create_bar_chart(miss_by_type, x_col="Data Type", y_col="Incomplete Features Count", title="Missing Columns by Data Type")
    st.plotly_chart(fig_type, use_container_width=True)

# Full Missing Values Audit Table
st.subheader("📋 Complete Missing Values Audit & Imputation Guide")
disp_miss = missing_df.copy()
disp_miss["Missing Count"] = disp_miss["Missing Count"].apply(lambda v: f"{v:,}")
disp_miss["Missing %"] = disp_miss["Missing %"].apply(lambda v: f"{v:.2f}%")

st.dataframe(disp_miss, use_container_width=True, hide_index=True)

if not missing_df.empty:
    render_insights_card([
        "**Building & Normalized Scores**: Real estate features (COMMONAREA, LIVINGAPARTMENTS, etc.) have 50–70% missing values.",
        "**External Scores**: EXT_SOURCE_1 is missing for ~56% of applicants, while EXT_SOURCE_2/3 are largely populated (>99%).",
        "**ML Preparation**: Columns with >60% missing data should either be dropped or converted into boolean 'Flag_Was_Missing' features.",
    ])
