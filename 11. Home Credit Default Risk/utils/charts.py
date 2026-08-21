import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Optional, List, Union

COLOR_SEQUENCE = ["#2563eb", "#dc2626", "#059669", "#d97706", "#7c3aed", "#0891b2", "#db2777", "#4f46e5"]
TARGET_COLORS = {"Repaid (TARGET = 0)": "#2563eb", "Default (TARGET = 1)": "#dc2626", "Repaid": "#2563eb", "Default": "#dc2626"}


def apply_chart_layout(fig: go.Figure, title: str = "", height: int = 420) -> go.Figure:
    """Configures clean, modern layout using native Plotly parameters."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=30, r=30, t=65, b=40),
        title=dict(text=f"<b>{title}</b>" if title else "", font=dict(size=14, color="#1e293b"), x=0.01, y=0.96),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#ffffff", font_size=12),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f1f5f9", title_font=dict(size=12, color="#64748b"))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f1f5f9", title_font=dict(size=12, color="#64748b"))
    return fig


def create_donut_chart(
    df: pd.DataFrame,
    names_col: str,
    values_col: str,
    title: str = "",
    height: int = 420,
    hole: float = 0.52
) -> go.Figure:
    """Creates an aesthetic donut chart with percentage callouts."""
    color_map = TARGET_COLORS if any(k in df[names_col].astype(str).values for k in TARGET_COLORS) else None
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        hole=hole,
        color=names_col if color_map else None,
        color_discrete_map=color_map if color_map else None,
        color_discrete_sequence=COLOR_SEQUENCE if not color_map else None
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent:.1%}<extra></extra>"
    )
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=30, r=30, t=65, b=50),
        title=dict(text=f"<b>{title}</b>" if title else "", font=dict(size=14, color="#1e293b"), x=0.01, y=0.96),
        legend=dict(orientation="h", yanchor="top", y=-0.08, xanchor="center", x=0.5, bgcolor="rgba(0,0,0,0)")
    )
    return fig


def create_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "",
    color_col: Optional[str] = None,
    orientation: str = "v",
    height: int = 420,
    text_auto: bool = True
) -> go.Figure:
    """Creates a responsive bar chart with vertical or horizontal orientation."""
    has_color = color_col and color_col in df.columns
    color_map = TARGET_COLORS if has_color and any(k in df[color_col].astype(str).values for k in TARGET_COLORS) else None
    
    fig = px.bar(
        df,
        x=x_col if orientation == "v" else y_col,
        y=y_col if orientation == "v" else x_col,
        color=color_col if has_color else None,
        orientation=orientation,
        text_auto=text_auto,
        color_discrete_map=color_map if color_map else None,
        color_discrete_sequence=COLOR_SEQUENCE if not color_map else None,
    )
    fig.update_traces(textposition="outside")
    return apply_chart_layout(fig, title=title, height=height)


def create_line_trend(
    df: pd.DataFrame,
    x_col: str,
    y_cols: Union[List[str], str],
    title: str = "",
    height: int = 420,
    show_markers: bool = True
) -> go.Figure:
    """Creates a smooth line trend chart."""
    cols = [y_cols] if isinstance(y_cols, str) else y_cols
    fig = go.Figure()
    for idx, col in enumerate(cols):
        c = COLOR_SEQUENCE[idx % len(COLOR_SEQUENCE)]
        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[col],
                name=col,
                mode="lines+markers" if show_markers else "lines",
                line=dict(width=3, color=c),
                marker=dict(size=6, color=c)
            )
        )
    return apply_chart_layout(fig, title=title, height=height)


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    hover_name: Optional[str] = None,
    title: str = "",
    height: int = 440
) -> go.Figure:
    """Creates an interactive scatter plot."""
    valid_df = df.copy()
    has_color = color_col and color_col in valid_df.columns
    color_map = TARGET_COLORS if has_color and any(k in valid_df[color_col].astype(str).values for k in TARGET_COLORS) else None

    fig = px.scatter(
        valid_df,
        x=x_col,
        y=y_col,
        color=color_col if has_color else None,
        hover_name=hover_name if hover_name in valid_df.columns else None,
        color_discrete_map=color_map if color_map else None,
        color_discrete_sequence=COLOR_SEQUENCE if not color_map else None,
        opacity=0.75,
    )
    return apply_chart_layout(fig, title=title, height=height)


def create_histogram(
    df: pd.DataFrame,
    col: str,
    nbins: int = 35,
    title: str = "",
    height: int = 400,
    color_by: Optional[str] = None
) -> go.Figure:
    """Creates a distribution histogram."""
    has_color = color_by and color_by in df.columns
    color_map = TARGET_COLORS if has_color and any(k in df[color_by].astype(str).values for k in TARGET_COLORS) else None

    fig = px.histogram(
        df,
        x=col,
        color=color_by if has_color else None,
        nbins=nbins,
        barmode="overlay" if has_color else None,
        color_discrete_map=color_map if color_map else None,
        color_discrete_sequence=COLOR_SEQUENCE if not color_map else None,
        opacity=0.65 if has_color else 0.85,
    )
    return apply_chart_layout(fig, title=title, height=height)


def create_box_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "",
    height: int = 420
) -> go.Figure:
    """Creates comparative box plots across categories (e.g. TARGET vs Credit/Annuity)."""
    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        color_discrete_sequence=COLOR_SEQUENCE
    )
    return apply_chart_layout(fig, title=title, height=height)


def create_heatmap_matrix(
    pivot_df: pd.DataFrame,
    title: str = "",
    height: int = 500,
    colorscale: str = "Blues"
) -> go.Figure:
    """Creates a correlation matrix heatmap with values displayed."""
    z_vals = pivot_df.values
    x_labels = pivot_df.columns.tolist()
    y_labels = pivot_df.index.tolist()

    fig = go.Figure(
        data=go.Heatmap(
            z=z_vals,
            x=x_labels,
            y=y_labels,
            colorscale=colorscale,
            text=np.round(z_vals, 2),
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        )
    )
    return apply_chart_layout(fig, title=title, height=height)
