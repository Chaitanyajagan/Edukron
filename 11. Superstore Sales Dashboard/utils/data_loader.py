import os
import glob
import pandas as pd
import numpy as np
import streamlit as st
from typing import Tuple, Optional

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(WORKSPACE_ROOT, "data")


def get_available_datasets() -> dict[str, str]:
    """Scans data/ and workspace root to identify present dataset files."""
    datasets = {f: os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".csv")} if os.path.exists(DATA_DIR) else {}
    for f in os.listdir(WORKSPACE_ROOT):
        if f.endswith(".csv") and f not in datasets:
            datasets[f] = os.path.join(WORKSPACE_ROOT, f)
    return datasets


@st.cache_data(show_spinner="Loading Home Credit Default Risk Dataset...")
def load_home_credit_data(max_rows: Optional[int] = None) -> pd.DataFrame:
    """Loads and engineers all features for Home Credit Default Risk dataset."""
    datasets = get_available_datasets()
    csv_path = datasets.get("application_train.csv") or next((v for k, v in datasets.items() if any(w in k.lower() for w in ["train", "credit", "application"])), None)
    if not csv_path or not os.path.exists(csv_path):
        csv_files = glob.glob(os.path.join(WORKSPACE_ROOT, "**", "*.csv"), recursive=True)
        if not csv_files:
            raise FileNotFoundError("No application_train.csv found in workspace.")
        csv_path = csv_files[0]

    df = pd.read_csv(csv_path, nrows=max_rows)
    df.columns = [c.strip() for c in df.columns]

    if "TARGET" in df.columns:
        df["TARGET"] = pd.to_numeric(df["TARGET"], errors="coerce").fillna(0).astype(int)
        df["Target Label"] = df["TARGET"].map({0: "Repaid (Non-Default)", 1: "Default (Payment Difficulty)"})

    if "DAYS_BIRTH" in df.columns:
        df["Age"] = (df["DAYS_BIRTH"].abs() / 365.0).round(1)
        bins, labels = [18, 25, 30, 35, 40, 45, 50, 55, 60, 100], ["18–25", "26–30", "31–35", "36–40", "41–45", "46–50", "51–55", "56–60", "61+"]
        df["Age Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)

    if "DAYS_EMPLOYED" in df.columns:
        df["Employment Years"] = (df["DAYS_EMPLOYED"].replace(365243, np.nan).abs() / 365.0).round(1)

    inc = df["AMT_INCOME_TOTAL"].replace(0, np.nan) if "AMT_INCOME_TOTAL" in df.columns else None
    if inc is not None and "AMT_CREDIT" in df.columns:
        df["Credit to Income Ratio"] = (df["AMT_CREDIT"] / inc).round(2)
        df["Credit Leverage Group"] = pd.cut(df["Credit to Income Ratio"], bins=[0, 2, 4, 6, 1000], labels=["Low (< 2x)", "Moderate (2–4x)", "High (4–6x)", "Very High (> 6x)"], right=False)
    if inc is not None and "AMT_ANNUITY" in df.columns:
        df["Annuity to Income Ratio"] = (df["AMT_ANNUITY"] / inc).round(4)
        df["Annuity Burden %"] = (df["Annuity to Income Ratio"] * 100).round(2)
    if "AMT_CREDIT" in df.columns and "AMT_GOODS_PRICE" in df.columns:
        df["Credit to Goods Ratio"] = (df["AMT_CREDIT"] / df["AMT_GOODS_PRICE"].replace(0, np.nan)).round(2)

    if "AMT_INCOME_TOTAL" in df.columns:
        df["Income Group"] = pd.cut(df["AMT_INCOME_TOTAL"], bins=[0, 50000, 100000, 150000, 200000, 300000, 500000, np.inf], labels=["Below 50K", "50K–100K", "100K–150K", "150K–200K", "200K–300K", "300K–500K", "Above 500K"], right=False)
    if "AMT_CREDIT" in df.columns:
        df["Credit Group"] = pd.cut(df["AMT_CREDIT"], bins=[0, 100000, 300000, 500000, 700000, 1000000, np.inf], labels=["Below 100K", "100K–300K", "300K–500K", "500K–700K", "700K–1M", "Above 1M"], right=False)

    ext = [c for c in ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"] if c in df.columns]
    if ext:
        df["Avg External Score"] = df[ext].mean(axis=1).round(3)
        df["External Score Rating"] = pd.cut(df["Avg External Score"], bins=[0, 0.25, 0.50, 0.75, 1.01], labels=["Poor (< 0.25)", "Fair (0.25–0.50)", "Good (0.50–0.75)", "Excellent (0.75–1.0)"], right=False)

    cat_cols = ["NAME_CONTRACT_TYPE", "CODE_GENDER", "FLAG_OWN_CAR", "FLAG_OWN_REALTY", "NAME_INCOME_TYPE", "NAME_EDUCATION_TYPE", "NAME_FAMILY_STATUS", "NAME_HOUSING_TYPE", "OCCUPATION_TYPE", "ORGANIZATION_TYPE"]
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].fillna("Unknown").astype(str)
    return df


@st.cache_data(show_spinner="Loading Superstore Dataset...")
def load_superstore_data() -> pd.DataFrame:
    """Loads and engineers features for Superstore Sales dataset."""
    datasets = get_available_datasets()
    csv_path = datasets.get("sample_superstore.csv") or next((v for k, v in datasets.items() if "superstore" in k.lower()), None)
    if not csv_path:
        raise FileNotFoundError("sample_superstore.csv not found.")
    try:
        df = pd.read_csv(csv_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="windows-1252")

    df.columns = [c.strip() for c in df.columns]
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed", errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="mixed", errors="coerce")
    df = df.dropna(subset=["Order Date", "Ship Date"]).copy()
    for col, default, dt in [("Sales", 0.0, float), ("Quantity", 1, int), ("Discount", 0.0, float), ("Profit", 0.0, float)]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(default).astype(dt)

    df["Order Year"], df["Order Month Num"] = df["Order Date"].dt.year, df["Order Date"].dt.month
    df["Order Month"], df["Order Quarter"] = df["Order Date"].dt.strftime("%B"), "Q" + df["Order Date"].dt.quarter.astype(str)
    df["Order Year-Month"] = df["Order Date"].dt.strftime("%Y-%m")
    df["Order Year-Quarter"] = df["Order Year"].astype(str) + "-" + df["Order Quarter"]
    df["Order Day of Week"] = df["Order Date"].dt.day_name()
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days.apply(lambda d: max(d, 0))
    df["Profit Margin %"] = np.where(df["Sales"] > 0, (df["Profit"] / df["Sales"]) * 100, 0.0).round(2)
    df["Is Loss"] = df["Profit"] < 0
    df["Loss Amount"] = df["Profit"].apply(lambda p: abs(p) if p < 0 else 0.0)
    df["Discount %"] = (df["Discount"] * 100).round(1)
    return df


def load_dataset() -> Tuple[pd.DataFrame, str]:
    """Auto-detects dataset present and loads it."""
    datasets = get_available_datasets()
    if any("train" in k.lower() or "credit" in k.lower() or "application" in k.lower() for k in datasets):
        return load_home_credit_data(), "home_credit"
    if any("superstore" in k.lower() for k in datasets):
        return load_superstore_data(), "superstore"
    raise FileNotFoundError("No CSV dataset found in workspace or data/ directory.")
