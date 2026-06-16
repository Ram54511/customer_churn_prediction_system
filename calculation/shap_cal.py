import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
import shap


def preprocess(df: pd.DataFrame):
    """
    Cleans and encodes dataset for SHAP analysis.
    """
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    df.drop(columns=["customerID"], inplace=True)

    le = LabelEncoder()
    for col in df.select_dtypes(include="object").columns:
        df[col] = le.fit_transform(df[col])

    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    return X, y


def get_shap_stats(df: pd.DataFrame) -> dict:
    """
    Trains XGBoost and computes SHAP values.
    Returns feature importance and SHAP values for the SHAP page.
    """
    X, y = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ── Train XGBoost ─────────────────────────────────────────────────────────
    model = XGBClassifier(
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42
    )
    model.fit(X_train, y_train)

    # ── SHAP Values ───────────────────────────────────────────────────────────
    explainer   = shap.Explainer(model, X_train)
    shap_values = explainer(X_test)

    # ── Global Feature Importance ─────────────────────────────────────────────
    mean_shap = pd.DataFrame({
        "Feature":    X.columns,
        "Importance": np.abs(shap_values.values).mean(axis=0),
    }).sort_values("Importance", ascending=False).reset_index(drop=True)

    # ── Top 10 features ───────────────────────────────────────────────────────
    top10 = mean_shap.head(10)

    return {
        "shap_values":  shap_values,
        "X_test":       X_test,
        "mean_shap":    mean_shap,
        "top10":        top10,
        "feature_names": list(X.columns),
        "model":        model,
    }