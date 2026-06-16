import sys
import os
import streamlit as st
sys.path.insert(0, os.path.join(os.getcwd(), "app"))
from styles.home import apply_home_styles
from footer import show_footer
from session import apply_session

# Apply session management
apply_session()

# Apply styles 
apply_home_styles()

#  Header banner with logout
username = st.session_state.get("username", "admin")
st.markdown(f"""
    <div class='home-header'>
        <div style='text-align:right; margin-bottom:8px;'>
            <span style='font-size:13px; color:rgba(255,255,255,0.7);'>
                Hello, {username}
            </span>
        </div>
        <h1>Customer Churn Prediction</h1>
    </div>
""", unsafe_allow_html=True)


# Logout button below header
_, _, logout_col = st.columns([6, 2, 1])
with logout_col:
    if st.button("⏻ Logout", use_container_width=True):
        st.session_state.clear()
        st.query_params.clear()
        st.switch_page("login.py")

st.markdown("<br>", unsafe_allow_html=True)



# Cards Row 1
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class='nav-card card-overview'>
            <p class='card-title'>Overview</p>
            <p class='card-desc'>Dataset summary, churn rate,
            and key customer statistics from IBM Telco.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='link-overview'>", unsafe_allow_html=True)
    st.page_link("pages/overview.py", label="→  Go to Overview")
    st.markdown("</div>", unsafe_allow_html=True)


with col2:
    st.markdown("""
        <div class='nav-card card-eda'>
            <p class='card-title'>EDA</p>
            <p class='card-desc'>Distributions, correlation matrix,
            and customer segmentation analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='link-eda'>", unsafe_allow_html=True)
    st.page_link("pages/eda.py", label="→  Go to EDA")
    st.markdown("</div>", unsafe_allow_html=True)


with col3:
    st.markdown("""
        <div class='nav-card card-model'>
            <p class='card-title'>Model Results</p>
            <p class='card-desc'>Compare Logistic Regression,
            Random Forest, and XGBoost performance.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='link-model'>", unsafe_allow_html=True)
    st.page_link("pages/model.py", label="→  Go to Model Results")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)



# Cards Row 2
col4, col5 = st.columns(2)
with col4:
    st.markdown("""
        <div class='nav-card card-shap'>
            <p class='card-title'>SHAP Analysis</p>
            <p class='card-desc'>Feature importance and key churn
            drivers explained with interpretable AI.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='link-shap'>", unsafe_allow_html=True)
    st.page_link("pages/shap.py", label="→  Go to SHAP Analysis")
    st.markdown("</div>", unsafe_allow_html=True)



with col5:
    st.markdown("""
        <div class='nav-card card-predict'>
            <p class='card-title'>Live Predict</p>
            <p class='card-desc'>Enter customer details and get
            a real-time churn prediction from 3 models.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='link-predict'>", unsafe_allow_html=True)
    st.page_link("pages/predict.py", label="→  Go to Live Predict")
    st.markdown("</div>", unsafe_allow_html=True)



#  Footer
show_footer()