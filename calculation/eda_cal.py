import pandas as pd


 
# Computes all stats and distributions for the EDA page.
def get_eda_stats(df: pd.DataFrame) -> dict:
   
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")


    # Churn Distribution
    churn_counts = df["Churn"].value_counts().reset_index()
    churn_counts.columns = ["Churn", "Count"]


    # Tenure Distribution
    tenure_bins = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 48, 72],
        labels=["0-12 months", "13-24 months", "25-48 months", "49-72 months"]
    )
    tenure_dist = tenure_bins.value_counts().sort_index().reset_index()
    tenure_dist.columns = ["Tenure Group", "Count"]



    # Monthly Charges by Churn
    monthly_churn = df.groupby("Churn")["MonthlyCharges"].mean().round(2).reset_index()
    monthly_churn.columns = ["Churn", "AvgMonthlyCharges"]


    #Churn by Gender
    gender_churn = df.groupby("gender").agg(
        Count=("Churn", "count"),
        ChurnRate=("Churn", lambda x: round((x == "Yes").mean() * 100, 1))
    ).reset_index()


    # Churn by Senior Citizen
    senior_churn = df.groupby("SeniorCitizen").agg(
        Count=("Churn", "count"),
        ChurnRate=("Churn", lambda x: round((x == "Yes").mean() * 100, 1))
    ).reset_index()
    senior_churn["SeniorCitizen"] = senior_churn["SeniorCitizen"].map({0: "Non-Senior", 1: "Senior"})


    #Churn by Contract
    contract_churn = df.groupby("Contract").agg(
        Count=("Churn", "count"),
        ChurnRate=("Churn", lambda x: round((x == "Yes").mean() * 100, 1))
    ).reset_index()


    # Churn by Internet Service
    internet_churn = df.groupby("InternetService").agg(
        Count=("Churn", "count"),
        ChurnRate=("Churn", lambda x: round((x == "Yes").mean() * 100, 1))
    ).reset_index()


    #Churn by Payment Method 
    payment_churn = df.groupby("PaymentMethod").agg(
        Count=("Churn", "count"),
        ChurnRate=("Churn", lambda x: round((x == "Yes").mean() * 100, 1))
    ).reset_index()



    # Churn by Partner & Dependents
    partner_churn = df.groupby("Partner").agg(
        ChurnRate=("Churn", lambda x: round((x == "Yes").mean() * 100, 1))
    ).reset_index()

    dependent_churn = df.groupby("Dependents").agg(
        ChurnRate=("Churn", lambda x: round((x == "Yes").mean() * 100, 1))
    ).reset_index()

    return {
        "df":               df,
        "churn_counts":     churn_counts,
        "tenure_dist":      tenure_dist,
        "monthly_churn":    monthly_churn,
        "gender_churn":     gender_churn,
        "senior_churn":     senior_churn,
        "contract_churn":   contract_churn,
        "internet_churn":   internet_churn,
        "payment_churn":    payment_churn,
        "partner_churn":    partner_churn,
        "dependent_churn":  dependent_churn,
    }