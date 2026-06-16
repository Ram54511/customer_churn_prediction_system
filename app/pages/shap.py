import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)
from config import DATASET_PATH, DATASET_DETAIL
from theme import apply_theme, TEXT_MUTED, PRIMARY, ACCENT, CHURN_COLOR, RETAINED_COLOR
from footer import show_footer
from calculation.shap_cal import get_shap_stats

# ── Guard ──────────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("login.py")
 
# ── Apply theme ────────────────────────────────────────────────────────────────
apply_theme()
 
# ── Load data & compute SHAP ───────────────────────────────────────────────────
df = pd.read_csv(DATASET_PATH)
 
with st.spinner("⏳ Computing SHAP values... please wait"):
    stats = get_shap_stats(df)
 
# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"<h4 style='color:white;'>👤 {st.session_state.get('username', 'admin')}</h4>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("<p style='color:white;'>📌 Navigation</p>", unsafe_allow_html=True)
    st.page_link("pages/home.py",     label="🏠 Home")
    st.page_link("pages/overview.py", label="📊 Overview")
    st.page_link("pages/eda.py",      label="🔍 EDA")
    st.page_link("pages/model.py",    label="🤖 Model Results")
    st.page_link("pages/shap.py",     label="🧠 SHAP Analysis")
    # st.page_link("pages/predict.py",  label="🎯 Live Predict")
    for _ in range(10):
        st.write("")
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("login.py")
 
# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🧠 SHAP Analysis")
st.markdown(
    f"<p style='color:{TEXT_MUTED}; margin-top:-15px;'>{DATASET_DETAIL} — XGBoost Interpretability</p>",
    unsafe_allow_html=True,
)
st.markdown("---")
 
# ── What is SHAP ──────────────────────────────────────────────────────────────
st.markdown("### ℹ️ What is SHAP?")
st.markdown(
    f"""<p style='color:{TEXT_MUTED};'>
    <b>SHAP (SHapley Additive exPlanations)</b> is a game-theoretic approach to explain the output
    of any machine learning model. It tells us <b>how much each feature contributes</b> to a prediction —
    both globally (across all customers) and locally (for a single customer).
    </p>""",
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)
 
# ── Section 1: Global Feature Importance ─────────────────────────────────────
st.markdown("### 🌍 Global Feature Importance")
st.markdown(
    f"<p style='color:{TEXT_MUTED};'>Average impact of each feature on churn prediction across all customers.</p>",
    unsafe_allow_html=True,
)
 
top10 = stats["top10"]
 
fig = px.bar(
    top10,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Top 10 Features by Mean SHAP Value",
    color="Importance",
    color_continuous_scale=[[0, RETAINED_COLOR], [0.5, ACCENT], [1, CHURN_COLOR]],
    text=top10["Importance"].round(4),
)
fig.update_layout(
    yaxis=dict(autorange="reversed"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    showlegend=False,
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)
 
st.markdown("---")
 
# ── Section 2: Top Features Cards ────────────────────────────────────────────
st.markdown("### 🏆 Top 5 Churn Drivers")
cols = st.columns(5)
for i, (col, (_, row)) in enumerate(zip(cols, top10.head(5).iterrows())):
    with col:
        st.markdown(
            f"""<div style='background:white; padding:14px; border-radius:8px;
                        border-top:4px solid {PRIMARY}; text-align:center;'>
                <h3 style='color:{PRIMARY}; margin:0;'>#{i+1}</h3>
                <b style='color:#212529;'>{row['Feature']}</b><br>
                <span style='color:{ACCENT}; font-size:13px;'>{row['Importance']:.4f}</span>
            </div>""",
            unsafe_allow_html=True,
        )
 
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
 
# ── Section 3: SHAP Beeswarm (manual using plotly) ───────────────────────────
st.markdown("### 🐝 SHAP Value Distribution (Top 10 Features)")
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
top10_features = top10["Feature"].tolist()
 
rows = []
for feat in top10_features:
    idx = features.index(feat)
    feat_vals  = X_test.iloc[:, idx].values
    shap_col   = shap_vals[:, idx]
    norm_vals  = (feat_vals - feat_vals.min()) / (feat_vals.max() - feat_vals.min() + 1e-9)
    for sv, nv in zip(shap_col, norm_vals):
        rows.append({"Feature": feat, "SHAP Value": sv, "Feature Value": nv})
 
beeswarm_df = pd.DataFrame(rows)
 
fig = px.scatter(
    beeswarm_df,
    x="SHAP Value",
    y="Feature",
    color="Feature Value",
    color_continuous_scale=[[0, RETAINED_COLOR], [1, CHURN_COLOR]],
    title="SHAP Beeswarm Plot",
    opacity=0.6,
)
fig.update_layout(
    yaxis=dict(autorange="reversed"),
    paper_bgcolor="white",
    plot_bgcolor="white",
)
st.plotly_chart(fig, use_container_width=True)
 
st.markdown("---")
 
# ── Section 4: Local Explanation ──────────────────────────────────────────────
st.markdown("### 🔍 Local Explanation — Single Customer")
st.markdown(
    f"<p style='color:{TEXT_MUTED};'>Select a customer to see which features drove their churn prediction.</p>",
    unsafe_allow_html=True,
)
 
customer_idx = st.slider("Select Customer Index", 0, len(X_test) - 1, 0)
 
local_shap = shap_vals[customer_idx]
local_df   = pd.DataFrame({
    "Feature": features,
    "SHAP Value": local_shap,
}).sort_values("SHAP Value", key=abs, ascending=False).head(10)
 
local_df["Color"] = local_df["SHAP Value"].apply(
    lambda x: CHURN_COLOR if x > 0 else RETAINED_COLOR
)
local_df["Direction"] = local_df["SHAP Value"].apply(
    lambda x: "↑ Increases Churn Risk" if x > 0 else "↓ Decreases Churn Risk"
)
 
fig = px.bar(
    local_df,
    x="SHAP Value",
    y="Feature",
    orientation="h",
    color="Direction",
    color_discrete_map={
        "↑ Increases Churn Risk": CHURN_COLOR,
        "↓ Decreases Churn Risk": RETAINED_COLOR,
    },
    title=f"Customer #{customer_idx} — Feature Impact on Churn",
)
fig.update_layout(
    yaxis=dict(autorange="reversed"),
    paper_bgcolor="white",
    plot_bgcolor="white",
)
st.plotly_chart(fig, use_container_width=True)
 
st.markdown("---")
 
# ── Section 5: Business Insights ─────────────────────────────────────────────
st.markdown("### 💡 Business Insights")
col1, col2 = st.columns(2)
 
with col1:
    st.error(
        "**⚠️ High Churn Risk Indicators**\n\n"
        "- Month-to-month contract\n"
        "- Fiber optic internet service\n"
        "- Electronic check payment\n"
        "- Short tenure (0-12 months)\n"
        "- High monthly charges"
    )
with col2:
    st.success(
        "**✅ Low Churn Risk Indicators**\n\n"
        "- Two-year contract\n"
        "- Long tenure (48+ months)\n"
        "- Has partner or dependents\n"
        "- Automatic bank transfer payment\n"
        "- Lower monthly charges"
    )
 
# ── Footer ────────────────────────────────────────────────────────────────────
show_footer()