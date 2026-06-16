import streamlit as st


def apply_home_styles():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

            /* ── Hide Streamlit elements ─────────────────────────── */
            [data-testid="stSidebar"]        { display: none !important; }
            [data-testid="collapsedControl"]  { display: none !important; }
            [data-testid="stToolbar"]         { display: none !important; }
            [data-testid="stDecoration"]      { display: none !important; }
            [data-testid="stStatusWidget"]    { display: none !important; }
            .stAppDeployButton                { display: none !important; }
            #MainMenu                         { display: none !important; }
            footer                            { display: none !important; }

            /* ── Global ──────────────────────────────────────────── */
            html, body, .stApp {
                font-family: 'Poppins', sans-serif;
                background-color: #f0f4f8;
            }
            .block-container {
                max-width:     100% !important;
                padding-left:  2.5rem !important;
                padding-right: 2.5rem !important;
                padding-top:   1rem !important;
            }

            /* ── Header banner ───────────────────────────────────── */
            .home-header {
                background: linear-gradient(135deg, #0f2742 0%, #1f77b4 100%);
                border-radius: 16px;
                padding: 44px 40px;
                margin-bottom: 32px;
                text-align: center;
            }
            .home-header h1 {
                font-size: 40px;
                font-weight: 700;
                color: white;
                margin: 0 0 8px 0;
                letter-spacing: -0.5px;
            }
            .home-header p {
                font-size: 15px;
                color: rgba(255,255,255,0.8);
                margin: 0 0 20px 0;
            }
            .badge {
                display: inline-block;
                background: rgba(255,255,255,0.15);
                border: 1px solid rgba(255,255,255,0.25);
                border-radius: 20px;
                padding: 5px 14px;
                font-size: 12px;
                color: white;
                margin: 3px;
            }

            /* ── Nav cards ───────────────────────────────────────── */
            .nav-card {
                background: white;
                border-radius: 16px;
                padding: 32px 28px 24px 28px;
                box-shadow: 0 2px 16px rgba(0,0,0,0.06);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                min-height: 180px;
            }
            .nav-card::after {
                content: '';
                position: absolute;
                bottom: 0; left: 0; right: 0;
                height: 4px;
                border-radius: 0 0 16px 16px;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            .nav-card:hover {
                box-shadow: 0 16px 40px rgba(0,0,0,0.12);
                transform: translateY(-5px);
            }
            .nav-card:hover::after {
                opacity: 1;
            }

            /* ── Card accent colors ──────────────────────────────── */
            .card-overview { border-top: 4px solid #1f77b4; }
            .card-eda      { border-top: 4px solid #2ecc71; }
            .card-model    { border-top: 4px solid #ff7f0e; }
            .card-shap     { border-top: 4px solid #9b59b6; }
            .card-predict  { border-top: 4px solid #e74c3c; }

            .card-overview::after { background: linear-gradient(90deg, #1f77b4, #4fa3d1); }
            .card-eda::after      { background: linear-gradient(90deg, #2ecc71, #27ae60); }
            .card-model::after    { background: linear-gradient(90deg, #ff7f0e, #e05c00); }
            .card-shap::after     { background: linear-gradient(90deg, #9b59b6, #6c3483); }
            .card-predict::after  { background: linear-gradient(90deg, #e74c3c, #c0392b); }

            .num-overview { background: rgba(31,119,180,0.1);  color: #1f77b4; }
            .num-eda      { background: rgba(46,204,113,0.1);  color: #27ae60; }
            .num-model    { background: rgba(255,127,14,0.1);  color: #ff7f0e; }
            .num-shap     { background: rgba(155,89,182,0.1);  color: #9b59b6; }
            .num-predict  { background: rgba(231,76,60,0.1);   color: #e74c3c; }

            /* ── Card text ───────────────────────────────────────── */
            .card-title {
                font-size: 20px;
                font-weight: 700;
                color: #0f2742;
                margin: 0 0 10px 0;
            }
            .card-desc {
                font-size: 13px;
                color: #6c757d;
                line-height: 1.7;
                margin: 0;
            }

            /* ── Go to button ────────────────────────────────────── */
            .stPageLink a {
                display: inline-block !important;
                width: 100% !important;
                text-align: center !important;
                padding: 11px 20px !important;
                border-radius: 10px !important;
                font-size: 14px !important;
                font-weight: 600 !important;
                text-decoration: none !important;
                letter-spacing: 0.3px !important;
                transition: all 0.25s ease !important;
                margin-top: 4px !important;
                box-sizing: border-box !important;
            }

            /* ── Overview button ─────────────────────────────────── */
            .link-overview .stPageLink a {
                background: rgba(31,119,180,0.06) !important;
                color: #1f77b4 !important;
                border: 1.5px solid #1f77b4 !important;
            }
            .link-overview .stPageLink a:hover {
                background: linear-gradient(90deg, #1f77b4, #4fa3d1) !important;
                color: white !important;
                border-color: transparent !important;
                box-shadow: 0 6px 20px rgba(31,119,180,0.35) !important;
                transform: translateY(-2px) !important;
                letter-spacing: 1px !important;
            }

            /* ── EDA button ──────────────────────────────────────── */
            .link-eda .stPageLink a {
                background: rgba(46,204,113,0.06) !important;
                color: #27ae60 !important;
                border: 1.5px solid #27ae60 !important;
            }
            .link-eda .stPageLink a:hover {
                background: linear-gradient(90deg, #2ecc71, #27ae60) !important;
                color: white !important;
                border-color: transparent !important;
                box-shadow: 0 6px 20px rgba(46,204,113,0.35) !important;
                transform: translateY(-2px) !important;
                letter-spacing: 1px !important;
            }

            /* ── Model button ────────────────────────────────────── */
            .link-model .stPageLink a {
                background: rgba(255,127,14,0.06) !important;
                color: #ff7f0e !important;
                border: 1.5px solid #ff7f0e !important;
            }
            .link-model .stPageLink a:hover {
                background: linear-gradient(90deg, #ff7f0e, #e05c00) !important;
                color: white !important;
                border-color: transparent !important;
                box-shadow: 0 6px 20px rgba(255,127,14,0.35) !important;
                transform: translateY(-2px) !important;
                letter-spacing: 1px !important;
            }

            /* ── SHAP button ─────────────────────────────────────── */
            .link-shap .stPageLink a {
                background: rgba(155,89,182,0.06) !important;
                color: #9b59b6 !important;
                border: 1.5px solid #9b59b6 !important;
            }
            .link-shap .stPageLink a:hover {
                background: linear-gradient(90deg, #9b59b6, #6c3483) !important;
                color: white !important;
                border-color: transparent !important;
                box-shadow: 0 6px 20px rgba(155,89,182,0.35) !important;
                transform: translateY(-2px) !important;
                letter-spacing: 1px !important;
            }

            /* ── Predict button ──────────────────────────────────── */
            .link-predict .stPageLink a {
                background: rgba(231,76,60,0.06) !important;
                color: #e74c3c !important;
                border: 1.5px solid #e74c3c !important;
            }
            .link-predict .stPageLink a:hover {
                background: linear-gradient(90deg, #e74c3c, #c0392b) !important;
                color: white !important;
                border-color: transparent !important;
                box-shadow: 0 6px 20px rgba(231,76,60,0.35) !important;
                transform: translateY(-2px) !important;
                letter-spacing: 1px !important;
            }

            /* ── Logout button ───────────────────────────────────── */
            .stButton > button {
                background: rgba(231,76,60,0.08) !important;
                color: #e74c3c !important;
                border: 1.5px solid #e74c3c !important;
                border-radius: 8px !important;
                font-size: 13px !important;
                font-weight: 600 !important;
                white-space: nowrap !important;
                padding: 8px 20px !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 2px 8px rgba(231,76,60,0.15) !important;
            }
            .stButton > button:hover {
                background: linear-gradient(90deg, #e74c3c, #c0392b) !important;
                color: white !important;
                border-color: transparent !important;
                box-shadow: 0 6px 16px rgba(231,76,60,0.35) !important;
                transform: translateY(-1px) !important;
            }

            /* ── Media queries ───────────────────────────────────── */
            @media (min-width: 1400px) {
                .home-header h1 { font-size: 48px !important; }
                .nav-card       { padding: 36px 32px 28px 32px !important; }
                .card-title     { font-size: 22px !important; }
                .card-desc      { font-size: 14px !important; }
            }
            @media (max-width: 899px) {
                .home-header h1 { font-size: 26px !important; }
                .home-header    { padding: 28px 20px !important; }
                .nav-card       { padding: 24px 18px 18px 18px !important; }
                .card-title     { font-size: 16px !important; }
            }
            @media (max-width: 600px) {
                .home-header h1 { font-size: 20px !important; }
                .home-header    { padding: 20px 14px !important; }
                .nav-card       { padding: 18px 14px 14px 14px !important; }
                .card-title     { font-size: 15px !important; }
                .card-desc      { font-size: 12px !important; }
            }
        </style>
    """, unsafe_allow_html=True)