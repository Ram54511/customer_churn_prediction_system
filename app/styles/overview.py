import streamlit as st


def apply_overview_styles():
    st.markdown("""
<style>
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stToolbar"]        { display: none !important; }
    #MainMenu                         { display: none !important; }
    footer                            { display: none !important; }

    html, body, .stApp {
        background: #1a1033 !important;
    }

    .block-container {
        max-width:     100% !important;
        padding-left:  2rem !important;
        padding-right: 2rem !important;
        padding-top:   0 !important;
        background:    #1a1033 !important;
    }

    /* section heading */
    .ov-section-title {
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: rgba(255,255,255,0.45);
        margin: 0 0 14px 0;
    }

    /* divider */
    .ov-divider {
        height: 1px;
        background: rgba(255,255,255,0.08);
        margin: 22px 0;
    }

    /* dark card */
    .ov-card {
        background: #231845;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 20px 22px;
        height: 100%;
    }

    .ov-card-title {
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: rgba(255,255,255,0.5);
        margin: 0 0 16px 0;
    }

    /* big metric inside a card */
    .ov-big-metric {
        font-size: 42px;
        font-weight: 800;
        color: white;
        line-height: 1;
        margin: 0 0 4px 0;
    }

    .ov-metric-sub {
        font-size: 13px;
        color: rgba(255,255,255,0.45);
        margin: 0 0 16px 0;
    }

    /* small stat cards row */
    .ov-stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 14px;
    }

    .ov-stat-card {
        background: #231845;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 18px 18px 14px 18px;
    }

    .ov-stat-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: rgba(255,255,255,0.4);
        margin: 0 0 8px 0;
    }

    .ov-stat-value {
        font-size: 26px;
        font-weight: 800;
        line-height: 1;
        margin: 0 0 4px 0;
    }

    .ov-stat-caption {
        font-size: 12px;
        color: rgba(255,255,255,0.35);
        margin: 0 0 10px 0;
    }

    /* shared bar */
    .ov-bar-bg {
        background: rgba(255,255,255,0.08);
        border-radius: 2px;
        height: 4px;
        overflow: hidden;
    }

    .ov-bar-fill {
        height: 100%;
        border-radius: 2px;
    }

    /* breakdown rows */
    .ov-row {
        margin-bottom: 16px;
    }

    .ov-row:last-child {
        margin-bottom: 0;
    }

    .ov-row-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
    }

    .ov-row-label {
        font-size: 13px;
        color: rgba(255,255,255,0.75);
    }

    .ov-row-rate {
        font-size: 14px;
        font-weight: 800;
    }

    .ov-row-count {
        font-size: 11px;
        color: rgba(255,255,255,0.3);
        margin: 4px 0 0 0;
    }

    /* demographics */
    .ov-demo-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 18px;
    }

    /* financial cards */
    .ov-fin-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 14px;
    }

    .ov-fin-card {
        background: #231845;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 18px 18px 14px 18px;
    }

    .ov-fin-value {
        font-size: 22px;
        font-weight: 800;
        color: white;
        margin: 0 0 4px 0;
    }

    /* badge pills */
    .ov-badge-up {
        display: inline-block;
        background: rgba(29,158,117,0.18);
        color: #1D9E75;
        border-radius: 6px;
        padding: 3px 9px;
        font-size: 12px;
        font-weight: 700;
    }

    .ov-badge-down {
        display: inline-block;
        background: rgba(226,75,74,0.18);
        color: #E24B4A;
        border-radius: 6px;
        padding: 3px 9px;
        font-size: 12px;
        font-weight: 700;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }
</style>
    """, unsafe_allow_html=True)