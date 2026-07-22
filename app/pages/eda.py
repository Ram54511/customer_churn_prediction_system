import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# path setup
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)

from styles.eda import apply_eda_styles, CARD_BG, PAGE_BG
from header import show_header
from footer import show_footer
from data_loader import load_data
from auth.guard import require_login
from calculation.eda_cal import get_eda_stats


# colours
CHURN_COLOR    = "#E24B4A"
RETAINED_COLOR = "#1D9E75"
TEAL           = "#00d4c8"
BLUE           = "#4f8ef7"
PURPLE         = "#a78bfa"
AMBER          = "#f59e0b"
CHURN_COLORS   = {"Yes": CHURN_COLOR, "No": RETAINED_COLOR}


@st.cache_data(show_spinner=False)
def get_cached_stats():
    return get_eda_stats(load_data())


# shared dark chart layout
def dark_fig(fig, show_legend=True):
    fig.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font_color="rgba(255,255,255,0.7)",
        title_font_color="rgba(255,255,255,0.38)",
        title_font_size=11,
        showlegend=show_legend,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.5)", size=11),
        ),
        margin=dict(l=8, r=8, t=32, b=8),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(255,255,255,0.07)",
            tickfont=dict(color="rgba(255,255,255,0.4)", size=10),
            title_font=dict(color="rgba(255,255,255,0.3)"),
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(255,255,255,0.07)",
            tickfont=dict(color="rgba(255,255,255,0.4)", size=10),
            title_font=dict(color="rgba(255,255,255,0.3)"),
        ),
    )
    fig.update_coloraxes(showscale=False)
    return fig


def section(title: str):
    st.markdown(f"<p class='eda-section-title'>{title}</p>", unsafe_allow_html=True)


def divider():
    st.markdown("<div class='eda-divider'></div>", unsafe_allow_html=True)


def brow(label, rate, color):
    return f"""
    <div class="eda-brow">
        <span class="eda-brow-label">{label}</span>
        <div class="eda-brow-bar">
            <div class="eda-brow-fill" style="width:{rate}%;background:{color};"></div>
        </div>
        <span class="eda-brow-val" style="color:{color};">{rate}%</span>
    </div>"""


# summary strip: 5 headline numbers
def render_summary(stats: dict):
    section("Summary")
    churned  = int(stats["churn_counts"][stats["churn_counts"]["Churn"]=="Yes"]["Count"].values[0])
    retained = int(stats["churn_counts"][stats["churn_counts"]["Churn"]=="No"]["Count"].values[0])
    total    = churned + retained
    c_pct    = round(churned / total * 100, 1)

    cards = [
        ("Total customers", f"{total:,}",   "IBM Telco",         "#4f8ef7", 100),
        ("Churned",         f"{churned:,}",  f"{c_pct}% of total","#E24B4A", c_pct),
        ("Retained",        f"{retained:,}", f"{100-c_pct}%",     "#1D9E75", 100-c_pct),
        ("Avg tenure (churned)",    "18 mo",  "months",           "#f59e0b", 18/72*100),
        ("Avg monthly (churned)",   "$74.44", "vs $61.27 retained","#a78bfa", 74.44/100*100),
    ]
    html = '<div class="eda-strip">'
    for label, value, sub, color, pct in cards:
        html += f"""
        <div class="eda-strip-card">
            <p class="eda-strip-label">{label}</p>
            <p class="eda-strip-value" style="color:{color};">{value}</p>
            <p class="eda-strip-sub">{sub}</p>
            <div class="eda-strip-bar">
                <div class="eda-strip-fill" style="width:{pct:.1f}%;background:{color};"></div>
            </div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# churn distribution: donut + histogram side by side
def render_churn_distribution(stats: dict):
    section("Churn Distribution")
    col1, col2 = st.columns([1, 1.8], gap="medium")

    with col1:
        churned  = int(stats["churn_counts"][stats["churn_counts"]["Churn"]=="Yes"]["Count"].values[0])
        retained = int(stats["churn_counts"][stats["churn_counts"]["Churn"]=="No"]["Count"].values[0])
        total    = churned + retained
        c_pct    = round(churned / total * 100, 1)

        fig = go.Figure(go.Pie(
            values=[churned, retained],
            labels=["Churned", "Retained"],
            hole=0.60,
            marker=dict(
                colors=[CHURN_COLOR, RETAINED_COLOR],
                line=dict(color=CARD_BG, width=3),
            ),
            textinfo="none",
        ))
        fig.add_annotation(
            text=f"<b>{c_pct}%</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5)'>churn</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="white", size=20), align="center",
        )
        fig.update_layout(
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)",
                        font=dict(color="rgba(255,255,255,0.5)", size=11),
                        orientation="h", y=-0.05),
            margin=dict(l=8, r=8, t=8, b=8),
            height=220,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            stats["df"], x="tenure", color="Churn",
            color_discrete_map=CHURN_COLORS,
            nbins=30, barmode="overlay", opacity=0.8,
        )
        fig.update_layout(title_text="Tenure distribution by churn status", bargap=0.05)
        st.plotly_chart(dark_fig(fig), use_container_width=True)


# monthly charges: histogram + box
def render_charges(stats: dict):
    section("Monthly Charges")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        fig = px.histogram(
            stats["df"], x="MonthlyCharges", color="Churn",
            color_discrete_map=CHURN_COLORS,
            nbins=30, barmode="overlay", opacity=0.8,
        )
        fig.update_layout(title_text="Monthly charges distribution", bargap=0.05)
        st.plotly_chart(dark_fig(fig), use_container_width=True)

    with col2:
        fig = px.box(
            stats["df"], x="Churn", y="MonthlyCharges", color="Churn",
            color_discrete_map=CHURN_COLORS,
        )
        fig.update_layout(title_text="Monthly charges by churn status")
        st.plotly_chart(dark_fig(fig, show_legend=False), use_container_width=True)


# contract + internet + tenure group
def render_service(stats: dict):
    section("Service & Contract Analysis")
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        html = '<div class="eda-bcard"><p class="eda-bcard-title">Churn by contract</p>'
        for _, row in stats["contract_churn"].iterrows():
            color = CHURN_COLOR if row["ChurnRate"] > 20 else RETAINED_COLOR
            html += brow(row["Contract"], row["ChurnRate"], color)
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with col2:
        html = '<div class="eda-bcard"><p class="eda-bcard-title">Churn by internet service</p>'
        for _, row in stats["internet_churn"].iterrows():
            color = CHURN_COLOR if row["ChurnRate"] > 20 else RETAINED_COLOR
            html += brow(row["InternetService"], row["ChurnRate"], color)
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with col3:
        fig = px.bar(
            stats["tenure_dist"], x="Tenure Group", y="Count",
            color="Count",
            color_continuous_scale=[[0, "#1c2333"], [0.5, BLUE], [1, TEAL]],
            text="Count",
        )
        fig.update_traces(
            textposition="outside",
            textfont_color="rgba(255,255,255,0.55)",
        )
        fig.update_layout(title_text="Customers by tenure group")
        st.plotly_chart(dark_fig(fig, show_legend=False), use_container_width=True)


# demographics + payment
def render_demo_payment(stats: dict):
    section("Demographics & Payment")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        g = stats["gender_churn"]
        s = stats["senior_churn"]
        p = stats["partner_churn"]

        gender_rows = (
            brow("Female", g[g['gender']=='Female']['ChurnRate'].values[0], PURPLE) +
            brow("Male",   g[g['gender']=='Male'  ]['ChurnRate'].values[0], BLUE)
        )
        senior_rows = (
            brow("Senior",     s[s['SeniorCitizen']=='Senior'    ]['ChurnRate'].values[0], CHURN_COLOR) +
            brow("Non-Senior", s[s['SeniorCitizen']=='Non-Senior']['ChurnRate'].values[0], RETAINED_COLOR)
        )
        partner_rows = (
            brow("No partner",  p[p['Partner']=='No' ]['ChurnRate'].values[0], AMBER) +
            brow("Has partner", p[p['Partner']=='Yes']['ChurnRate'].values[0], TEAL)
        )

        sub = "<p style='font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:rgba(255,255,255,0.3);margin:10px 0 8px 0;'>"

        html = (
            "<div class='eda-bcard'>"
            "<p class='eda-bcard-title'>Demographics vs churn</p>"
            f"{sub}Gender</p>"
            f"{gender_rows}"
            f"{sub}Senior Citizen</p>"
            f"{senior_rows}"
            f"{sub}Partner</p>"
            f"{partner_rows}"
            "</div>"
        )
        st.markdown(html, unsafe_allow_html=True)

    with col2:
        pay = stats["payment_churn"]
        tiles = ""
        for _, row in pay.iterrows():
            color = (CHURN_COLOR if row["ChurnRate"] > 25
                     else AMBER if row["ChurnRate"] > 18
                     else RETAINED_COLOR)
            tiles += f"""
            <div class="eda-pay-tile">
                <p class="eda-pay-name">{row['PaymentMethod']}</p>
                <p class="eda-pay-rate" style="color:{color};">{row['ChurnRate']}%</p>
                <p class="eda-pay-count">{row['Count']:,} customers</p>
            </div>"""
        st.markdown(
            f"<div class='eda-bcard'><p class='eda-bcard-title'>Churn by payment method</p>"
            f"<div class='eda-pay-grid'>{tiles}</div></div>",
            unsafe_allow_html=True,
        )


# churn rate area chart across contract + internet
def render_trend(stats: dict):
    section("Churn Rate Trends")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=stats["contract_churn"]["Contract"],
            y=stats["contract_churn"]["ChurnRate"],
            fill="tozeroy",
            fillcolor="rgba(226,75,74,0.15)",
            line=dict(color=CHURN_COLOR, width=2.5),
            mode="lines+markers",
            marker=dict(size=8, color=CHURN_COLOR,
                        line=dict(color="white", width=1.5)),
            name="Churn Rate",
        ))
        fig.update_layout(title_text="Churn rate by contract type",
                          yaxis_title="Churn %")
        st.plotly_chart(dark_fig(fig, show_legend=False), use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=stats["internet_churn"]["InternetService"],
            y=stats["internet_churn"]["ChurnRate"],
            fill="tozeroy",
            fillcolor="rgba(0,212,200,0.12)",
            line=dict(color=TEAL, width=2.5),
            mode="lines+markers",
            marker=dict(size=8, color=TEAL,
                        line=dict(color="white", width=1.5)),
            name="Churn Rate",
        ))
        fig.update_layout(title_text="Churn rate by internet service",
                          yaxis_title="Churn %")
        st.plotly_chart(dark_fig(fig, show_legend=False), use_container_width=True)


# guard and render
require_login()
apply_eda_styles()
show_header(back=True)

stats = get_cached_stats()

render_summary(stats)
divider()
render_churn_distribution(stats)
divider()
render_charges(stats)
divider()
render_service(stats)
divider()
render_demo_payment(stats)
divider()
render_trend(stats)
st.markdown("<br>", unsafe_allow_html=True)

show_footer()