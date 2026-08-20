import streamlit as st
from typing import List, Optional


def apply_page_config(page_title: str = "Home Credit Default Risk", page_icon: str = "🏦"):
    """Configures Streamlit page layout using native Streamlit settings."""
    st.set_page_config(
        page_title=f"{page_title} | Risk Analytics",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_header(title: str, subtitle: str, badge: Optional[str] = None):
    """Renders page header using pure Streamlit native components."""
    if badge:
        st.caption(f"📌 {badge}")
    st.title(title)
    st.caption(subtitle)
    st.divider()


def render_insights_card(insights: List[str], title: str = "Key Business Insights"):
    """Renders business insights using native Streamlit container and markdown."""
    with st.container(border=True):
        st.subheader(f"💡 {title}")
        for insight in insights:
            st.markdown(f"• {insight}")
