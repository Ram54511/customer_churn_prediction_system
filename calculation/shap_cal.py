"""
SHAP analysis built on the SHARED tuned XGBoost pipeline (calculation.pipeline).
No separate model is trained here — the model being explained is exactly the
model whose metrics are reported on the Model Results page.
"""

import numpy as np
import pandas as pd
import shap

from calculation.pipeline import load_or_train


def get_shap_stats(df: pd.DataFrame, artifacts: dict | None = None) -> dict:
    if artifacts is None:
        artifacts = load_or_train(df)

    model = artifacts["pipelines"]["XGBoost"].named_steps["model"]
    X_test_t = artifacts["X_test_transformed"]
    feature_names = artifacts["feature_names"]

    # tree_path_dependent: exact TreeSHAP without a background dataset —
    # also required for compatibility with XGBoost >= 3.x
    explainer = shap.TreeExplainer(model, feature_perturbation="tree_path_dependent")
    shap_values = explainer(X_test_t)

    mean_shap = pd.DataFrame({
        "Feature":    feature_names,
        "Importance": np.abs(shap_values.values).mean(axis=0),
    }).sort_values("Importance", ascending=False).reset_index(drop=True)

    return {
        "shap_values":   shap_values,
        "X_test":        X_test_t,
        "mean_shap":     mean_shap,
        "top10":         mean_shap.head(10),
        "feature_names": feature_names,
        "model":         model,
    }