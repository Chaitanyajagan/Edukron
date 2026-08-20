import pandas as pd
import numpy as np
from typing import Dict, Any


def format_currency(value: float) -> str:
    """Formats numeric value into clean currency notation ($1.23M, $45.6K, $789)."""
    if pd.isna(value):
        return "$0.00"
    sign, abs_val = ("-" if value < 0 else ""), abs(value)
    if abs_val >= 1_000_000:
        return f"{sign}${abs_val / 1_000_000:.2f}M"
    elif abs_val >= 1_000:
        return f"{sign}${abs_val / 1_000:.1f}K"
    return f"{sign}${abs_val:,.2f}"


def format_percent(value: float) -> str:
    """Formats decimal or percentage into formatted percentage string."""
    return "0.0%" if pd.isna(value) else f"{value:.2f}%"


def format_number(value: int | float) -> str:
    """Formats integer count with comma separators."""
    if pd.isna(value):
        return "0"
    if isinstance(value, float):
        return f"{int(value):,}" if value.is_integer() else f"{value:,.1f}"
    return f"{value:,}"


def calculate_home_credit_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes all standard Home Credit Default Risk KPIs."""
    if df.empty:
        return {
            "total_applications": 0, "default_customers": 0, "non_default_customers": 0,
            "default_rate": 0.0, "total_credit": 0.0, "avg_credit": 0.0,
            "avg_income": 0.0, "avg_annuity": 0.0, "avg_age": 0.0,
            "avg_ext_score": 0.0, "avg_credit_income_ratio": 0.0,
        }
    t = len(df)
    d = int((df["TARGET"] == 1).sum()) if "TARGET" in df.columns else 0
    nd = int((df["TARGET"] == 0).sum()) if "TARGET" in df.columns else 0
    return {
        "total_applications": t,
        "default_customers": d,
        "non_default_customers": nd,
        "default_rate": round(d / t * 100, 2) if t else 0.0,
        "total_credit": round(float(df["AMT_CREDIT"].sum()), 2) if "AMT_CREDIT" in df.columns else 0.0,
        "avg_credit": round(float(df["AMT_CREDIT"].mean()), 2) if "AMT_CREDIT" in df.columns else 0.0,
        "avg_income": round(float(df["AMT_INCOME_TOTAL"].mean()), 2) if "AMT_INCOME_TOTAL" in df.columns else 0.0,
        "avg_annuity": round(float(df["AMT_ANNUITY"].mean()), 2) if "AMT_ANNUITY" in df.columns else 0.0,
        "avg_age": round(float(df["Age"].mean()), 1) if "Age" in df.columns else 0.0,
        "avg_ext_score": round(float(df["Avg External Score"].mean()), 3) if "Avg External Score" in df.columns else 0.0,
        "avg_credit_income_ratio": round(float(df["Credit to Income Ratio"].mean()), 2) if "Credit to Income Ratio" in df.columns else 0.0,
    }


def calculate_core_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes standard Superstore Sales KPIs."""
    if df.empty:
        return {
            "total_sales": 0.0, "total_profit": 0.0, "profit_margin": 0.0, "total_orders": 0,
            "total_customers": 0, "total_quantity": 0, "aov": 0.0, "max_order_sales": 0.0,
            "min_order_sales": 0.0, "avg_discount": 0.0, "total_loss": 0.0, "loss_orders_count": 0,
            "loss_rate": 0.0, "avg_shipping_days": 0.0,
        }
    ts = float(df["Sales"].sum()) if "Sales" in df.columns else 0.0
    tp = float(df["Profit"].sum()) if "Profit" in df.columns else 0.0
    orders = int(df["Order ID"].nunique()) if "Order ID" in df.columns else 0
    osales = df.groupby("Order ID")["Sales"].sum() if "Order ID" in df.columns and "Sales" in df.columns else pd.Series()
    loss = df[df["Profit"] < 0] if "Profit" in df.columns else pd.DataFrame()
    l_count = int(loss["Order ID"].nunique()) if not loss.empty and "Order ID" in loss.columns else 0
    return {
        "total_sales": ts, "total_profit": tp, "profit_margin": round(tp / ts * 100, 2) if ts else 0.0,
        "total_orders": orders, "total_customers": int(df["Customer ID"].nunique()) if "Customer ID" in df.columns else 0,
        "total_quantity": int(df["Quantity"].sum()) if "Quantity" in df.columns else 0,
        "aov": round(ts / orders, 2) if orders else 0.0,
        "max_order_sales": round(float(osales.max()), 2) if not osales.empty else 0.0,
        "min_order_sales": round(float(osales.min()), 2) if not osales.empty else 0.0,
        "avg_discount": round(float(df["Discount"].mean() * 100), 2) if "Discount" in df.columns else 0.0,
        "total_loss": round(float(abs(loss["Profit"].sum())), 2) if not loss.empty else 0.0,
        "loss_orders_count": l_count, "loss_rate": round(l_count / orders * 100, 2) if orders else 0.0,
        "avg_shipping_days": round(float(df["Shipping Days"].mean()), 1) if "Shipping Days" in df.columns else 0.0,
    }


def calculate_growth_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes growth metrics for time series."""
    if df.empty or "Order Date" not in df.columns:
        return {"mom_sales_growth": 0.0, "mom_profit_growth": 0.0, "yoy_sales_growth": 0.0, "yoy_profit_growth": 0.0}
    m = df.set_index("Order Date").resample("ME").agg({"Sales": "sum", "Profit": "sum"})
    if len(m) < 2:
        return {"mom_sales_growth": 0.0, "mom_profit_growth": 0.0, "yoy_sales_growth": 0.0, "yoy_profit_growth": 0.0}
    y = df.set_index("Order Date").resample("YE").agg({"Sales": "sum", "Profit": "sum"})
    p_s, p_p = m["Sales"].iloc[-2], m["Profit"].iloc[-2]
    yoy_s = ((y["Sales"].iloc[-1] - y["Sales"].iloc[-2]) / y["Sales"].iloc[-2] * 100) if len(y) >= 2 and y["Sales"].iloc[-2] > 0 else 0.0
    yoy_p = ((y["Profit"].iloc[-1] - y["Profit"].iloc[-2]) / abs(y["Profit"].iloc[-2]) * 100) if len(y) >= 2 and y["Profit"].iloc[-2] != 0 else 0.0
    return {
        "mom_sales_growth": round(((m["Sales"].iloc[-1] - p_s) / p_s * 100) if p_s > 0 else 0.0, 2),
        "mom_profit_growth": round(((m["Profit"].iloc[-1] - p_p) / abs(p_p) * 100) if p_p != 0 else 0.0, 2),
        "yoy_sales_growth": round(yoy_s, 2), "yoy_profit_growth": round(yoy_p, 2),
        "latest_month_name": m.index[-1].strftime("%B %Y"), "prev_month_name": m.index[-2].strftime("%B %Y"),
    }
