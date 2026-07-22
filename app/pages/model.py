import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# path setup
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)

from header import show_header
from footer import show_footer
from data_loader import load_data
from auth.guard import require_login
from calculation.model_cal import get_model_stats


# colours
PAGE_BG  = "#0d1117"
CARD_BG  = "#161b27"
TEAL     = "#00d4c8"
BLUE     = "#4f8ef7"
PURPLE   = "#a78bfa"
AMBER    = "#f59e0b"
RED      = "#E24B4A"
GREEN    = "#1D9E75"

MODEL_COLORS = [BLUE, TEAL, PURPLE]
METRICS      = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]


@st.cache_resource(show_spinner=False)
def get_cached_stats():
    return get_model_stats(load_data())


# dark page styles
def apply_model_styles():
    st.markdown(f"""
<style>
    [data-testid="stSidebar"]        {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    [data-testid="stToolbar"]        {{ display: none !important; }}
    #MainMenu                         {{ display: none !important; }}
    footer                            {{ display: none !important; }}

    html, body, .stApp {{ background: {PAGE_BG} !important; }}

    .block-container {{
        max-width:     100% !important;
        padding-left:  2rem !important;
        padding-right: 2rem !important;
        padding-top:   0 !important;
        background:    {PAGE_BG} !important;
    }}

    .m-section {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: rgba(255,255,255,0.3);
        margin: 0 0 12px 0;
    }}

    .m-divider {{
        height: 1px;
        background: rgba(255,255,255,0.06);
        margin: 20px 0;
    }}

    /* metric strip */
    .m-strip {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 12px;
    }}

    .m-strip-card {{
        background: {CARD_BG};
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.07);
        padding: 16px 18px;
    }}

    .m-strip-label {{
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: rgba(255,255,255,0.32);
        margin: 0 0 6px 0;
    }}

    .m-strip-value {{
        font-size: 26px;
        font-weight: 800;
        line-height: 1;
        margin: 0 0 3px 0;
    }}

    .m-strip-sub {{
        font-size: 11px;
        color: rgba(255,255,255,0.28);
        margin: 0 0 10px 0;
    }}

    .m-strip-bar {{
        background: rgba(255,255,255,0.07);
        border-radius: 3px;
        height: 3px;
        overflow: hidden;
    }}

    .m-strip-fill {{
        height: 100%;
        border-radius: 3px;
    }}

    /* model cards */
    .m-model-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
    }}

    .m-model-card {{
        background: {CARD_BG};
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.07);
        padding: 20px 20px;
        border-top: 3px solid transparent;
    }}

    .m-model-name {{
        font-size: 13px;
        font-weight: 700;
        color: rgba(255,255,255,0.85);
        margin: 0 0 14px 0;
    }}

    .m-model-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }}

    .m-model-metric {{
        font-size: 12px;
        color: rgba(255,255,255,0.42);
    }}

    .m-model-val {{
        font-size: 13px;
        font-weight: 700;
        color: rgba(255,255,255,0.85);
    }}

    .m-model-bar-bg {{
        background: rgba(255,255,255,0.07);
        border-radius: 3px;
        height: 4px;
        margin: 3px 0 10px 0;
        overflow: hidden;
    }}

    .m-model-bar-fill {{
        height: 100%;
        border-radius: 3px;
    }}

    .m-best-badge {{
        display: inline-block;
        background: rgba(0,212,200,0.12);
        color: {TEAL};
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-left: 8px;
    }}

    /* params table */
    .m-params {{
        background: {CARD_BG};
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.07);
        padding: 18px 20px;
    }}

    .m-params-row {{
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }}

    .m-params-row:last-child {{ border-bottom: none; }}

    .m-params-model {{
        font-size: 12px;
        font-weight: 700;
        color: rgba(255,255,255,0.65);
        width: 160px;
        flex-shrink: 0;
    }}

    .m-params-val {{
        font-size: 12px;
        color: rgba(255,255,255,0.38);
        flex: 1;
    }}

    .m-params-thr {{
        font-size: 12px;
        font-weight: 700;
        color: {TEAL};
        width: 50px;
        text-align: right;
        flex-shrink: 0;
    }}
</style>
""", unsafe_allow_html=True)


# shared dark chart layout
def dark_fig(fig, show_legend=True):
    fig.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font_color="rgba(255,255,255,0.7)",
        title_font_color="rgba(255,255,255,0.38)",
        title_font_size=11,
        showlegend=show_legend,
        legend=dict(bgcolor="rgba(0,0,0,0)",
                    font=dict(color="rgba(255,255,255,0.5)", size=11)),
        margin=dict(l=8, r=8, t=32, b=8),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)",
                   linecolor="rgba(255,255,255,0.07)",
                   tickfont=dict(color="rgba(255,255,255,0.4)", size=10),
                   title_font=dict(color="rgba(255,255,255,0.3)")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)",
                   linecolor="rgba(255,255,255,0.07)",
                   tickfont=dict(color="rgba(255,255,255,0.4)", size=10),
                   title_font=dict(color="rgba(255,255,255,0.3)")),
    )
    fig.update_coloraxes(showscale=False)
    return fig


def section(title: str):
    st.markdown(f"<p class='m-section'>{title}</p>", unsafe_allow_html=True)


def divider():
    st.markdown("<div class='m-divider'></div>", unsafe_allow_html=True)


# top summary strip: best model's key metrics
def render_summary_strip(results_df: pd.DataFrame, best_model: str):
    section("Best Model Summary")
    best = results_df[results_df["Model"] == best_model].iloc[0]
    cards = [
        ("Best Model",  best_model,              "highest ROC-AUC",   TEAL,   100),
        ("ROC-AUC",     f"{best['ROC-AUC']}%",   "discriminability",  BLUE,   best["ROC-AUC"]),
        ("F1 Score",    f"{best['F1 Score']}%",   "harmonic mean",     PURPLE, best["F1 Score"]),
        ("Recall",      f"{best['Recall']}%",     "churn detection",   AMBER,  best["Recall"]),
        ("Precision",   f"{best['Precision']}%",  "prediction quality",GREEN,  best["Precision"]),
    ]
    html = '<div class="m-strip">'
    for label, value, sub, color, pct in cards:
        html += f"""
        <div class="m-strip-card" style="border-top:3px solid {color};">
            <p class="m-strip-label">{label}</p>
            <p class="m-strip-value" style="color:{color};">{value}</p>
            <p class="m-strip-sub">{sub}</p>
            <div class="m-strip-bar">
                <div class="m-strip-fill" style="width:{pct:.1f}%;background:{color};"></div>
            </div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# three model cards with per-metric bar rows
def render_model_cards(results_df: pd.DataFrame, best_model: str):
    section("Model Comparison")
    color_map = {
        results_df.iloc[0]["Model"]: BLUE,
        results_df.iloc[1]["Model"]: TEAL,
        results_df.iloc[2]["Model"]: PURPLE,
    }

    cards_html = ""
    for _, row in results_df.iterrows():
        color   = color_map[row["Model"]]
        is_best = row["Model"] == best_model
        badge   = '<span class="m-best-badge">Best</span>' if is_best else ""

        metric_rows = ""
        for m in METRICS:
            val = row[m]
            metric_rows += (
                f'<div class="m-model-row">'
                f'<span class="m-model-metric">{m}</span>'
                f'<span class="m-model-val">{val}%</span>'
                f'</div>'
                f'<div class="m-model-bar-bg">'
                f'<div class="m-model-bar-fill" style="width:{val}%;background:{color};"></div>'
                f'</div>'
            )

        cards_html += (
            f'<div class="m-model-card" style="border-top-color:{color};">'
            f'<p class="m-model-name">{row["Model"]}{badge}</p>'
            f'{metric_rows}'
            f'</div>'
        )

    st.markdown(
        f'<div class="m-model-grid">{cards_html}</div>',
        unsafe_allow_html=True,
    )

# grouped bar chart
def render_metrics_chart(results_df: pd.DataFrame):
    section("Metrics Bar Chart")
    melted = results_df.melt(
        id_vars="Model", value_vars=METRICS,
        var_name="Metric", value_name="Score",
    )
    fig = px.bar(
        melted, x="Metric", y="Score", color="Model", barmode="group",
        color_discrete_sequence=MODEL_COLORS, text="Score",
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%", textposition="outside",
        textfont_color="rgba(255,255,255,0.6)",
    )
    fig.update_layout(
        title_text="All models — all metrics",
        yaxis=dict(range=[0, 115]),
        bargap=0.2, bargroupgap=0.05,
    )
    st.plotly_chart(dark_fig(fig), use_container_width=True)


# roc curves
def render_roc_curves(stats: dict):
    section("ROC Curves")
    results_df = stats["results_df"]
    fig = go.Figure()

    for i, (model_name, roc) in enumerate(stats["roc_data"].items()):
        auc = results_df.loc[results_df["Model"] == model_name, "ROC-AUC"].values[0]
        fig.add_trace(go.Scatter(
            x=roc["fpr"], y=roc["tpr"],
            name=f"{model_name} (AUC={auc:.1f}%)",
            line=dict(color=MODEL_COLORS[i], width=2.5),
            fill="tozeroy" if i == 0 else None,
            fillcolor=f"rgba{(*bytes.fromhex(MODEL_COLORS[i].lstrip('#')), 0.08)}",
        ))

    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        name="Random classifier",
        line=dict(color="rgba(255,255,255,0.2)", dash="dash", width=1.5),
    ))
    fig.update_layout(
        title_text="ROC curve comparison",
        xaxis_title="False positive rate",
        yaxis_title="True positive rate",
    )
    st.plotly_chart(dark_fig(fig), use_container_width=True)


# confusion matrices
def render_confusion_matrices(stats: dict):
    section("Confusion Matrices")
    cols = st.columns(3)

    for col, (model_name, cm) in zip(cols, stats["conf_matrices"].items()):
        with col:
            fig = px.imshow(
                cm, text_auto=True,
                color_continuous_scale=[[0, CARD_BG], [1, TEAL]],
                title=model_name,
                labels=dict(x="Predicted", y="Actual"),
                x=["Not Churn", "Churn"],
                y=["Not Churn", "Churn"],
            )
            fig.update_traces(textfont_color="white")
            fig.update_layout(paper_bgcolor=CARD_BG)
            st.plotly_chart(dark_fig(fig, show_legend=False), use_container_width=True)


# methodology + hyperparameters
def render_methodology(stats: dict):
    section("Methodology & Hyperparameters")
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown(
            f'<div style="background:{CARD_BG};border-radius:14px;'
            f'border:1px solid rgba(255,255,255,0.07);padding:20px 22px;">'
            f'<p style="font-size:11px;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:0.8px;color:rgba(255,255,255,0.35);margin:0 0 14px 0;">Pipeline</p>'
            f'<p style="font-size:13px;color:rgba(255,255,255,0.6);line-height:1.8;margin:0;">'
            f'One-hot encoding on categoricals, standard scaling on numerics.<br><br>'
            f'SMOTE applied <b style="color:{TEAL};">inside each CV fold</b> only — '
            f'validation scores are never inflated.<br><br>'
            f'GridSearchCV (3-fold stratified, scoring=ROC-AUC) tuned all models.<br><br>'
            f'Decision threshold optimised to maximise F1 on cross-validated '
            f'training predictions — <b style="color:{TEAL};">never on the test set.</b>'
            f'</p></div>',
            unsafe_allow_html=True,
        )

    with col2:
        header_row = (
            '<div class="m-params-row" style="border-bottom:1px solid rgba(255,255,255,0.08);'
            'padding-bottom:6px;margin-bottom:2px;">'
            '<span class="m-params-model" style="color:rgba(255,255,255,0.28);font-size:10px;">Model</span>'
            '<span class="m-params-val" style="color:rgba(255,255,255,0.28);font-size:10px;">Parameters</span>'
            '<span class="m-params-thr" style="color:rgba(255,255,255,0.28);font-size:10px;">Threshold</span>'
            '</div>'
        )

        rows_html = ""
        for m, p in stats["best_params"].items():
            params = ", ".join(
                f"{k.replace('model__', '')}={v}" for k, v in p.items()
            )
            thr = round(stats["thresholds"][m], 3)
            rows_html += (
                f'<div class="m-params-row">'
                f'<span class="m-params-model">{m}</span>'
                f'<span class="m-params-val">{params}</span>'
                f'<span class="m-params-thr">{thr}</span>'
                f'</div>'
            )

        st.markdown(
            f'<div class="m-params">'
            f'<p style="font-size:11px;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:0.8px;color:rgba(255,255,255,0.35);margin:0 0 4px 0;">'
            f'Best Hyperparameters</p>'
            f'{header_row}'
            f'{rows_html}'
            f'</div>',
            unsafe_allow_html=True,
        )


# guard and render
require_login()
apply_model_styles()
show_header(back=True)

with st.spinner("Loading models..."):
    stats = get_cached_stats()

results_df = stats["results_df"]
best_model = results_df.loc[results_df["ROC-AUC"].idxmax(), "Model"]

render_summary_strip(results_df, best_model)
divider()
render_model_cards(results_df, best_model)
divider()
render_metrics_chart(results_df)
divider()
render_roc_curves(stats)
divider()
render_confusion_matrices(stats)
divider()
render_methodology(stats)
st.markdown("<br>", unsafe_allow_html=True)

show_footer()