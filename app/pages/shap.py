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

from config import DATASET_DETAIL
from theme import apply_theme, TEXT_MUTED, PRIMARY, ACCENT, CHURN_COLOR, RETAINED_COLOR
from footer import show_footer
from data_loader import load_data
from calculation.shap_cal import get_shap_stats


# compute SHAP once on the shared tuned XGBoost and reuse
@st.cache_resource(show_spinner=False)
def get_cached_shap():
    return get_shap_stats(load_data())


# short explanation of what SHAP is
def render_intro():
    st.markdown("### What is SHAP?")
    st.markdown(
        f"""<p style='color:{TEXT_MUTED};'>
        <b>SHAP (SHapley Additive exPlanations)</b> is a game-theoretic approach to explain the output
        of any machine learning model. It tells us <b>how much each feature contributes</b> to a prediction —
        both globally (across all customers) and locally (for a single customer).
        </p>""",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)


# horizontal bar chart of mean absolute SHAP values
def render_global_importance(top10: pd.DataFrame):
    st.markdown("### Global Feature Importance")
    st.markdown(
        f"<p style='color:{TEXT_MUTED};'>Average impact of each feature on churn prediction across all customers.</p>",
        unsafe_allow_html=True,
    )

    fig = px.bar(
        top10, x="Importance", y="Feature", orientation="h",
        title="Top 10 Features by Mean SHAP Value",
        color="Importance",
        color_continuous_scale=[[0, RETAINED_COLOR], [0.5, ACCENT], [1, CHURN_COLOR]],
        text=top10["Importance"].round(4),
    )
    fig.update_layout(yaxis=dict(autorange="reversed"),
                      paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


# ranked cards for the five strongest churn drivers
def render_top_drivers(top10: pd.DataFrame):
    st.markdown("### Top 5 Churn Drivers")
    cols = st.columns(5)

    for i, (col, (_, row)) in enumerate(zip(cols, top10.head(5).iterrows())):
        with col:
            st.markdown(
                f"""<div style='background:white; padding:14px; border-radius:8px;
                            border-top:4px solid {PRIMARY}; text-align:center;'>
                    <h3 style='color:{PRIMARY}; margin:0;'>#{i + 1}</h3>
                    <b style='color:#212529;'>{row['Feature']}</b><br>
                    <span style='color:{ACCENT}; font-size:13px;'>{row['Importance']:.4f}</span>
                </div>""",
                unsafe_allow_html=True,
            )
    st.markdown("<br>", unsafe_allow_html=True)


# beeswarm-style scatter of SHAP values for the top 10 features
def render_beeswarm(stats: dict, top10: pd.DataFrame):
    st.markdown("### SHAP Value Distribution (Top 10 Features)")
    st.markdown(
        f"<p style='color:{TEXT_MUTED};'>Each dot is a customer. "
        f"<span style='color:{CHURN_COLOR};'>Red = high feature value</span>, "
        f"<span style='color:{RETAINED_COLOR};'>Blue = low feature value</span>. "
        f"Position on x-axis shows impact on churn prediction.</p>",
        unsafe_allow_html=True,
    )

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
        pd.DataFrame(rows), x="SHAP Value", y="Feature", color="Feature Value",
        color_continuous_scale=[[0, RETAINED_COLOR], [1, CHURN_COLOR]],
        title="SHAP Beeswarm Plot", opacity=0.6,
    )
    fig.update_layout(yaxis=dict(autorange="reversed"),
                      paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)


# per-customer explanation with a selector slider
def render_local_explanation(stats: dict):
    st.markdown("### Local Explanation — Single Customer")
    st.markdown(
        f"<p style='color:{TEXT_MUTED};'>Select a customer to see which features drove their churn prediction.</p>",
        unsafe_allow_html=True,
    )

    shap_vals = stats["shap_values"].values
    X_test    = stats["X_test"]
    features  = stats["feature_names"]

    customer_idx = st.slider("Select Customer Index", 0, len(X_test) - 1, 0)

    local_df = pd.DataFrame({
        "Feature":    features,
        "SHAP Value": shap_vals[customer_idx],
    }).sort_values("SHAP Value", key=abs, ascending=False).head(10)

    local_df["Direction"] = local_df["SHAP Value"].apply(
        lambda x: "Increases Churn Risk" if x > 0 else "Decreases Churn Risk"
    )

    fig = px.bar(
        local_df, x="SHAP Value", y="Feature", orientation="h", color="Direction",
        color_discrete_map={
            "Increases Churn Risk": CHURN_COLOR,
            "Decreases Churn Risk": RETAINED_COLOR,
        },
        title=f"Customer #{customer_idx} — Feature Impact on Churn",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"),
                      paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)


# summary of high and low churn risk indicators
def render_business_insights():
    st.markdown("### Business Insights")
    col1, col2 = st.columns(2)

    with col1:
        st.error(
            "**High Churn Risk Indicators**\n\n"
            "- Month-to-month contract\n"
            "- Fiber optic internet service\n"
            "- Electronic check payment\n"
            "- Short tenure (0-12 months)\n"
            "- High monthly charges"
        )
    with col2:
        st.success(
            "**Low Churn Risk Indicators**\n\n"
            "- Two-year contract\n"
            "- Long tenure (48+ months)\n"
            "- Has partner or dependents\n"
            "- Automatic bank transfer payment\n"
            "- Lower monthly charges"
        )


# redirect to login if not logged in
if not st.session_state.get("logged_in"):
    st.switch_page("main.py")

apply_theme()

# back to home
st.page_link("pages/home.py", label="← Back to Home")

# header
st.title("SHAP Analysis")
st.markdown(
    f"<p style='color:{TEXT_MUTED}; margin-top:-15px;'>{DATASET_DETAIL} — Tuned XGBoost Interpretability</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# compute SHAP values (cached, uses the same tuned model as the Model Results page)
with st.spinner("Computing SHAP values..."):
    stats = get_cached_shap()

top10 = stats["top10"]

# page sections
render_intro()
render_global_importance(top10)
st.markdown("---")
render_top_drivers(top10)
st.markdown("---")
render_beeswarm(stats, top10)
st.markdown("---")
render_local_explanation(stats)
st.markdown("---")
render_business_insights()

show_footer()