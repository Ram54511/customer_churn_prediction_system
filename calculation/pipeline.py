"""
Shared ML pipeline for the Customer Churn project.

This module is the SINGLE source of truth for:
  - data cleaning
  - preprocessing (one-hot encoding + scaling)
  - class-imbalance handling (SMOTE, applied inside CV folds only)
  - hyperparameter tuning (GridSearchCV)
  - decision-threshold optimisation (maximising F1 on cross-validated
    training predictions — never on the test set)
  - model persistence (joblib)

All pages (Model Results, SHAP, Live Predict) consume the same trained
artifacts, so reported metrics and live predictions always agree.
"""

import os
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    train_test_split, StratifiedKFold, GridSearchCV, cross_val_predict
)
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, roc_curve,
    precision_recall_curve,
)
from xgboost import XGBClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE

RANDOM_STATE = 42
ARTIFACT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
ARTIFACT_PATH = os.path.join(ARTIFACT_DIR, "churn_artifacts.joblib")


# Data cleaning
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning shared by every consumer of the dataset."""
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    # The 11 blank TotalCharges rows are all tenure==0 customers:
    # their true total spend is 0, so impute rather than drop.
    df["TotalCharges"] = df["TotalCharges"].fillna(0)
    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])
    return df


def split_features_target(df: pd.DataFrame):
    df = clean_data(df)
    X = df.drop(columns=["Churn"])
    y = (df["Churn"] == "Yes").astype(int)
    return X, y


# Preprocessor (shared by all models)
def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """
    One-hot encode nominal categoricals (no fake ordinal relationships),
    scale numeric features. handle_unknown='ignore' makes live prediction
    robust to unseen categories.
    """
    categorical = X.select_dtypes(include="object").columns.tolist()
    numeric = X.select_dtypes(exclude="object").columns.tolist()

    return ColumnTransformer([
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(drop="if_binary", handle_unknown="ignore"), categorical),
    ])


# Model definitions + hyperparameter grids
def model_grids():
    return {
        "Logistic Regression": (
            LogisticRegression(max_iter=2000, random_state=RANDOM_STATE),
            {"model__C": [0.01, 0.1, 1, 10]},
        ),
        "Random Forest": (
            RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1),
            {"model__max_depth": [6, 10, None],
             "model__min_samples_leaf": [1, 4]},
        ),
        "XGBoost": (
            XGBClassifier(eval_metric="logloss", random_state=RANDOM_STATE, n_jobs=-1),
            {"model__n_estimators": [200, 400],
             "model__max_depth": [3, 5],
             "model__learning_rate": [0.05, 0.1]},
        ),
    }


def optimise_threshold(y_true, y_prob) -> float:
    """Return the probability threshold that maximises F1."""
    precision, recall, thresholds = precision_recall_curve(y_true, y_prob)
    f1 = 2 * precision * recall / (precision + recall + 1e-12)
    # precision_recall_curve returns one more point than thresholds
    best_idx = int(np.argmax(f1[:-1]))
    return float(thresholds[best_idx])


# Training
def train_all(df: pd.DataFrame, verbose: bool = False) -> dict:
    """
    Full training routine:
      1. 80/20 stratified train/test split
      2. For each model: Pipeline(preprocess -> SMOTE -> model)
         tuned with GridSearchCV (SMOTE is applied only to training folds,
         so validation scores are computed on untouched data)
      3. Decision threshold tuned on cross-validated TRAINING predictions
      4. Final evaluation on the untouched test set at both the default
         (0.50) and the optimised threshold
    """
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=RANDOM_STATE)

    results, conf_matrices, roc_data = [], {}, {}
    best_pipelines, thresholds, best_params = {}, {}, {}

    for name, (estimator, grid) in model_grids().items():
        if verbose:
            print(f"Tuning {name} ...")

        pipe = ImbPipeline([
            ("preprocess", build_preprocessor(X)),
            ("smote", SMOTE(random_state=RANDOM_STATE)),
            ("model", estimator),
        ])

        search = GridSearchCV(pipe, grid, cv=cv, scoring="roc_auc", n_jobs=-1)
        search.fit(X_train, y_train)
        best = search.best_estimator_
        best_pipelines[name] = best
        best_params[name] = search.best_params_

        # Threshold tuning on cross-validated training predictions (no leakage)
        cv_prob = cross_val_predict(best, X_train, y_train, cv=cv,
                                    method="predict_proba", n_jobs=-1)[:, 1]
        thr = optimise_threshold(y_train, cv_prob)
        thresholds[name] = thr

        # Final evaluation on hold-out test set
        y_prob = best.predict_proba(X_test)[:, 1]
        y_pred_default = (y_prob >= 0.5).astype(int)
        y_pred_tuned = (y_prob >= thr).astype(int)

        results.append({
            "Model":        name,
            "Accuracy":     round(accuracy_score(y_test, y_pred_tuned) * 100, 2),
            "Precision":    round(precision_score(y_test, y_pred_tuned) * 100, 2),
            "Recall":       round(recall_score(y_test, y_pred_tuned) * 100, 2),
            "F1 Score":     round(f1_score(y_test, y_pred_tuned) * 100, 2),
            "ROC-AUC":      round(roc_auc_score(y_test, y_prob) * 100, 2),
            "Recall @0.50": round(recall_score(y_test, y_pred_default) * 100, 2),
            "F1 @0.50":     round(f1_score(y_test, y_pred_default) * 100, 2),
            "Threshold":    round(thr, 3),
        })
        conf_matrices[name] = confusion_matrix(y_test, y_pred_tuned)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_data[name] = {"fpr": fpr, "tpr": tpr}

    results_df = pd.DataFrame(results)


    # Transformed test matrix + feature names (used by the SHAP page)
    xgb_pipe = best_pipelines["XGBoost"]
    pre = xgb_pipe.named_steps["preprocess"]
    feature_names = [n.split("__", 1)[1] for n in pre.get_feature_names_out()]
    X_test_transformed = pd.DataFrame(
        pre.transform(X_test), columns=feature_names, index=X_test.index
    )

    return {
        "results_df":         results_df,
        "conf_matrices":      conf_matrices,
        "roc_data":           roc_data,
        "pipelines":          best_pipelines,
        "best_params":        best_params,
        "thresholds":         thresholds,
        "feature_names":      feature_names,
        "raw_feature_names":  list(X.columns),
        "X_test":             X_test,
        "y_test":             y_test,
        "X_test_transformed": X_test_transformed,
    }


# Persistence
def load_or_train(df: pd.DataFrame, force_retrain: bool = False) -> dict:
    """Load saved artifacts if present, otherwise train once and save."""
    if not force_retrain and os.path.exists(ARTIFACT_PATH):
        try:
            return joblib.load(ARTIFACT_PATH)
        except Exception:
            pass  # corrupt/incompatible file -> retrain
    artifacts = train_all(df)
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    joblib.dump(artifacts, ARTIFACT_PATH, compress=3)
    return artifacts


# Live prediction
def predict_single(input_dict: dict, artifacts: dict) -> dict:
    """
    Predict churn probability for one customer with every trained pipeline.
    Returns {model_name: {"probability": %, "threshold": %, "will_churn": bool}}.
    The SAME pipelines evaluated on the Model page are used here.
    """
    row = pd.DataFrame([input_dict])[artifacts["raw_feature_names"]]
    out = {}
    for name, pipe in artifacts["pipelines"].items():
        prob = float(pipe.predict_proba(row)[0, 1])
        thr = artifacts["thresholds"][name]
        out[name] = {
            "probability": round(prob * 100, 1),
            "threshold":   round(thr * 100, 1),
            "will_churn":  prob >= thr,
        }
    return out