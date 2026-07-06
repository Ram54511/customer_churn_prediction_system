"""
Model Results page backend — thin wrapper over the shared pipeline.
Kept for backwards compatibility: all real logic lives in calculation.pipeline.
"""

import pandas as pd
from calculation.pipeline import load_or_train


def get_model_stats(df: pd.DataFrame) -> dict:
    art = load_or_train(df)
    return {
        "results_df":    art["results_df"],
        "conf_matrices": art["conf_matrices"],
        "roc_data":      art["roc_data"],
        "feature_names": art["feature_names"],
        "models":        art["pipelines"],
        "best_params":   art["best_params"],
        "thresholds":    art["thresholds"],
        "X_test":        art["X_test"],
        "y_test":        art["y_test"],
    }