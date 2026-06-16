import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


def preprocess(df: pd.DataFrame):
    """
    Cleans and encodes dataset for prediction.
    Returns X, y, scaler, label encoders, and feature names.
    """
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    df.drop(columns=["customerID"], inplace=True)

    le = LabelEncoder()
    encoders = {}
    for col in df.select_dtypes(include="object").columns:
        encoders[col] = LabelEncoder()
        df[col] = encoders[col].fit_transform(df[col])

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    scaler  = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X, y, scaler, encoders


def train_models(df: pd.DataFrame) -> dict:
    """
    Trains LR, RF, XGBoost on full dataset.
    Returns trained models, scaler, encoders, and feature names.
    """
    X, y, scaler, encoders = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost":             XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
    }

    for name, model in models.items():
        Xtr = X_train_scaled if name == "Logistic Regression" else X_train
        model.fit(Xtr, y_train)

    return {
        "models":        models,
        "scaler":        scaler,
        "encoders":      encoders,
        "feature_names": list(X.columns),
    }


def predict_churn(input_dict: dict, trained: dict) -> dict:
    """
    Takes raw customer input, encodes it, and returns
    churn probability from all 3 models.
    """
    models   = trained["models"]
    scaler   = trained["scaler"]
    encoders = trained["encoders"]
    features = trained["feature_names"]

    # Encode input
    row = {}
    for col, val in input_dict.items():
        if col in encoders:
            le = encoders[col]
            if val in le.classes_:
                row[col] = le.transform([val])[0]
            else:
                row[col] = 0
        else:
            row[col] = val

    input_df     = pd.DataFrame([row])[features]
    input_scaled = scaler.transform(input_df)

    results = {}
    for name, model in models.items():
        X_in = input_scaled if name == "Logistic Regression" else input_df
        prob = model.predict_proba(X_in)[0][1]
        results[name] = round(prob * 100, 1)

    return results