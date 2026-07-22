import streamlit as st

PAGE_BG = "#0d1117"
CARD_BG = "#161b27"


def apply_eda_styles():
    st.markdown(f"""
<style>
    [data-testid="stSidebar"]        {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    [data-testid="stToolbar"]        {{ display: none !important; }}
    #MainMenu                         {{ display: none !important; }}
    footer                            {{ display: none !important; }}

    html, body, .stApp {{
        background: {PAGE_BG} !important;
    }}

    .block-container {{
        max-width:     100% !important;
        padding-left:  2rem !important;
        padding-right: 2rem !important;
        padding-top:   0 !important;
        background:    {PAGE_BG} !important;
    }}

    .eda-section-title {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: rgba(255,255,255,0.3);
        margin: 0 0 12px 0;
    }}

    .eda-divider {{
        height: 1px;
        background: rgba(255,255,255,0.06);
        margin: 20px 0;
    }}

    /* summary strip cards */
    .eda-strip {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 12px;
        margin-bottom: 4px;
    }}

    .eda-strip-card {{
        background: {CARD_BG};
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.07);
        padding: 16px 18px;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }}

    .eda-strip-label {{
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: rgba(255,255,255,0.32);
        margin: 0;
    }}

    .eda-strip-value {{
        font-size: 24px;
        font-weight: 800;
        line-height: 1;
        margin: 0;
    }}

    .eda-strip-sub {{
        font-size: 11px;
        color: rgba(255,255,255,0.28);
        margin: 0;
    }}

    .eda-strip-bar {{
        margin-top: 8px;
        background: rgba(255,255,255,0.07);
        border-radius: 3px;
        height: 3px;
        overflow: hidden;
    }}

    .eda-strip-fill {{
        height: 100%;
        border-radius: 3px;
    }}

    /* breakdown card */
    .eda-bcard {{
        background: {CARD_BG};
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.07);
        padding: 18px 20px;
        height: 100%;
    }}

    .eda-bcard-title {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: rgba(255,255,255,0.35);
        margin: 0 0 16px 0;
    }}

    .eda-brow {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 13px;
    }}

    .eda-brow:last-child {{ margin-bottom: 0; }}

    .eda-brow-label {{
        font-size: 12px;
        color: rgba(255,255,255,0.6);
        width: 130px;
        flex-shrink: 0;
    }}

    .eda-brow-bar {{
        flex: 1;
        background: rgba(255,255,255,0.07);
        border-radius: 3px;
        height: 6px;
        overflow: hidden;
    }}

    .eda-brow-fill {{
        height: 100%;
        border-radius: 3px;
    }}

    .eda-brow-val {{
        font-size: 13px;
        font-weight: 800;
        width: 42px;
        text-align: right;
        flex-shrink: 0;
    }}

    /* payment tiles */
    .eda-pay-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 12px;
    }}

    .eda-pay-tile {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 14px 16px;
    }}

    .eda-pay-name {{
        font-size: 11px;
        color: rgba(255,255,255,0.4);
        margin: 0 0 6px 0;
        line-height: 1.4;
    }}

    .eda-pay-rate {{
        font-size: 26px;
        font-weight: 800;
        line-height: 1;
        margin: 0 0 3px 0;
    }}

    .eda-pay-count {{
        font-size: 10px;
        color: rgba(255,255,255,0.25);
        margin: 0;
    }}

    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)