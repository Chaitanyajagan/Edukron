import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

COLOR_SEQUENCE = ["#2563eb", "#059669", "#7c3aed", "#d97706", "#0891b2", "#db2777", "#4f46e5", "#0d9488"]


def apply_chart_layout(fig: go.Figure, title: str = "", height: int = 420) -> go.Figure:
    """Configures clean, spacious layout using native Plotly parameters."""
    fig.update_layout(
        template="plotly_white", height=height, margin=dict(l=30, r=30, t=70, b=40),
        title=dict(text=title, font=dict(size=15), x=0.02, y=0.96, pad=dict(b=15)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#e2e8f0")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#e2e8f0")
    return fig


def create_donut_chart(df: pd.DataFrame, names_col: str, values_col: str, title: str = "", height: int = 430, hole: float = 0.52) -> go.Figure:
    """Creates a clean donut chart with bottom legend."""
    fig = px.pie(df, names=names_col, values=values_col, hole=hole, color_discrete_sequence=COLOR_SEQUENCE)
    fig.update_traces(textposition="inside", textinfo="percent", hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>")
    fig.update_layout(
        template="plotly_white", height=height, margin=dict(l=30, r=30, t=70, b=60),
        title=dict(text=title, font=dict(size=15), x=0.02, y=0.96, pad=dict(b=15)),
        legend=dict(orientation="h", yanchor="top", y=-0.08, xanchor="center", x=0.5, bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def create_line_trend(df: pd.DataFrame, x_col: str, y_cols: list[str] | str, title: str = "", height: int = 420, show_markers: bool = True) -> go.Figure:
    """Creates a line trend chart."""
    cols = [y_cols] if isinstance(y_cols, str) else y_cols
    fig = go.Figure()
    for idx, col in enumerate(cols):
        c = COLOR_SEQUENCE[idx % len(COLOR_SEQUENCE)]
        fig.add_trace(go.Scatter(x=df[x_col], y=df[col], name=col, mode="lines+markers" if show_markers else "lines", line=dict(width=3, color=c), marker=dict(size=6, color=c)))
    return apply_chart_layout(fig, title=title, height=height)


def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str = "", color_col: str | None = None, orientation: str = "v", height: int = 420, is_currency: bool = False) -> go.Figure:
    """Creates a bar chart with horizontal or vertical orientation."""
    has_color = color_col and color_col in df.columns
    fig = px.bar(
        df, x=x_col if orientation == "v" else y_col, y=y_col if orientation == "v" else x_col,
        color=color_col if has_color else None, orientation=orientation,
        color_discrete_sequence=COLOR_SEQUENCE if has_color else [COLOR_SEQUENCE[0]],
    )
    return apply_chart_layout(fig, title=title, height=height)


def create_scatter_plot(df: pd.DataFrame, x_col: str, y_col: str, size_col: str | None = None, color_col: str | None = None, hover_name: str | None = None, title: str = "", height: int = 440) -> go.Figure:
    """Creates an interactive scatter plot."""
    valid_df = df.copy()
    if size_col and size_col in valid_df.columns:
        valid_df[size_col] = pd.to_numeric(valid_df[size_col], errors="coerce").fillna(1).abs() + 0.1
    fig = px.scatter(
        valid_df, x=x_col, y=y_col,
        size=size_col if size_col in valid_df.columns else None,
        color=color_col if color_col in valid_df.columns else None,
        hover_name=hover_name if hover_name in valid_df.columns else None,
        color_discrete_sequence=COLOR_SEQUENCE, opacity=0.8,
    )
    return apply_chart_layout(fig, title=title, height=height)


def create_histogram(df: pd.DataFrame, col: str, nbins: int = 35, title: str = "", height: int = 400, color_by: str | None = None) -> go.Figure:
    """Creates a distribution histogram."""
    has_c = color_by and color_by in df.columns
    fig = px.histogram(
        df, x=col, color=color_by if has_c else None, nbins=nbins,
        barmode="overlay" if has_c else None,
        color_discrete_sequence=COLOR_SEQUENCE if has_c else [COLOR_SEQUENCE[0]],
        opacity=0.7 if has_c else 0.8,
    )
    return apply_chart_layout(fig, title=title, height=height)


def create_heatmap_matrix(pivot_df: pd.DataFrame, title: str = "", height: int = 480, colorscale: str = "Blues") -> go.Figure:
    """Creates a correlation matrix heatmap."""
    fig = go.Figure(data=go.Heatmap(z=pivot_df.values, x=pivot_df.columns.tolist(), y=pivot_df.index.tolist(), colorscale=colorscale, hoverongaps=False))
    return apply_chart_layout(fig, title=title, height=height)
