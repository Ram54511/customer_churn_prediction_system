import streamlit as st
from styles.header import apply_header_styles


# slim full-width header bar with hamburger nav
# optional title/subtitle rendered as a page heading below the bar
def show_header(title: str = "", subtitle: str = ""):
    apply_header_styles()

    # handle logout from navbar on any page
    if st.query_params.get("logout") == "true":
        st.query_params.clear()
        st.session_state.clear()
        st.switch_page("main.py")

    st.markdown("""
<div class="app-header">
    <div class="nav-brand"><span class="brand-dot">&#9679;</span><span>Churn System</span></div>
    <div class="header-right">
        <a class="logout-btn" href="?logout=true">Logout</a>
        <input type="checkbox" id="nav-toggle" class="nav-toggle">
        <label for="nav-toggle" class="hamburger" aria-label="Menu">
            <span></span><span></span><span></span>
        </label>
        <div class="nav-menu">
            <a href="/home">Home</a>
            <a href="/overview">Overview</a>
            <a href="/eda">EDA</a>
            <a href="/model">Models</a>
            <a href="/shap">SHAP</a>
            <a href="/predict">Predict</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    if title:
        st.markdown(f"""
<div class="page-heading">
    <h1>{title}</h1>
    <p>{subtitle}</p>
</div>
""", unsafe_allow_html=True)