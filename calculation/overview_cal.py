import pandas as pd


# Computes all overview statistics from the dataframe.
# Returns a dictionary of stats used by 01_overview.py
def get_overview_stats(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")


    # Basic Stats
    total_customers  = len(df)
    total_features   = df.shape[1] - 1
    churned          = int(df["Churn"].value_counts().get("Yes", 0))
    retained         = int(df["Churn"].value_counts().get("No", 0))
    churn_rate       = round(churned / total_customers * 100, 1)
    retention_rate   = round(retained / total_customers * 100, 1)


    #Financial & Tenure
    avg_monthly      = round(df["MonthlyCharges"].mean(), 2)
    avg_total        = round(df["TotalCharges"].mean(), 2)
    avg_tenure       = round(df["tenure"].mean(), 1)
    max_tenure       = int(df["tenure"].max())


    #Demographics
    male_count       = int(df["gender"].value_counts().get("Male", 0))
    female_count     = int(df["gender"].value_counts().get("Female", 0))
    senior_count     = int(df["SeniorCitizen"].sum())
    senior_pct       = round(df["SeniorCitizen"].mean() * 100, 1)
    dependents_count = int(df["Dependents"].value_counts().get("Yes", 0))



    #Churn by Contract
    contract_stats = df.groupby("Contract").agg(
        Count=("Churn", "count"),
        ChurnRate=("Churn", lambda x: round((x == "Yes").mean() * 100, 1))
    ).reset_index()



    #Churn by Internet Service
    internet_stats = df.groupby("InternetService").agg(
        Count=("Churn", "count"),
        ChurnRate=("Churn", lambda x: round((x == "Yes").mean() * 100, 1))
    ).reset_index()

    return {
        "total_customers":  total_customers,
        "total_features":   total_features,
        "churned":          churned,
        "retained":         retained,
        "churn_rate":       churn_rate,
        "retention_rate":   retention_rate,
        "avg_monthly":      avg_monthly,
        "avg_total":        avg_total,
        "avg_tenure":       avg_tenure,
        "max_tenure":       max_tenure,
        "male_count":       male_count,
        "female_count":     female_count,
        "senior_count":     senior_count,
        "senior_pct":       senior_pct,
        "dependents_count": dependents_count,
        "contract_stats":   contract_stats,
        "internet_stats":   internet_stats,
    }