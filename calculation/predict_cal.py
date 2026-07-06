"""
Live Predict page backend — thin wrapper over the shared pipeline.
The models used here are the EXACT tuned pipelines evaluated on the
Model Results page, loaded from the saved joblib artifacts.
"""

import pandas as pd
from calculation.pipeline import load_or_train, predict_single


def train_models(df: pd.DataFrame) -> dict:
    """Load (or train once) the shared artifacts."""
    return load_or_train(df)


def predict_churn(input_dict: dict, trained: dict) -> dict:
    """
    Returns {model_name: {"probability": %, "threshold": %, "will_churn": bool}}
    using each model's optimised decision threshold.
    """
    return predict_single(input_dict, trained)