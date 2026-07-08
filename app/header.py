import base64
from pathlib import Path
import streamlit as st
from styles.header import apply_header_styles

# logo at project root
LOGO_PATH = Path(__file__).resolve().parent.parent / "logo.png"


# read the logo as a base64 data uri, or empty string if missing
@st.cache_data(show_spinner=False)
def logo_data_uri() -> str:
    if not LOGO_PATH.exists():
        return ""
    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return f"data:image/png;base64,{encoded}"


# slim full-width header bar with hamburger nav
# optional title/subtitle rendered as a page heading below the bar
# back=True shows a back-to-home button (use on every page except home)
def show_header(title: str = "", subtitle: str = "", back: bool = False):
    apply_header_styles()

    # handle logout from navbar on any page
    if st.query_params.get("logout") == "true":
        st.query_params.clear()
        st.session_state.clear()
        st.switch_page("main.py")

    logo = logo_data_uri()
    brand_logo = f'<img src="{logo}" class="brand-logo" alt="logo">' if logo \
                 else '<span class="brand-dot">&#9679;</span>'

    # carry the auth token on every nav link so login survives navigation
    token = st.query_params.get("auth", "")
    q = f"?auth={token}" if token else ""

    st.markdown(f"""
<div class="app-header">
    <a class="nav-brand" href="/home{q}" target="_self">{brand_logo}<span>Churn System</span></a>
    <div class="header-right">
        <a class="logout-btn" href="?logout=true">Logout</a>
        <input type="checkbox" id="nav-toggle" class="nav-toggle">
        <label for="nav-toggle" class="hamburger" aria-label="Menu">
            <span></span><span></span><span></span>
        </label>
        <div class="nav-menu">
            <a href="/home{q}">Home</a>
            <a href="/overview{q}">Overview</a>
            <a href="/eda{q}">EDA</a>
            <a href="/model{q}">Models</a>
            <a href="/shap{q}">SHAP</a>
            <a href="/predict{q}">Predict</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    if back:
        st.markdown(
            f'<a class="back-btn" href="/home{q}" target="_self">&larr; Back to Home</a>',
            unsafe_allow_html=True,
        )

    if title:
        st.markdown(f"""
<div class="page-heading">
    <h1>{title}</h1>
    <p>{subtitle}</p>
</div>
""", unsafe_allow_html=True)