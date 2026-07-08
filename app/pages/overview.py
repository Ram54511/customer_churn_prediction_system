import sys
import os
import streamlit as st

# path setup
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)

from styles.overview import apply_overview_styles
from config import DATASET_DETAIL
from theme import CHURN_COLOR, RETAINED_COLOR
from header import show_header
from footer import show_footer
from data_loader import load_data
from auth.guard import require_login
from calculation.overview_cal import get_overview_stats


# section heading helper
def section_head(title: str):
    st.markdown(f"<div class='sec-head'><span></span>{title}</div>", unsafe_allow_html=True)


def section_divider():
    st.markdown("<div class='sec-divider'></div>", unsafe_allow_html=True)


# project description card
def render_about():
    section_head("About the Project")
    st.markdown("""
        <div class='about-card'>
        Customer churn — the rate at which customers discontinue their relationship with a business —
        represents one of the most costly challenges facing modern organisations. This project builds a
        proactive, data-driven pipeline to identify at-risk customers <b>before they churn</b>, enabling
        targeted retention strategies using machine learning models trained on real telecom data.
        </div>
    """, unsafe_allow_html=True)


# headline dataset metrics
def render_dataset_summary(stats: dict):
    section_head("Dataset Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{stats['total_customers']:,}")
    col2.metric("Total Features",  str(stats['total_features']))
    col3.metric("Churned",  f"{stats['churned']:,}",
                delta=f"-{stats['churn_rate']}%", delta_color="inverse")
    col4.metric("Retained", f"{stats['retained']:,}",
                delta=f"+{stats['retention_rate']}%")


# financial and tenure metrics
def render_financial_tenure(stats: dict):
    section_head("Financial & Tenure Insights")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Monthly Charges", f"${stats['avg_monthly']}")
    col2.metric("Avg Total Charges",   f"${stats['avg_total']:,.2f}")
    col3.metric("Avg Tenure",          f"{stats['avg_tenure']} months")
    col4.metric("Max Tenure",          f"{stats['max_tenure']} months")


# demographic metrics
def render_demographics(stats: dict):
    section_head("Customer Demographics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Male Customers",   f"{stats['male_count']:,}")
    col2.metric("Female Customers", f"{stats['female_count']:,}")
    col3.metric("Senior Citizens",  f"{stats['senior_count']:,}",
                delta=f"{stats['senior_pct']}% of total")
    col4.metric("Has Dependents",   f"{stats['dependents_count']:,}")


# one row in the churn breakdown list
def churn_row(label: str, count: int, rate: float):
    color = CHURN_COLOR if rate > 20 else RETAINED_COLOR
    st.markdown(f"""
        <div class='churn-row' style='border-left:4px solid {color};'>
            <div>
                <b style='color:#0f2742;'>{label}</b>
                <span style='color:#adb5bd; font-size:12px; margin-left:6px;'>{count:,} customers</span>
            </div>
            <span style='color:{color}; font-weight:700; font-size:15px;'>{rate}%</span>
        </div>""", unsafe_allow_html=True)


# churn rate by contract type and internet service
def render_churn_breakdown(stats: dict):
    section_head("Churn Breakdown")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<p style='font-weight:600; color:#0f2742; margin-bottom:10px;'>By Contract Type</p>",
                    unsafe_allow_html=True)
        for _, row in stats["contract_stats"].iterrows():
            churn_row(row["Contract"], row["Count"], row["ChurnRate"])

    with col2:
        st.markdown("<p style='font-weight:600; color:#0f2742; margin-bottom:10px;'>By Internet Service</p>",
                    unsafe_allow_html=True)
        for _, row in stats["internet_stats"].iterrows():
            churn_row(row["InternetService"], row["Count"], row["ChurnRate"])


# dissertation research questions
def render_research_questions():
    section_head("Research Questions")
    col1, col2 = st.columns(2)
    rqs = [
        ("RQ1", "Which customer attributes are the strongest predictors of churn?"),
        ("RQ2", "How do ML models compare in accuracy, precision, and interpretability?"),
        ("RQ3", "How can churn models be translated into actionable retention strategies?"),
        ("RQ4", "What role does data visualisation play in communicating insights to stakeholders?"),
    ]
    for i, (label, text) in enumerate(rqs):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
                <div class='rq-card'>
                    <b>{label}</b> — {text}
                </div>""", unsafe_allow_html=True)


# login guard: restores session from the signed url token
require_login()

apply_overview_styles()

# header bar (handles logout)
show_header("Exploratory Data Analysis", DATASET_DETAIL, back=True)

# load data and compute stats
stats = get_overview_stats(load_data())

# page sections
render_about()
section_divider()
render_dataset_summary(stats)
st.markdown("<br>", unsafe_allow_html=True)
render_financial_tenure(stats)
section_divider()
render_demographics(stats)
section_divider()
render_churn_breakdown(stats)
section_divider()
render_research_questions()
section_divider()

show_footer()