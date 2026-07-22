import streamlit as st

PAGE_BG        = "#0d1117"
CARD_BG        = "#161b27"
TEAL           = "#00d4c8"
CHURN_COLOR    = "#E24B4A"
RETAINED_COLOR = "#1D9E75"
BLUE           = "#4f8ef7"
PURPLE         = "#a78bfa"
AMBER          = "#f59e0b"


def apply_predict_styles():
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

    .pr-section {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: rgba(255,255,255,0.3);
        margin: 0 0 12px 0;
    }}

    .pr-divider {{
        height: 1px;
        background: rgba(255,255,255,0.06);
        margin: 20px 0;
    }}

    /* form column headings */
    .pr-col-title {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: rgba(255,255,255,0.35);
        margin: 0 0 14px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }}

    /* verdict banner */
    .pr-verdict {{
        border-radius: 16px;
        padding: 28px 24px;
        text-align: center;
        margin-bottom: 4px;
    }}

    .pr-verdict-title {{
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: rgba(255,255,255,0.7);
        margin: 0 0 8px 0;
    }}

    .pr-verdict-value {{
        font-size: 56px;
        font-weight: 800;
        color: white;
        line-height: 1;
        margin: 0 0 8px 0;
    }}

    .pr-verdict-detail {{
        font-size: 13px;
        color: rgba(255,255,255,0.55);
        margin: 0;
    }}

    /* model cards */
    .pr-model-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
    }}

    .pr-model-card {{
        background: {CARD_BG};
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.07);
        padding: 18px 18px;
        text-align: center;
    }}

    .pr-model-name {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: rgba(255,255,255,0.38);
        margin: 0 0 10px 0;
    }}

    .pr-model-prob {{
        font-size: 36px;
        font-weight: 800;
        line-height: 1;
        margin: 0 0 6px 0;
    }}

    .pr-model-verdict {{
        font-size: 12px;
        font-weight: 700;
        margin: 0 0 4px 0;
    }}

    .pr-model-threshold {{
        font-size: 11px;
        color: rgba(255,255,255,0.28);
        margin: 0 0 12px 0;
    }}

    .pr-model-bar {{
        background: rgba(255,255,255,0.07);
        border-radius: 3px;
        height: 4px;
        overflow: hidden;
    }}

    .pr-model-fill {{
        height: 100%;
        border-radius: 3px;
    }}

    /* suggestion cards */
    .pr-suggestion {{
        background: {CARD_BG};
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.07);
        border-left: 3px solid {TEAL};
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 13px;
        color: rgba(255,255,255,0.6);
        line-height: 1.6;
    }}

    .pr-suggestion:last-child {{ margin-bottom: 0; }}
    .pr-suggestion b {{ color: {TEAL}; }}

    /* streamlit widget dark overrides */
    .stSelectbox label,
    .stSlider label,
    .stNumberInput label {{
        color: rgba(255,255,255,0.5) !important;
        font-size: 12px !important;
    }}

    .stSelectbox > div > div {{
        background: {CARD_BG} !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: rgba(255,255,255,0.75) !important;
        border-radius: 8px !important;
    }}

    .stNumberInput > div > div > input {{
        background: {CARD_BG} !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: rgba(255,255,255,0.75) !important;
        border-radius: 8px !important;
    }}

    /* predict button */
    .stButton > button {{
        background: linear-gradient(135deg, {TEAL}, {BLUE}) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 14px !important;
        letter-spacing: 0.5px !important;
        transition: all 0.2s ease !important;
    }}

    .stButton > button:hover {{
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }}
</style>
""", unsafe_allow_html=True)