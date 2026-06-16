import os
import pandas as pd
import streamlit as st
from config import DATASET_PATH

#fallback-url-- this is backup for if the local file not workikng
_DATASET_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"



# Loads the IBM Telco Customer Churn dataset.
# Loads from local file (data/raw/telco_data.csv)
# Falls back to downloading from IBM GitHub if file is missing
@st.cache_data
def load_data() -> pd.DataFrame:
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
    else:
        st.warning("Local file not found.Please wait...., Downloading from IBM GitHub...")
        df = pd.read_csv(_DATASET_URL)
        os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
        df.to_csv(DATASET_PATH, index=False)
        st.success("Dataset downloaded and saved locally!")

    return df