import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, roc_curve
)
from xgboost import XGBClassifier



# Cleans and encodes the dataset for model training.
def preprocess(df: pd.DataFrame):
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


# Trains LR, RF, XGBoost and returns evaluation metrics,
# confusion matrices, and ROC curve data.
def get_model_stats(df: pd.DataFrame) -> dict:
    X, y = preprocess(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale for Logistic Regression
    scaler  = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # Models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost":             XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
    }

    results      = []
    conf_matrices = {}
    roc_data      = {}

    for name, model in models.items():
        # Use scaled data for LR only
        Xtr = X_train_scaled if name == "Logistic Regression" else X_train
        Xte = X_test_scaled  if name == "Logistic Regression" else X_test

        model.fit(Xtr, y_train)
        y_pred = model.predict(Xte)
        y_prob = model.predict_proba(Xte)[:, 1]

        results.append({
            "Model":     name,
            "Accuracy":  round(accuracy_score(y_test, y_pred) * 100, 2),
            "Precision": round(precision_score(y_test, y_pred) * 100, 2),
            "Recall":    round(recall_score(y_test, y_pred) * 100, 2),
            "F1 Score":  round(f1_score(y_test, y_pred) * 100, 2),
            "ROC-AUC":   round(roc_auc_score(y_test, y_prob) * 100, 2),
        })

        conf_matrices[name] = confusion_matrix(y_test, y_pred)

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_data[name] = {"fpr": fpr, "tpr": tpr}

    results_df = pd.DataFrame(results)

    return {
        "results_df":    results_df,
        "conf_matrices": conf_matrices,
        "roc_data":      roc_data,
        "feature_names": list(X.columns),
        "models":        models,
        "X_test":        X_test,
        "y_test":        y_test,
    }