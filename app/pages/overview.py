import sys
import os
import streamlit as st
import pandas as pd
sys.path.insert(0, os.path.join(os.getcwd(), "app"))
from styles.overview import apply_overview_styles
from footer import show_footer
from config import DATASET_DETAIL, DATASET_PATH
from calculation.overview_cal import get_overview_stats
from theme import CHURN_COLOR, RETAINED_COLOR, PRIMARY
from session import apply_session


# Guard
apply_session()


# Styles & data
apply_overview_styles()
df    = pd.read_csv(DATASET_PATH)
stats = get_overview_stats(df)


#  Back button
st.page_link("pages/home.py", label="← Back to Home")

#  Hero 
st.markdown(f"""
    <div class='hero' style=align-items:center;>
        <h1>Project Overview</h1>
    </div>
""", unsafe_allow_html=True)



# About
st.markdown("<div class='sec-head'><span></span>About the Project</div>", unsafe_allow_html=True)
st.markdown("""
    <div class='about-card'>
    Customer churn — the rate at which customers discontinue their relationship with a business —
    represents one of the most costly challenges facing modern organisations. This project builds a
    proactive, data-driven pipeline to identify at-risk customers <b>before they churn</b>, enabling
    targeted retention strategies using machine learning models trained on real telecom data.
    </div>
""", unsafe_allow_html=True)
st.markdown("<div class='sec-divider'></div>", unsafe_allow_html=True)



# Dataset Summary
st.markdown("<div class='sec-head'><span></span>Dataset Summary</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Customers",    f"{stats['total_customers']:,}")
with col2:
    st.metric("Total Features",     str(stats['total_features']))
with col3:
    st.metric("Churned",  f"{stats['churned']:,}", delta=f"-{stats['churn_rate']}%", delta_color="inverse")
with col4:
    st.metric("Retained", f"{stats['retained']:,}", delta=f"+{stats['retention_rate']}%")

st.markdown("<br>", unsafe_allow_html=True)



# Financial & Tenure
st.markdown("<div class='sec-head'><span></span>Financial & Tenure Insights</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Avg Monthly Charges", f"${stats['avg_monthly']}")
with col2:
    st.metric("Avg Total Charges",   f"${stats['avg_total']:,.2f}")
with col3:
    st.metric("Avg Tenure",          f"{stats['avg_tenure']} months")
with col4:
    st.metric("Max Tenure",          f"{stats['max_tenure']} months")

st.markdown("<div class='sec-divider'></div>", unsafe_allow_html=True)



# Demographics
st.markdown("<div class='sec-head'><span></span>Customer Demographics</div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Male Customers",   f"{stats['male_count']:,}")
with col2:
    st.metric("Female Customers", f"{stats['female_count']:,}")
with col3:
    st.metric("Senior Citizens",  f"{stats['senior_count']:,}", delta=f"{stats['senior_pct']}% of total")
with col4:
    st.metric("Has Dependents",   f"{stats['dependents_count']:,}")

st.markdown("<div class='sec-divider'></div>", unsafe_allow_html=True)



# Churn Breakdown
st.markdown("<div class='sec-head'><span></span>Churn Breakdown</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("<p style='font-weight:600; color:#0f2742; margin-bottom:10px;'>By Contract Type</p>", unsafe_allow_html=True)
    for _, row in stats["contract_stats"].iterrows():
        color = CHURN_COLOR if row["ChurnRate"] > 20 else RETAINED_COLOR
        st.markdown(f"""
            <div class='churn-row' style='border-left:4px solid {color};'>
                <div>
                    <b style='color:#0f2742;'>{row['Contract']}</b>
                    <span style='color:#adb5bd; font-size:12px; margin-left:6px;'>{row['Count']:,} customers</span>
                </div>
                <span style='color:{color}; font-weight:700; font-size:15px;'>{row['ChurnRate']}%</span>
            </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("<p style='font-weight:600; color:#0f2742; margin-bottom:10px;'>By Internet Service</p>", unsafe_allow_html=True)
    for _, row in stats["internet_stats"].iterrows():
        color = CHURN_COLOR if row["ChurnRate"] > 20 else RETAINED_COLOR
        st.markdown(f"""
            <div class='churn-row' style='border-left:4px solid {color};'>
                <div>
                    <b style='color:#0f2742;'>{row['InternetService']}</b>
                    <span style='color:#adb5bd; font-size:12px; margin-left:6px;'>{row['Count']:,} customers</span>
                </div>
                <span style='color:{color}; font-weight:700; font-size:15px;'>{row['ChurnRate']}%</span>
            </div>""", unsafe_allow_html=True)

st.markdown("<div class='sec-divider'></div>", unsafe_allow_html=True)



# Research Questions
st.markdown("<div class='sec-head'><span></span>Research Questions</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
rqs = [
    ("RQ1", "Which customer attributes are the strongest predictors of churn?"),
    ("RQ2", "How do ML models compare in accuracy, precision, and interpretability?"),
    ("RQ3", "How can churn models be translated into actionable retention strategies?"),
    ("RQ4", "What role does data visualisation play in communicating insights to stakeholders?"),
]
for i, (label, text) in enumerate(rqs):
    col = col1 if i % 2 == 0 else col2
    with col:
        st.markdown(f"""
            <div class='rq-card'>
                <b>{label}</b> — {text}
            </div>""", unsafe_allow_html=True)

st.markdown("<div class='sec-divider'></div>", unsafe_allow_html=True)


#Footer
show_footer()