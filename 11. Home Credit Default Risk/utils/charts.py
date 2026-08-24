import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Optional, List, Union

COLOR_SEQUENCE = [
    "#3B82F6",  # Electric Blue
    "#06B6D4",  # Cyan
    "#10B981",  # Emerald
    "#F59E0B",  # Amber
    "#8B5CF6",  # Violet
    "#EC4899",  # Pink
    "#6366F1",  # Indigo
    "#14B8A6",  # Teal
]

TARGET_COLORS = {
    "Repaid (TARGET = 0)": "#3B82F6",
    "Default (TARGET = 1)": "#EF4444",
    "Repaid": "#3B82F6",
    "Default": "#EF4444",
    "0": "#3B82F6",
    "1": "#EF4444"
}


def apply_chart_layout(
    fig: go.Figure,
    title: str = "",
    height: int = 420,
    show_legend: bool = True
) -> go.Figure:
    """Configures modern, dark-slate transparent layout with clean typography and zero collisions."""
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=35, r=25, t=55, b=50),
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
            color="#F1F5F9",
            size=12
        ),
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(
                family="Plus Jakarta Sans, sans-serif",
                size=14,
                color="#F8FAFC"
            ),
            x=0.0,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.16,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)",
            title=dict(text=""),
            font=dict(size=11, color="#94A3B8")
        ),
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor="#334155",
            font_size=12,
            font_family="Inter, sans-serif",
            font_color="#F8FAFC"
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(148, 163, 184, 0.08)",
        zeroline=False,
        tickfont=dict(size=11, color="#94A3B8"),
        title_font=dict(size=12, color="#CBD5E1"),
        automargin=True,
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(148, 163, 184, 0.08)",
        zeroline=False,
        tickfont=dict(size=11, color="#94A3B8"),
        title_font=dict(size=12, color="#CBD5E1"),
        automargin=True,
    )
    return fig


def create_donut_chart(
    df: pd.DataFrame,
    names_col: str,
    values_col: str,
    title: str = "",
    height: int = 420,
    hole: float = 0.58
) -> go.Figure:
    """Creates a sleek donut chart with high-contrast labels and smooth colors."""
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
        insidetextorientation="radial",
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent:.1%}<extra></extra>",
        textfont=dict(size=12, color="#FFFFFF", family="Inter, sans-serif"),
        marker=dict(line=dict(color="#0B0F19", width=2))
    )
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=55, b=45),
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family="Plus Jakarta Sans, sans-serif", size=14, color="#F8FAFC"),
            x=0.0,
            y=0.98,
            xanchor="left",
            yanchor="top"
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)",
            title=dict(text=""),
            font=dict(size=11, color="#94A3B8")
        )
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
    """Creates a responsive modern bar chart with sleek styling."""
    has_color = color_col and color_col in df.columns
    color_map = TARGET_COLORS if has_color and any(k in df[color_col].astype(str).values for k in TARGET_COLORS) else None
    text_format = ".1f" if text_auto else None

    fig = px.bar(
        df,
        x=x_col if orientation == "v" else y_col,
        y=y_col if orientation == "v" else x_col,
        color=color_col if has_color else None,
        orientation=orientation,
        text_auto=text_format,
        color_discrete_map=color_map if color_map else None,
        color_discrete_sequence=COLOR_SEQUENCE if not color_map else None,
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        textfont=dict(size=11, color="#CBD5E1", family="Inter, sans-serif"),
        marker=dict(line=dict(width=0))
    )
    
    show_leg = has_color and color_col != x_col
    return apply_chart_layout(fig, title=title, height=height, show_legend=show_leg)


def create_line_trend(
    df: pd.DataFrame,
    x_col: str,
    y_cols: Union[List[str], str],
    title: str = "",
    height: int = 420,
    show_markers: bool = True
) -> go.Figure:
    """Creates a smooth spline line trend chart."""
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
                line=dict(width=3, color=c, shape="spline"),
                marker=dict(size=7, color=c, line=dict(width=1.5, color="#0B0F19"))
            )
        )
    show_leg = len(cols) > 1
    return apply_chart_layout(fig, title=title, height=height, show_legend=show_leg)


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    hover_name: Optional[str] = None,
    title: str = "",
    height: int = 440
) -> go.Figure:
    """Creates an interactive scatter plot with clean modern markers."""
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
        opacity=0.78,
    )
    fig.update_traces(
        marker=dict(size=6, line=dict(width=0.5, color="rgba(255,255,255,0.2)"))
    )
    fig.update_layout(legend_title_text="")
    return apply_chart_layout(fig, title=title, height=height, show_legend=bool(has_color))


def create_histogram(
    df: pd.DataFrame,
    col: str,
    nbins: int = 35,
    title: str = "",
    height: int = 400,
    color_by: Optional[str] = None
) -> go.Figure:
    """Creates a distribution histogram with clean translucent bars."""
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
        opacity=0.7 if has_color else 0.85,
    )
    fig.update_traces(
        marker=dict(line=dict(width=1, color="rgba(0,0,0,0.25)"))
    )
    fig.update_layout(legend_title_text="")
    return apply_chart_layout(fig, title=title, height=height, show_legend=bool(has_color))


def create_box_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "",
    height: int = 420
) -> go.Figure:
    """Creates comparative box plots with vibrant color styling."""
    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        color_discrete_sequence=COLOR_SEQUENCE
    )
    fig.update_traces(
        marker=dict(size=4),
        line=dict(width=1.5)
    )
    return apply_chart_layout(fig, title=title, height=height, show_legend=False)


def create_heatmap_matrix(
    pivot_df: pd.DataFrame,
    title: str = "",
    height: int = 500,
    colorscale: str = "Blues"
) -> go.Figure:
    """Creates an aesthetic correlation matrix heatmap with legible values."""
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
            textfont=dict(size=10, family="JetBrains Mono, monospace"),
            hoverongaps=False,
            colorbar=dict(
                title="",
                tickfont=dict(size=10, color="#94A3B8"),
                len=0.8
            )
        )
    )
    return apply_chart_layout(fig, title=title, height=height, show_legend=False)
