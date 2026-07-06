import streamlit as st
from config import DATASET_DETAIL
from styles.footer import apply_footer_styles


def show_footer():
    apply_footer_styles()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='app-footer'>
            <p class='footer-title'>Customer Churn Prediction System</p>
            <p class='footer-meta'>
                {DATASET_DETAIL} &nbsp;&middot;&nbsp; MSc Data Analysis &nbsp;&middot;&nbsp; UWS 2025&ndash;2026
            </p>
            <p class='footer-stack'>
                Built with Streamlit &nbsp;&middot;&nbsp; scikit-learn &nbsp;&middot;&nbsp; XGBoost &nbsp;&middot;&nbsp; SHAP
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )