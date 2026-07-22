import streamlit as st

PAGE_BG = "#0d1117"
CARD_BG = "#161b27"
TEAL    = "#00d4c8"
CHURN_COLOR    = "#E24B4A"
RETAINED_COLOR = "#1D9E75"


def apply_shap_styles():
    st.markdown(f"""
<style>
    [data-testid="stSidebar"]        {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    [data-testid="stToolbar"]        {{ display: none !important; }}
    #MainMenu                         {{ display: none !important; }}
    footer                            {{ display: none !important; }}

    html, body, .stApp {{ background: {PAGE_BG} !important; }}

    .block-container {{
        max-width:     100% !important;
        padding-left:  2rem !important;
        padding-right: 2rem !important;
        padding-top:   0 !important;
        background:    {PAGE_BG} !important;
    }}

    .sh-section {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: rgba(255,255,255,0.3);
        margin: 0 0 12px 0;
    }}

    .sh-divider {{
        height: 1px;
        background: rgba(255,255,255,0.06);
        margin: 20px 0;
    }}

    .sh-intro {{
        background: {CARD_BG};
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.07);
        border-left: 3px solid {TEAL};
        padding: 18px 22px;
    }}

    .sh-intro p {{
        font-size: 13px;
        color: rgba(255,255,255,0.55);
        line-height: 1.8;
        margin: 0;
    }}

    .sh-intro b {{ color: {TEAL}; }}

    .sh-driver-grid {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 12px;
    }}

    .sh-driver-card {{
        background: {CARD_BG};
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.07);
        padding: 16px 14px;
        text-align: center;
    }}

    .sh-driver-rank {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: rgba(255,255,255,0.28);
        margin: 0 0 8px 0;
    }}

    .sh-driver-name {{
        font-size: 12px;
        font-weight: 700;
        color: rgba(255,255,255,0.8);
        margin: 0 0 8px 0;
        line-height: 1.4;
    }}

    .sh-driver-val {{
        font-size: 18px;
        font-weight: 800;
        margin: 0;
        line-height: 1;
    }}

    .sh-driver-bar {{
        margin-top: 10px;
        background: rgba(255,255,255,0.07);
        border-radius: 3px;
        height: 3px;
        overflow: hidden;
    }}

    .sh-driver-fill {{
        height: 100%;
        border-radius: 3px;
    }}

    .sh-insight-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
    }}

    .sh-insight-card {{
        background: {CARD_BG};
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.07);
        padding: 20px 22px;
    }}

    .sh-insight-title {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 0 0 14px 0;
    }}

    .sh-insight-item {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }}

    .sh-insight-item:last-child {{ margin-bottom: 0; }}

    .sh-insight-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }}

    .sh-insight-text {{
        font-size: 13px;
        color: rgba(255,255,255,0.6);
        margin: 0;
    }}

    .stSlider label {{
        color: rgba(255,255,255,0.5) !important;
        font-size: 12px !important;
    }}
</style>
""", unsafe_allow_html=True)