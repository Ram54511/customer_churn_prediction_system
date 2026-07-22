import sys
import os
import pandas as pd
import plotly.express as px
import streamlit as st

# path setup
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)

from styles.shap import apply_shap_styles, PAGE_BG, CARD_BG, TEAL, CHURN_COLOR, RETAINED_COLOR
from header import show_header
from footer import show_footer
from data_loader import load_data
from auth.guard import require_login
from calculation.shap_cal import get_shap_stats


# colours not in styles file
BLUE   = "#4f8ef7"
PURPLE = "#a78bfa"
AMBER  = "#f59e0b"


@st.cache_resource(show_spinner=False)
def get_cached_shap():
    return get_shap_stats(load_data())


def dark_fig(fig, show_legend=True):
    fig.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font_color="rgba(255,255,255,0.7)",
        title_font_color="rgba(255,255,255,0.38)",
        title_font_size=11,
        showlegend=show_legend,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.5)", size=11),
        ),
        margin=dict(l=8, r=8, t=32, b=8),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(255,255,255,0.07)",
            tickfont=dict(color="rgba(255,255,255,0.4)", size=10),
            title_font=dict(color="rgba(255,255,255,0.3)"),
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(255,255,255,0.07)",
            tickfont=dict(color="rgba(255,255,255,0.4)", size=10),
            title_font=dict(color="rgba(255,255,255,0.3)"),
        ),
    )
    fig.update_coloraxes(showscale=False)
    return fig


def section(title: str):
    st.markdown(f"<p class='sh-section'>{title}</p>", unsafe_allow_html=True)


def divider():
    st.markdown("<div class='sh-divider'></div>", unsafe_allow_html=True)


# what is SHAP intro card
def render_intro():
    section("About SHAP")
    st.markdown(
        '<div class="sh-intro">'
        '<p><b>SHAP (SHapley Additive exPlanations)</b> is a game-theoretic approach '
        'to explain the output of any machine learning model. It tells us '
        '<b>how much each feature contributes</b> to a prediction — both globally '
        '(across all customers) and locally (for a single customer). The model being '
        'explained here is the <b>same tuned XGBoost</b> evaluated on the Model Results page.</p>'
        '</div>',
        unsafe_allow_html=True,
    )


# top 5 driver cards
def render_top_drivers(top10: pd.DataFrame):
    section("Top 5 Churn Drivers")
    max_imp      = top10["Importance"].max()
    driver_colors = [TEAL, BLUE, PURPLE, AMBER, CHURN_COLOR]

    cards_html = '<div class="sh-driver-grid">'
    for i, (_, row) in enumerate(top10.head(5).iterrows()):
        color = driver_colors[i]
        pct   = row["Importance"] / max_imp * 100
        cards_html += (
            f'<div class="sh-driver-card" style="border-top:3px solid {color};">'
            f'<p class="sh-driver-rank">#{i + 1}</p>'
            f'<p class="sh-driver-name">{row["Feature"]}</p>'
            f'<p class="sh-driver-val" style="color:{color};">{row["Importance"]:.4f}</p>'
            f'<div class="sh-driver-bar">'
            f'<div class="sh-driver-fill" style="width:{pct:.1f}%;background:{color};"></div>'
            f'</div>'
            f'</div>'
        )
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


# global feature importance bar chart
def render_global_importance(top10: pd.DataFrame):
    section("Global Feature Importance")
    fig = px.bar(
        top10, x="Importance", y="Feature", orientation="h",
        color="Importance",
        color_continuous_scale=[[0, RETAINED_COLOR], [0.5, TEAL], [1, CHURN_COLOR]],
        text=top10["Importance"].round(4),
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        title_text="Top 10 features by mean |SHAP| value",
    )
    fig.update_traces(
        textposition="outside",
        textfont_color="rgba(255,255,255,0.55)",
    )
    st.plotly_chart(dark_fig(fig, show_legend=False), use_container_width=True)


# beeswarm scatter
def render_beeswarm(stats: dict, top10: pd.DataFrame):
    section("SHAP Value Distribution")
    col1, col2 = st.columns([3, 1], gap="medium")

    with col1:
        shap_vals = stats["shap_values"].values
        X_test    = stats["X_test"]
        features  = stats["feature_names"]

        rows = []
        for feat in top10["Feature"]:
            idx       = features.index(feat)
            feat_vals = X_test.iloc[:, idx].values
            shap_col  = shap_vals[:, idx]
            norm_vals = (feat_vals - feat_vals.min()) / (feat_vals.max() - feat_vals.min() + 1e-9)
            for sv, nv in zip(shap_col, norm_vals):
                rows.append({"Feature": feat, "SHAP Value": sv, "Feature Value": nv})

        fig = px.scatter(
            pd.DataFrame(rows), x="SHAP Value", y="Feature",
            color="Feature Value",
            color_continuous_scale=[[0, RETAINED_COLOR], [0.5, TEAL], [1, CHURN_COLOR]],
            opacity=0.5,
        )
        fig.update_layout(
            yaxis=dict(autorange="reversed"),
            title_text="Each dot = one customer · colour = feature value (green=low, red=high)",
        )
        fig.update_coloraxes(
            showscale=True,
            colorbar=dict(
                tickfont=dict(color="rgba(255,255,255,0.4)", size=10),
                title=dict(
                    text="Feature value",
                    font=dict(color="rgba(255,255,255,0.35)", size=10),
                ),
            ),
        )
        st.plotly_chart(dark_fig(fig, show_legend=False), use_container_width=True)

    with col2:
        st.markdown(
            f'<div style="background:{CARD_BG};border-radius:14px;'
            f'border:1px solid rgba(255,255,255,0.07);padding:18px 16px;margin-top:32px;">'
            f'<p style="font-size:11px;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:.8px;color:rgba(255,255,255,0.3);margin:0 0 12px 0;">How to read</p>'
            f'<p style="font-size:12px;color:rgba(255,255,255,0.5);line-height:1.8;margin:0;">'
            f'<b style="color:{CHURN_COLOR};">Right of 0</b> → pushes toward churn<br><br>'
            f'<b style="color:{RETAINED_COLOR};">Left of 0</b> → pushes away from churn<br><br>'
            f'<b style="color:{TEAL};">Red dots</b> → high feature value<br><br>'
            f'<b style="color:{TEAL};">Green dots</b> → low feature value<br><br>'
            f'Spread of dots shows how consistently a feature drives predictions.'
            f'</p></div>',
            unsafe_allow_html=True,
        )


# local explanation slider
def render_local_explanation(stats: dict):
    section("Local Explanation — Single Customer")
    shap_vals = stats["shap_values"].values
    X_test    = stats["X_test"]
    features  = stats["feature_names"]

    col1, col2 = st.columns([3, 1], gap="medium")

    with col2:
        customer_idx = st.slider(
            "Customer index", 0, len(X_test) - 1, 0,
            help="Each index is a customer from the hold-out test set.",
        )

    with col1:
        local_df = pd.DataFrame({
            "Feature":    features,
            "SHAP Value": shap_vals[customer_idx],
        }).sort_values("SHAP Value", key=abs, ascending=False).head(10)

        local_df["Direction"] = local_df["SHAP Value"].apply(
            lambda x: "Increases churn risk" if x > 0 else "Decreases churn risk"
        )

        fig = px.bar(
            local_df, x="SHAP Value", y="Feature",
            orientation="h", color="Direction",
            color_discrete_map={
                "Increases churn risk": CHURN_COLOR,
                "Decreases churn risk": RETAINED_COLOR,
            },
        )
        fig.update_layout(
            yaxis=dict(autorange="reversed"),
            title_text=f"Customer #{customer_idx} — top 10 feature impacts",
        )
        st.plotly_chart(dark_fig(fig), use_container_width=True)


# business insight cards
def render_business_insights():
    section("Business Insights")

    high_risk = [
        "Month-to-month contract",
        "Fiber optic internet service",
        "Electronic check payment",
        "Short tenure (0–12 months)",
        "High monthly charges (>$70)",
    ]
    low_risk = [
        "Two-year contract",
        "Long tenure (48+ months)",
        "Has partner or dependents",
        "Automatic bank transfer payment",
        "Lower monthly charges",
    ]

    def items_html(items, color):
        return "".join(
            f'<div class="sh-insight-item">'
            f'<div class="sh-insight-dot" style="background:{color};"></div>'
            f'<p class="sh-insight-text">{item}</p>'
            f'</div>'
            for item in items
        )

    html = (
        '<div class="sh-insight-grid">'
        f'<div class="sh-insight-card" style="border-left:3px solid {CHURN_COLOR};">'
        f'<p class="sh-insight-title" style="color:{CHURN_COLOR};">High churn risk indicators</p>'
        f'{items_html(high_risk, CHURN_COLOR)}'
        f'</div>'
        f'<div class="sh-insight-card" style="border-left:3px solid {RETAINED_COLOR};">'
        f'<p class="sh-insight-title" style="color:{RETAINED_COLOR};">Low churn risk indicators</p>'
        f'{items_html(low_risk, RETAINED_COLOR)}'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


# guard and render
require_login()
apply_shap_styles()
show_header(back=True)

with st.spinner("Computing SHAP values..."):
    stats = get_cached_shap()

top10 = stats["top10"]

render_intro()
divider()
render_top_drivers(top10)
divider()
render_global_importance(top10)
divider()
render_beeswarm(stats, top10)
divider()
render_local_explanation(stats)
divider()
render_business_insights()
st.markdown("<br>", unsafe_allow_html=True)

show_footer()