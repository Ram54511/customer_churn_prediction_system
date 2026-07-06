import sys
from pathlib import Path
import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))

from config import LOGO_PATH, APP_TITLE, USERNAME, PASSWORD
from styles.login import apply_login_styles


def show_login_page():
    # Apply login styles
    apply_login_styles()

    # Redirect if already logged in
    if st.session_state.get("logged_in"):
        st.switch_page("pages/home.py")

    # Card for the login page
    st.markdown("<br><br>", unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.2, 1])

    with center:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)

        logo_col, title_col = st.columns([1, 4])

        with logo_col:
            st.image(LOGO_PATH, width=70)

        with title_col:
            st.markdown(
                f"""
                <div style='display:flex; align-items:center; height:70px;'>
                    <p class='login-title' style='margin:0; font-size:40px;'>{APP_TITLE}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<hr class='login-divider'>", unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input(
            "Password",
            placeholder="Enter your password",
            type="password"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        login_btn = st.button(
            "Login →",
            use_container_width=True,
            type="primary"
        )

        if login_btn:
            if username == "" or password == "":
                st.warning("Please enter both username and password.")

            elif username == USERNAME and password == PASSWORD:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.switch_page("pages/home.py")

            else:
                st.error("Incorrect username or password.")

        st.markdown(
            "<p class='login-footer'>MSc Data Analysis &nbsp;·&nbsp; UWS &nbsp;·&nbsp; 2025–2026</p>",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)