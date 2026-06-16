import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Path setup
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)
from config import DATASET_PATH, DATASET_DETAIL
from theme import apply_theme, TEXT_MUTED, PRIMARY, ACCENT, CHURN_COLOR, RETAINED_COLOR
from footer import show_footer
from calculation.eda_cal import get_eda_stats


#Guard
if not st.session_state.get("logged_in"):
    st.switch_page("login.py")

# Apply theme
apply_theme()



# Load data
df    = pd.read_csv(DATASET_PATH)
stats = get_eda_stats(df)



# Sidebar 
with st.sidebar:
    st.markdown(
        f"<h4 style='color:white;'>{st.session_state.get('username', 'admin')}</h4>",
        unsafe_allow_html=True,
    )

    for _ in range(40):
        st.write("")
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("login.py")

# Header
st.title("Exploratory Data Analysis")
st.markdown(
    f"<p style='color:{TEXT_MUTED}; margin-top:-15px;'>{DATASET_DETAIL}</p>",
    unsafe_allow_html=True,
)
st.markdown("---")



# Churn Distribution 
st.markdown("### Churn Distribution")
col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
        stats["churn_counts"],
        names="Churn",
        values="Count",
        color="Churn",
        color_discrete_map={"Yes": CHURN_COLOR, "No": RETAINED_COLOR},
        title="Churn vs Retained",
        hole=0.4,
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        stats["churn_counts"],
        x="Churn",
        y="Count",
        color="Churn",
        color_discrete_map={"Yes": CHURN_COLOR, "No": RETAINED_COLOR},
        title="Churn Count",
        text="Count",
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")



# Section 2: Tenure Distribution
st.markdown("### Tenure Distribution")
col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        stats["df"],
        x="tenure",
        color="Churn",
        color_discrete_map={"Yes": CHURN_COLOR, "No": RETAINED_COLOR},
        nbins=30,
        title="Tenure Distribution by Churn",
        barmode="overlay",
        opacity=0.7,
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        stats["tenure_dist"],
        x="Tenure Group",
        y="Count",
        title="Customers by Tenure Group",
        color="Count",
        color_continuous_scale=[[0, RETAINED_COLOR], [1, PRIMARY]],
        text="Count",
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")



# Monthly Charges
st.markdown("### Monthly Charges Analysis")
col1, col2 = st.columns(2)

with col1:
    fig = px.box(
        stats["df"],
        x="Churn",
        y="MonthlyCharges",
        color="Churn",
        color_discrete_map={"Yes": CHURN_COLOR, "No": RETAINED_COLOR},
        title="Monthly Charges by Churn",
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(
        stats["df"],
        x="MonthlyCharges",
        color="Churn",
        color_discrete_map={"Yes": CHURN_COLOR, "No": RETAINED_COLOR},
        nbins=30,
        title="Monthly Charges Distribution",
        barmode="overlay",
        opacity=0.7,
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")



# Demographics
st.markdown("### Demographics vs Churn")
col1, col2, col3 = st.columns(3)

with col1:
    fig = px.bar(
        stats["gender_churn"],
        x="gender",
        y="ChurnRate",
        color="gender",
        title="Churn Rate by Gender",
        text="ChurnRate",
        color_discrete_sequence=[PRIMARY, ACCENT],
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        stats["senior_churn"],
        x="SeniorCitizen",
        y="ChurnRate",
        color="SeniorCitizen",
        title="Churn Rate by Senior Citizen",
        text="ChurnRate",
        color_discrete_sequence=[RETAINED_COLOR, CHURN_COLOR],
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = px.bar(
        stats["partner_churn"],
        x="Partner",
        y="ChurnRate",
        color="Partner",
        title="Churn Rate by Partner",
        text="ChurnRate",
        color_discrete_sequence=[PRIMARY, ACCENT],
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")



# Contract & Internet
st.markdown("### Contract & Internet Service vs Churn")
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        stats["contract_churn"],
        x="Contract",
        y="ChurnRate",
        color="ChurnRate",
        title="Churn Rate by Contract Type",
        text="ChurnRate",
        color_continuous_scale=[[0, RETAINED_COLOR], [1, CHURN_COLOR]],
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        stats["internet_churn"],
        x="InternetService",
        y="ChurnRate",
        color="ChurnRate",
        title="Churn Rate by Internet Service",
        text="ChurnRate",
        color_continuous_scale=[[0, RETAINED_COLOR], [1, CHURN_COLOR]],
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")


# Payment Method 
st.markdown("### Payment Method vs Churn")
fig = px.bar(
    stats["payment_churn"],
    x="PaymentMethod",
    y="ChurnRate",
    color="ChurnRate",
    title="Churn Rate by Payment Method",
    text="ChurnRate",
    color_continuous_scale=[[0, RETAINED_COLOR], [1, CHURN_COLOR]],
)
fig.update_traces(texttemplate="%{text}%", textposition="outside")
fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")


# Raw Data
st.markdown("### Raw Data Preview")
st.dataframe(stats["df"].head(20), use_container_width=True)


# Footer 
show_footer()