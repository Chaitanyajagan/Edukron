import streamlit as st
import textwrap
from typing import List, Optional, Dict, Any

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --font-heading: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --bg-main: #0B0F19;
    --bg-card: rgba(19, 28, 46, 0.75);
    --bg-card-hover: rgba(25, 38, 62, 0.85);
    --border-card: rgba(59, 130, 246, 0.16);
    --border-card-hover: rgba(59, 130, 246, 0.4);
    --accent-blue: #3B82F6;
    --accent-cyan: #06B6D4;
    --accent-emerald: #10B981;
    --accent-amber: #F59E0B;
    --accent-rose: #EF4444;
    --accent-purple: #8B5CF6;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
}

html, body, [class*="css"] {
    font-family: var(--font-body);
    color: var(--text-primary);
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading) !important;
    letter-spacing: -0.02em;
}

/* Header & Top Bar Fix */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 3.2rem !important;
}

/* Base App Layout Padding */
.block-container {
    padding-top: 4.8rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1400px;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c111d 0%, #070a12 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

section[data-testid="stSidebar"] hr {
    margin: 1.2rem 0 !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
}

/* Native Streamlit Metric Cards Styling */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(19, 28, 46, 0.8) 0%, rgba(13, 19, 33, 0.95) 100%) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.06) !important;
    backdrop-filter: blur(12px) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative;
    overflow: hidden;
}

[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3B82F6, #6366F1);
    opacity: 0.8;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    border-color: var(--border-card-hover) !important;
    box-shadow: 0 12px 30px -4px rgba(0, 0, 0, 0.6), 0 0 15px rgba(59, 130, 246, 0.2) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    margin-bottom: 4px !important;
}

[data-testid="stMetricValue"] {
    font-family: var(--font-heading) !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em !important;
}

[data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
}

/* Border Containers (Cards) */
[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: linear-gradient(145deg, rgba(19, 28, 46, 0.65) 0%, rgba(10, 15, 26, 0.8) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 14px !important;
    padding: 1.25rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
    backdrop-filter: blur(10px) !important;
    transition: border-color 0.2s ease, transform 0.2s ease;
}

[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
    border-color: rgba(59, 130, 246, 0.25) !important;
}

/* Custom Header Badge */
.header-badge-container {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(90deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.15));
    border: 1px solid rgba(59, 130, 246, 0.35);
    border-radius: 9999px;
    padding: 4px 14px;
    margin-top: 0.25rem;
    margin-bottom: 12px;
}

.header-badge-text {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #60A5FA;
}

.header-title-gradient {
    font-family: var(--font-heading);
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1.2;
    background: linear-gradient(135deg, #FFFFFF 20%, #CBD5E1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
    letter-spacing: -0.03em;
}

.header-subtitle {
    font-size: 1.02rem;
    color: #94A3B8;
    line-height: 1.5;
    margin-bottom: 1.25rem;
    max-width: 900px;
}

/* Formula Callout Card */
.formula-card-wrapper {
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.9) 0%, rgba(10, 15, 26, 0.95) 100%);
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-left: 4px solid #3B82F6;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0 16px 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.formula-card-title {
    font-family: var(--font-heading);
    font-size: 0.95rem;
    font-weight: 700;
    color: #93C5FD;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}

.formula-card-math {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 10px 14px;
    font-family: var(--font-mono);
    font-size: 0.88rem;
    color: #38BDF8;
    margin-bottom: 8px;
    overflow-x: auto;
}

.formula-card-desc {
    font-size: 0.85rem;
    color: #94A3B8;
    line-height: 1.4;
}

/* Executive Insights Card */
.insights-card-wrapper {
    background: linear-gradient(145deg, rgba(16, 26, 44, 0.8) 0%, rgba(10, 18, 30, 0.95) 100%);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-left: 4px solid #10B981;
    border-radius: 14px;
    padding: 20px 24px;
    margin: 16px 0;
    box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.35);
}

.insights-card-header {
    font-family: var(--font-heading);
    font-size: 1.1rem;
    font-weight: 700;
    color: #6EE7B7;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    letter-spacing: -0.01em;
}

.insights-list {
    margin: 0;
    padding-left: 0;
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.insights-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 0.92rem;
    color: #E2E8F0;
    line-height: 1.5;
}

.insights-bullet {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 6px;
    height: 6px;
    background-color: #10B981;
    border-radius: 50%;
    margin-top: 8px;
    flex-shrink: 0;
    box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.45) !important;
    transform: translateY(-1px) !important;
}

/* Download Buttons */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
    color: #F1F5F9 !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    border-color: #60A5FA !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
    transform: translateY(-1px) !important;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(15, 23, 42, 0.6);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.stTabs [data-baseweb="tab"] {
    height: 38px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 8px;
    color: #94A3B8;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 0 16px;
    border: none;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(11, 15, 25, 0.5);
}

::-webkit-scrollbar-thumb {
    background: rgba(59, 130, 246, 0.3);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(59, 130, 246, 0.6);
}
</style>
"""


def apply_page_config(page_title: str = "Home Credit Default Risk", page_icon: str = "🏦"):
    """Configures Streamlit page layout, metadata, and injects global modern CSS design system."""
    st.set_page_config(
        page_title=f"{page_title} | Home Credit Risk Intelligence",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Inject ultra-modern global styling without leading indentation
    st.markdown(textwrap.dedent(GLOBAL_CSS).strip(), unsafe_allow_html=True)


def render_header(title: str, subtitle: str, badge: Optional[str] = None):
    """Renders modern executive page header with category pill badge, gradient title, and subtitle."""
    badge_html = ""
    if badge:
        badge_html = f'<div class="header-badge-container"><span style="font-size: 0.8rem;">🛡️</span><span class="header-badge-text">Enterprise Risk Analytics • {badge}</span></div>'
    
    header_html = f"""<div style="margin-bottom: 1.5rem;">{badge_html}<h1 class="header-title-gradient">{title}</h1><p class="header-subtitle">{subtitle}</p></div>"""
    st.markdown(header_html, unsafe_allow_html=True)
    st.divider()


def render_formula_card(formula_name: str, formula_math: str, formula_desc: str):
    """Renders mathematical calculation formula callout with styled blueprint design."""
    card_html = f"""<div class="formula-card-wrapper"><div class="formula-card-title"><span>📐</span><span>Metric Formula: {formula_name}</span></div><div class="formula-card-math">{formula_math}</div><div class="formula-card-desc">{formula_desc}</div></div>"""
    st.markdown(card_html, unsafe_allow_html=True)


def render_insights_card(insights: List[str], title: str = "Key Underwriting & Risk Insights"):
    """Renders structured key business insights using custom glassmorphic callout card."""
    items_html = ""
    for insight in insights:
        # Format bold tags nicely if markdown asterisks exist
        formatted = insight
        while "**" in formatted:
            formatted = formatted.replace("**", "<strong style='color: #60A5FA;'>", 1).replace("**", "</strong>", 1)
        items_html += f'<li class="insights-item"><span class="insights-bullet"></span><span>{formatted}</span></li>'

    card_html = f"""<div class="insights-card-wrapper"><div class="insights-card-header"><span>💡</span><span>{title}</span></div><ul class="insights-list">{items_html}</ul></div>"""
    st.markdown(card_html, unsafe_allow_html=True)


def render_metric_card(
    label: str,
    value: str,
    subtext: str = "",
    delta: Optional[str] = None,
    delta_type: str = "neutral",
    accent_color: str = "#3B82F6",
):
    """
    Renders an elevated standalone custom metric card with glowing accent bar,
    subtext badge, and delta indicator.
    """
    delta_colors = {
        "positive": "#10B981",
        "negative": "#EF4444",
        "neutral": "#94A3B8",
        "warning": "#F59E0B"
    }
    d_color = delta_colors.get(delta_type, "#94A3B8")
    
    delta_html = ""
    if delta:
        delta_html = f'<span style="display: inline-flex; align-items: center; background: rgba(255,255,255,0.06); color: {d_color}; font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 9999px;">{delta}</span>'
        
    subtext_html = ""
    if subtext:
        subtext_html = f'<div style="font-size: 0.78rem; color: #94A3B8;">{subtext}</div>'

    card_html = f"""<div style="background: linear-gradient(145deg, rgba(19, 28, 46, 0.8) 0%, rgba(13, 19, 33, 0.95) 100%); border: 1px solid rgba(59, 130, 246, 0.18); border-radius: 14px; padding: 16px 20px; position: relative; overflow: hidden; box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4); min-height: 120px; display: flex; flex-direction: column; justify-content: space-between;"><div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: {accent_color};"></div><div><div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; color: #94A3B8; margin-bottom: 4px;">{label}</div><div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.65rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.02em;">{value}</div></div><div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; margin-top: 6px;">{subtext_html}{delta_html}</div></div>"""
    st.markdown(card_html, unsafe_allow_html=True)
