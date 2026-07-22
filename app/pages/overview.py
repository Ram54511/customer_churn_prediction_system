import sys
import os
import streamlit as st

# path setup
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)

from styles.overview import apply_overview_styles
from theme import CHURN_COLOR, RETAINED_COLOR
from header import show_header
from footer import show_footer
from data_loader import load_data
from auth.guard import require_login
from calculation.overview_cal import get_overview_stats


@st.cache_data(show_spinner=False)
def get_cached_stats():
    return get_overview_stats(load_data())


# two big hero cards: churn rate + retention rate with mini area sparkline
def render_hero(stats: dict):
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown(f"""
<div class="ov-card">
    <p class="ov-card-title">Churn Rate</p>
    <p class="ov-big-metric" style="color:#E24B4A;">{stats['churn_rate']}%</p>
    <p class="ov-metric-sub">{stats['churned']:,} customers lost</p>
    <svg viewBox="0 0 300 60" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:60px;">
        <defs>
            <linearGradient id="rg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#E24B4A" stop-opacity="0.35"/>
                <stop offset="100%" stop-color="#E24B4A" stop-opacity="0"/>
            </linearGradient>
        </defs>
        <path d="M0,45 C30,40 50,55 80,35 C110,15 130,50 160,30 C190,10 210,45 240,25 C260,12 280,38 300,20 L300,60 L0,60 Z" fill="url(#rg)"/>
        <path d="M0,45 C30,40 50,55 80,35 C110,15 130,50 160,30 C190,10 210,45 240,25 C260,12 280,38 300,20" fill="none" stroke="#E24B4A" stroke-width="2"/>
    </svg>
</div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
<div class="ov-card">
    <p class="ov-card-title">Retention Rate</p>
    <p class="ov-big-metric" style="color:#1D9E75;">{stats['retention_rate']}%</p>
    <p class="ov-metric-sub">{stats['retained']:,} customers retained</p>
    <svg viewBox="0 0 300 60" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:60px;">
        <defs>
            <linearGradient id="gg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#1D9E75" stop-opacity="0.35"/>
                <stop offset="100%" stop-color="#1D9E75" stop-opacity="0"/>
            </linearGradient>
        </defs>
        <path d="M0,40 C30,35 50,45 80,25 C110,8 130,38 160,20 C190,5 210,30 240,15 C260,5 280,22 300,10 L300,60 L0,60 Z" fill="url(#gg)"/>
        <path d="M0,40 C30,35 50,45 80,25 C110,8 130,38 160,20 C190,5 210,30 240,15 C260,5 280,22 300,10" fill="none" stroke="#1D9E75" stroke-width="2"/>
    </svg>
</div>""", unsafe_allow_html=True)


# four small stat cards
def render_stat_cards(stats: dict):
    cards = [
        ("Total customers",  f"{stats['total_customers']:,}", "IBM Telco dataset",  "#a78bfa", 100),
        ("Total features",   str(stats['total_features']),    "Input variables",    "#60a5fa", 100),
        ("Avg monthly",      f"${stats['avg_monthly']}",      "per customer",       "#34d399", 100),
        ("Avg tenure",       f"{stats['avg_tenure']} mo",     "time with company",  "#f59e0b", stats['avg_tenure'] / 72 * 100),
    ]
    html = '<div class="ov-stat-grid">'
    for label, value, caption, color, pct in cards:
        html += f"""
        <div class="ov-stat-card">
            <p class="ov-stat-label">{label}</p>
            <p class="ov-stat-value" style="color:{color};">{value}</p>
            <p class="ov-stat-caption">{caption}</p>
            <div class="ov-bar-bg"><div class="ov-bar-fill" style="width:{pct}%;background:{color};"></div></div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# churn breakdown side by side
def render_churn_breakdown(stats: dict):
    col1, col2 = st.columns(2, gap="medium")

    def breakdown_card(title, rows, label_col, col):
        html = f'<div class="ov-card"><p class="ov-card-title">{title}</p>'
        for _, row in rows.iterrows():
            rate  = row["ChurnRate"]
            color = "#E24B4A" if rate > 20 else "#1D9E75"
            html += f"""
            <div class="ov-row">
                <div class="ov-row-meta">
                    <span class="ov-row-label">{row[label_col]}</span>
                    <span class="ov-row-rate" style="color:{color};">{rate}%</span>
                </div>
                <div class="ov-bar-bg"><div class="ov-bar-fill" style="width:{rate}%;background:{color};"></div></div>
                <p class="ov-row-count">{row['Count']:,} customers</p>
            </div>"""
        html += '</div>'
        with col:
            st.markdown(html, unsafe_allow_html=True)

    breakdown_card("Churn by contract",         stats["contract_stats"], "Contract",       col1)
    breakdown_card("Churn by internet service", stats["internet_stats"], "InternetService", col2)


# financial + demographics side by side
def render_financial_demo(stats: dict):
    col1, col2 = st.columns(2, gap="medium")

    # financial
    with col1:
        cards = [
            ("Avg monthly charges", f"${stats['avg_monthly']}",     "per customer"),
            ("Avg total charges",   f"${stats['avg_total']:,.0f}",  "lifetime spend"),
            ("Max tenure",          f"{stats['max_tenure']} mo",    "longest customer"),
        ]
        html = '<div class="ov-card"><p class="ov-card-title">Financial & Tenure</p><div class="ov-fin-grid">'
        for label, value, caption in cards:
            html += f"""
            <div class="ov-fin-card">
                <p class="ov-stat-label">{label}</p>
                <p class="ov-fin-value">{value}</p>
                <p class="ov-stat-caption">{caption}</p>
            </div>"""
        html += '</div></div>'
        st.markdown(html, unsafe_allow_html=True)

    # demographics
    with col2:
        total = stats['total_customers']
        items = [
            ("Male",            stats['male_count'],       "#60a5fa"),
            ("Female",          stats['female_count'],     "#a78bfa"),
            ("Senior citizens", stats['senior_count'],     "#f59e0b"),
            ("Has dependents",  stats['dependents_count'], "#34d399"),
        ]
        html = '<div class="ov-card"><p class="ov-card-title">Demographics</p><div class="ov-demo-grid">'
        for label, count, color in items:
            pct = round(count / total * 100, 1)
            html += f"""
            <div>
                <div class="ov-row-meta">
                    <span class="ov-row-label">{label}</span>
                    <span class="ov-row-rate" style="color:{color};">{count:,}</span>
                </div>
                <div class="ov-bar-bg"><div class="ov-bar-fill" style="width:{pct}%;background:{color};"></div></div>
                <p class="ov-row-count">{pct}%</p>
            </div>"""
        html += '</div></div>'
        st.markdown(html, unsafe_allow_html=True)


# guard and render
require_login()
apply_overview_styles()
show_header(back=True)

stats = get_cached_stats()

st.markdown("<p class='ov-section-title'>Summary</p>", unsafe_allow_html=True)
render_hero(stats)
st.markdown("<div class='ov-divider'></div>", unsafe_allow_html=True)
render_stat_cards(stats)
st.markdown("<div class='ov-divider'></div>", unsafe_allow_html=True)
render_churn_breakdown(stats)
st.markdown("<div class='ov-divider'></div>", unsafe_allow_html=True)
render_financial_demo(stats)
st.markdown("<br>", unsafe_allow_html=True)

show_footer()