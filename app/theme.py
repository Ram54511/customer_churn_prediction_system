# Theme Colors
PRIMARY    = "#1f77b4"   # Blue       — main color, buttons, headers
SECONDARY  = "#ffffff"   # White      — backgrounds, cards
ACCENT     = "#ff7f0e"   # Orange     — churn alerts, highlights
BACKGROUND = "#f8f9fa"   # Light grey — page background
TEXT       = "#212529"   # Dark       — body text

# Text Colors
TEXT_HEADING = "#1f77b4"   # Blue       — page/section headings
TEXT_BODY    = "#212529"   # Dark       — general body text
TEXT_MUTED   = "#6c757d"   # Grey       — subtitles, descriptions
TEXT_CAPTION = "#adb5bd"   # Light grey — captions, footnotes

# Semantic Colors
CHURN_COLOR    = "#e74c3c"   # Red   — churned / high risk
RETAINED_COLOR = "#2ecc71"   # Green — retained / low risk

# CSS Injection
def apply_theme():
    import streamlit as st
    st.markdown(f"""
        <style>
            /* Page background */
            .stApp {{
                background-color: {BACKGROUND};
                color: {TEXT_BODY};
            }}
 
            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: {PRIMARY};
            }}
            [data-testid="stSidebar"] * {{
                color: {SECONDARY} !important;
            }}
 
            /* Primary buttons */
            .stButton > button {{
                background-color: {PRIMARY};
                color: {SECONDARY};
                border: none;
                border-radius: 6px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
                transition: all 0.2s ease;
            }}
            .stButton > button:hover {{
                background-color: {ACCENT};
                color: {SECONDARY};
                box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }}
 
            /* Headings */
            h1, h2, h3 {{
                color: {TEXT_HEADING};
            }}
 
            /* Body text */
            p, li {{
                color: {TEXT_BODY};
            }}
 
            /* Metric cards */
            [data-testid="stMetric"] {{
                background-color: {SECONDARY};
                border-left: 4px solid {PRIMARY};
                padding: 12px;
                border-radius: 6px;
            }}
        </style>
    """, unsafe_allow_html=True)