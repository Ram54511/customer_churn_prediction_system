from pathlib import Path

# Base Paths — anchored to this file, so the app works
# no matter which directory it is launched from.
APP_DIR  = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent

# Assets
LOGO_PATH = str(ROOT_DIR / "logo.png")

# App Info
APP_TITLE      = "IBM Telco Customer Churn Prediction"
DATASET_DETAIL = "IBM Telco Customer Churn Dataset"
APP_SUBTITLE   = "UWS Dissertation Project"
APP_ICON       = LOGO_PATH

# Dataset
DATASET_PATH = str(ROOT_DIR / "data" / "telco_data.csv")

# Authentication (demo credentials — for a real deployment these would
# come from environment variables / a secrets manager, never source code)
USERNAME = "admin"
PASSWORD = "admin123"