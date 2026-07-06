import streamlit as st
from theme import TEXT_CAPTION, TEXT_MUTED


# footer css, injected once per page
def apply_footer_styles():
    st.markdown(
        f"""
        <style>
            .app-footer {{
                border-top: 1px solid #e9ecef;
                margin-top: 24px;
                padding: 18px 0 8px 0;
                text-align: center;
            }}

            .app-footer .footer-title {{
                color: {TEXT_MUTED};
                font-size: 13px;
                font-weight: 600;
                margin: 0;
            }}

            .app-footer .footer-meta {{
                color: {TEXT_CAPTION};
                font-size: 12px;
                margin: 4px 0 0 0;
            }}

            .app-footer .footer-stack {{
                color: {TEXT_CAPTION};
                font-size: 11px;
                margin: 6px 0 0 0;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )