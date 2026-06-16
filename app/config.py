import os

# Base Paths
ROOT_DIR = os.getcwd()  # B:\desertation project\customer_churn\

#Assets
LOGO_PATH = os.path.join(ROOT_DIR, "logo.png")

#App Info
APP_TITLE    = "IBM Telco Customer Churn Prediction"
DATASET_DETAIL = "IBM Telco Customer Churn Dataset"
APP_SUBTITLE = "UWS Dissertation Project"
APP_ICON     = LOGO_PATH


# dataset
DATASET_PATH = os.path.join(ROOT_DIR, "data", "telco_data.csv")


# authication
USERNAME = "admin"
PASSWORD = "admin123"