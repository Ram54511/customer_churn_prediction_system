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

from config import DATASET_DETAIL
from theme import apply_theme, TEXT_MUTED, PRIMARY, ACCENT, CHURN_COLOR
from header import show_header
from footer import show_footer
from data_loader import load_data
from auth.guard import require_login
from calculation.model_cal import get_model_stats

MODEL_COLORS = [PRIMARY, ACCENT, CHURN_COLOR]
METRICS = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]


# train once (or load saved artifacts) and share across reruns
@st.cache_resource(show_spinner=False)
def get_cached_stats():
    return get_model_stats(load_data())


# comparison table with the best model highlighted
def render_comparison_table(stats: dict, best_model: str):
    st.markdown("### Model Comparison")
    st.markdown(
        f"<p style='color:{TEXT_MUTED};'>Best performing model: "
        f"<b style='color:{PRIMARY};'>{best_model}</b> (highest ROC-AUC)</p>",
        unsafe_allow_html=True,
    )
    st.dataframe(
        stats["results_df"].style
        .highlight_max(subset=METRICS, color="#d4edda")
        .format("{:.2f}%", subset=METRICS),
        use_container_width=True,
        hide_index=True,
    )


# expandable methodology and tuning details
def render_methodology(stats: dict):
    with st.expander("Methodology: SMOTE, GridSearchCV & Threshold Optimisation"):
        st.markdown(
            """
- **Preprocessing:** numeric features standardised, categorical features
  one-hot encoded (no artificial ordinal relationships).
- **Class imbalance:** SMOTE oversampling applied inside each
  cross-validation fold only, so validation scores are never inflated.
- **Hyperparameter tuning:** GridSearchCV (3-fold stratified CV,
  optimising ROC-AUC) for every model.
- **Threshold optimisation:** the decision threshold is tuned to maximise
  F1 on cross-validated training predictions (never the test set).
  Metrics above are reported at each model's optimised threshold; the
  Recall @0.50 and F1 @0.50 columns show the untuned baseline.
            """
        )
        st.markdown("**Best hyperparameters found:**")
        rows = [{"Model": m,
                 "Best Parameters": ", ".join(f"{k.replace('model__', '')}={v}" for k, v in p.items()),
                 "Optimised Threshold": round(stats["thresholds"][m], 3)}
                for m, p in stats["best_params"].items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# grouped bar chart of all metrics
def render_metrics_chart(results_df: pd.DataFrame):
    st.markdown("### Metrics Comparison")
    melted = results_df.melt(id_vars="Model", value_vars=METRICS,
                             var_name="Metric", value_name="Score")
    fig = px.bar(
        melted, x="Metric", y="Score", color="Model", barmode="group",
        title="Model Performance Comparison",
        color_discrete_sequence=MODEL_COLORS, text="Score",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                      yaxis=dict(range=[0, 110]))
    st.plotly_chart(fig, use_container_width=True)


# roc curves for all models plus the random-classifier baseline
def render_roc_curves(stats: dict):
    st.markdown("### ROC Curves")
    results_df = stats["results_df"]
    fig = go.Figure()

    for i, (model_name, roc) in enumerate(stats["roc_data"].items()):
        auc = results_df.loc[results_df["Model"] == model_name, "ROC-AUC"].values[0]
        fig.add_trace(go.Scatter(
            x=roc["fpr"], y=roc["tpr"],
            name=f"{model_name} (AUC={auc:.1f}%)",
            line=dict(color=MODEL_COLORS[i], width=2),
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
        paper_bgcolor="white", plot_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)


# confusion matrix heatmap for each model
def render_confusion_matrices(stats: dict):
    st.markdown("### Confusion Matrices")
    cols = st.columns(3)

    for col, (model_name, cm) in zip(cols, stats["conf_matrices"].items()):
        with col:
            fig = px.imshow(
                cm, text_auto=True,
                color_continuous_scale=[[0, "white"], [1, PRIMARY]],
                title=model_name,
                labels=dict(x="Predicted", y="Actual"),
                x=["Not Churn", "Churn"], y=["Not Churn", "Churn"],
            )
            fig.update_layout(paper_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)


# summary card per model, best one highlighted
def render_key_findings(results_df: pd.DataFrame, best_model: str):
    st.markdown("### Key Findings")
    cols = st.columns(3)

    for col, (_, row) in zip(cols, results_df.iterrows()):
        body = (
            f"**{row['Model']}{' — Best' if row['Model'] == best_model else ''}**\n\n"
            f"Accuracy: {row['Accuracy']}%\n\n"
            f"F1 Score: {row['F1 Score']}%\n\n"
            f"ROC-AUC: {row['ROC-AUC']}%"
        )
        with col:
            if row["Model"] == best_model:
                st.success(body)
            else:
                st.info(body)


# login guard: restores session from the signed url token
require_login()

apply_theme()

# header bar (handles logout)
show_header("Model Results", DATASET_DETAIL, back=True)

# load models (trained once, persisted with joblib, cached by Streamlit)
with st.spinner("Loading models (first run trains & tunes — about 1 min)..."):
    stats = get_cached_stats()

results_df = stats["results_df"]
best_model = results_df.loc[results_df["ROC-AUC"].idxmax(), "Model"]

# page sections
render_comparison_table(stats, best_model)
render_methodology(stats)
st.markdown("<br>", unsafe_allow_html=True)
render_metrics_chart(results_df)
st.markdown("---")
render_roc_curves(stats)
st.markdown("---")
render_confusion_matrices(stats)
st.markdown("---")
render_key_findings(results_df, best_model)

show_footer()