import streamlit as st
from theme import TEXT_CAPTION


def show_footer():
    st.markdown("---")
    st.markdown(
        f"<p style='text-align:center; color:{TEXT_CAPTION}; font-size:12px;'>"
        f"IBM Telco Customer Churn Dataset &nbsp "
        f"MSc Data Analysis | UWS 2025–2026</p>",
        unsafe_allow_html=True,
    )