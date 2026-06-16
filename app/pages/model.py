import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Path setup 
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)



from config import DATASET_PATH, DATASET_DETAIL
from theme import apply_theme, TEXT_MUTED, PRIMARY, ACCENT, CHURN_COLOR, RETAINED_COLOR
from footer import show_footer
from calculation.model_cal import get_model_stats

# Guard
if not st.session_state.get("logged_in"):
    st.switch_page("login.py")

# Apply theme
apply_theme()

# Load data & train models 
df = pd.read_csv(DATASET_PATH)

with st.spinner("⏳ Training models... please wait"):
    stats = get_model_stats(df)

# Sidebar
with st.sidebar:
    st.markdown(
        f"<h4 style='color:white;'>👤 {st.session_state.get('username', 'admin')}</h4>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    # st.markdown("<p style='color:white;'>📌 Navigation</p>", unsafe_allow_html=True)
    # st.page_link("pages/home.py",         label="🏠 Home")
    # st.page_link("pages/overview.py",     label="📊 Overview")
    # st.page_link("pages/eda.py",          label="🔍 EDA")
    # st.page_link("pages/model.py",label="🤖 Model Results")
    # st.page_link("pages/shap.py",         label="🧠 SHAP Analysis")
    # st.page_link("pages/predict.py",      label="🎯 Live Predict")
    for _ in range(10):
        st.write("")
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("login.py")

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🤖 Model Results")
st.markdown(
    f"<p style='color:{TEXT_MUTED}; margin-top:-15px;'>{DATASET_DETAIL}</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ── Section 1: Model Comparison Table ────────────────────────────────────────
st.markdown("### 📊 Model Comparison")
results_df = stats["results_df"]

# Highlight best model
best_model = results_df.loc[results_df["ROC-AUC"].idxmax(), "Model"]
st.markdown(
    f"<p style='color:{TEXT_MUTED};'>Best performing model: "
    f"<b style='color:{PRIMARY};'>{best_model}</b> (highest ROC-AUC)</p>",
    unsafe_allow_html=True,
)

st.dataframe(
    results_df.style
    .highlight_max(subset=["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"],
                   color="#d4edda")
    .format("{:.2f}%", subset=["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]),
    use_container_width=True,
    hide_index=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 2: Metrics Bar Chart ─────────────────────────────────────────────
st.markdown("### 📈 Metrics Comparison")
metrics = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]
melted  = results_df.melt(id_vars="Model", value_vars=metrics, var_name="Metric", value_name="Score")

fig = px.bar(
    melted,
    x="Metric",
    y="Score",
    color="Model",
    barmode="group",
    title="Model Performance Comparison",
    color_discrete_sequence=[PRIMARY, ACCENT, CHURN_COLOR],
    text="Score",
)
fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    yaxis=dict(range=[0, 110]),
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Section 3: ROC Curve ──────────────────────────────────────────────────────
st.markdown("### 📉 ROC Curves")
fig = go.Figure()

colors = [PRIMARY, ACCENT, CHURN_COLOR]
for i, (model_name, roc) in enumerate(stats["roc_data"].items()):
    auc = results_df.loc[results_df["Model"] == model_name, "ROC-AUC"].values[0]
    fig.add_trace(go.Scatter(
        x=roc["fpr"],
        y=roc["tpr"],
        name=f"{model_name} (AUC={auc:.1f}%)",
        line=dict(color=colors[i], width=2),
    ))

fig.add_trace(go.Scatter(
    x=[0, 1], y=[0, 1],
    name="Random Classifier",
    line=dict(color="grey", dash="dash"),
))
fig.update_layout(
    title="ROC Curve Comparison",
    xaxis_title="False Positive Rate",
    yaxis_title="True Positive Rate",
    paper_bgcolor="white",
    plot_bgcolor="white",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Section 4: Confusion Matrices ────────────────────────────────────────────
st.markdown("### 🔢 Confusion Matrices")
col1, col2, col3 = st.columns(3)

for col, (model_name, cm) in zip([col1, col2, col3], stats["conf_matrices"].items()):
    with col:
        fig = px.imshow(
            cm,
            text_auto=True,
            color_continuous_scale=[[0, "white"], [1, PRIMARY]],
            title=model_name,
            labels=dict(x="Predicted", y="Actual"),
            x=["Not Churn", "Churn"],
            y=["Not Churn", "Churn"],
        )
        fig.update_layout(paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Section 5: Key Findings ───────────────────────────────────────────────────
st.markdown("### 💡 Key Findings")
col1, col2, col3 = st.columns(3)

with col1:
    lr = results_df[results_df["Model"] == "Logistic Regression"].iloc[0]
    st.info(
        f"**Logistic Regression**\n\n"
        f"Accuracy: {lr['Accuracy']}%\n\n"
        f"F1 Score: {lr['F1 Score']}%\n\n"
        f"ROC-AUC: {lr['ROC-AUC']}%"
    )
with col2:
    rf = results_df[results_df["Model"] == "Random Forest"].iloc[0]
    st.info(
        f"**Random Forest**\n\n"
        f"Accuracy: {rf['Accuracy']}%\n\n"
        f"F1 Score: {rf['F1 Score']}%\n\n"
        f"ROC-AUC: {rf['ROC-AUC']}%"
    )
with col3:
    xgb = results_df[results_df["Model"] == "XGBoost"].iloc[0]
    st.success(
        f"**XGBoost ✅ Best**\n\n"
        f"Accuracy: {xgb['Accuracy']}%\n\n"
        f"F1 Score: {xgb['F1 Score']}%\n\n"
        f"ROC-AUC: {xgb['ROC-AUC']}%"
    )

# ── Footer ────────────────────────────────────────────────────────────────────
show_footer()