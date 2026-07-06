import sys
from pathlib import Path
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_DIR))

from config import APP_TITLE, APP_ICON
from auth.login import show_login_page

st.set_page_config(
    page_title=f"Login | {APP_TITLE}",
    page_icon=APP_ICON,
    layout="wide",
)

show_login_page()