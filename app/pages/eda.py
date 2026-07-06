import sys
import os
import pandas as pd
import plotly.express as px
import streamlit as st

# path setup
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)

from config import DATASET_DETAIL
from theme import apply_theme, TEXT_MUTED, PRIMARY, ACCENT, CHURN_COLOR, RETAINED_COLOR
from footer import show_footer
from data_loader import load_data
from calculation.eda_cal import get_eda_stats


# shared chart styling
CHURN_COLORS = {"Yes": CHURN_COLOR, "No": RETAINED_COLOR}

def style_fig(fig, show_legend=True):
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=show_legend)
    return fig


# churn distribution: pie and count bar
def render_churn_distribution(stats: dict):
    st.markdown("### Churn Distribution")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            stats["churn_counts"], names="Churn", values="Count", color="Churn",
            color_discrete_map=CHURN_COLORS, title="Churn vs Retained", hole=0.4,
        )
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col2:
        fig = px.bar(
            stats["churn_counts"], x="Churn", y="Count", color="Churn",
            color_discrete_map=CHURN_COLORS, title="Churn Count", text="Count",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(style_fig(fig, show_legend=False), use_container_width=True)


# tenure: histogram by churn and grouped bar
def render_tenure(stats: dict):
    st.markdown("### Tenure Distribution")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            stats["df"], x="tenure", color="Churn", color_discrete_map=CHURN_COLORS,
            nbins=30, title="Tenure Distribution by Churn", barmode="overlay", opacity=0.7,
        )
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col2:
        fig = px.bar(
            stats["tenure_dist"], x="Tenure Group", y="Count",
            title="Customers by Tenure Group", color="Count",
            color_continuous_scale=[[0, RETAINED_COLOR], [1, PRIMARY]], text="Count",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(style_fig(fig, show_legend=False), use_container_width=True)


# monthly charges: box plot and histogram
def render_monthly_charges(stats: dict):
    st.markdown("### Monthly Charges Analysis")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(
            stats["df"], x="Churn", y="MonthlyCharges", color="Churn",
            color_discrete_map=CHURN_COLORS, title="Monthly Charges by Churn",
        )
        st.plotly_chart(style_fig(fig, show_legend=False), use_container_width=True)

    with col2:
        fig = px.histogram(
            stats["df"], x="MonthlyCharges", color="Churn", color_discrete_map=CHURN_COLORS,
            nbins=30, title="Monthly Charges Distribution", barmode="overlay", opacity=0.7,
        )
        st.plotly_chart(style_fig(fig), use_container_width=True)


# churn rate by gender, senior citizen, and partner
def render_demographics(stats: dict):
    st.markdown("### Demographics vs Churn")
    col1, col2, col3 = st.columns(3)

    charts = [
        (col1, stats["gender_churn"],  "gender",        "Churn Rate by Gender",         [PRIMARY, ACCENT]),
        (col2, stats["senior_churn"],  "SeniorCitizen", "Churn Rate by Senior Citizen", [RETAINED_COLOR, CHURN_COLOR]),
        (col3, stats["partner_churn"], "Partner",       "Churn Rate by Partner",        [PRIMARY, ACCENT]),
    ]

    for col, data, x, title, colors in charts:
        with col:
            fig = px.bar(
                data, x=x, y="ChurnRate", color=x, title=title,
                text="ChurnRate", color_discrete_sequence=colors,
            )
            fig.update_traces(texttemplate="%{text}%", textposition="outside")
            st.plotly_chart(style_fig(fig, show_legend=False), use_container_width=True)


# churn rate by contract type and internet service
def render_contract_internet(stats: dict):
    st.markdown("### Contract & Internet Service vs Churn")
    col1, col2 = st.columns(2)

    charts = [
        (col1, stats["contract_churn"], "Contract",        "Churn Rate by Contract Type"),
        (col2, stats["internet_churn"], "InternetService", "Churn Rate by Internet Service"),
    ]

    for col, data, x, title in charts:
        with col:
            fig = px.bar(
                data, x=x, y="ChurnRate", color="ChurnRate", title=title, text="ChurnRate",
                color_continuous_scale=[[0, RETAINED_COLOR], [1, CHURN_COLOR]],
            )
            fig.update_traces(texttemplate="%{text}%", textposition="outside")
            st.plotly_chart(style_fig(fig, show_legend=False), use_container_width=True)


# churn rate by payment method
def render_payment_method(stats: dict):
    st.markdown("### Payment Method vs Churn")
    fig = px.bar(
        stats["payment_churn"], x="PaymentMethod", y="ChurnRate", color="ChurnRate",
        title="Churn Rate by Payment Method", text="ChurnRate",
        color_continuous_scale=[[0, RETAINED_COLOR], [1, CHURN_COLOR]],
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(style_fig(fig, show_legend=False), use_container_width=True)


# first 20 rows of the dataset
def render_raw_data(stats: dict):
    st.markdown("### Raw Data Preview")
    st.dataframe(stats["df"].head(20), use_container_width=True)


# redirect to login if not logged in
if not st.session_state.get("logged_in"):
    st.switch_page("main.py")

apply_theme()

# back to home
st.page_link("pages/home.py", label="← Back to Home")

# header
st.title("Exploratory Data Analysis")
st.markdown(
    f"<p style='color:{TEXT_MUTED}; margin-top:-15px;'>{DATASET_DETAIL}</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# load data and compute stats
df    = load_data()
stats = get_eda_stats(df)

# page sections
render_churn_distribution(stats)
st.markdown("---")
render_tenure(stats)
st.markdown("---")
render_monthly_charges(stats)
st.markdown("---")
render_demographics(stats)
st.markdown("---")
render_contract_internet(stats)
st.markdown("---")
render_payment_method(stats)
st.markdown("---")
render_raw_data(stats)

show_footer()