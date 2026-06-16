import streamlit as st


def apply_overview_styles():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');

            /* ── Hide Streamlit elements ─────────────────────────── */
            [data-testid="stSidebar"]        { display: none !important; }
            [data-testid="collapsedControl"]  { display: none !important; }
            [data-testid="stToolbar"]         { display: none !important; }
            [data-testid="stDecoration"]      { display: none !important; }
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

            /* ── Hero header ─────────────────────────────────────── */
            .hero {
                background: linear-gradient(135deg, #0f2742 0%, #1a5c99 50%, #1f77b4 100%);
                border-radius: 20px;
                padding: 48px 44px;
                margin-bottom: 32px;
                position: relative;
                overflow: hidden;
            }
            .hero::before {
                content: '';
                position: absolute;
                top: -60px; right: -60px;
                width: 240px; height: 240px;
                background: rgba(255,255,255,0.05);
                border-radius: 50%;
            }
            .hero::after {
                content: '';
                position: absolute;
                bottom: -80px; left: -40px;
                width: 300px; height: 300px;
                background: rgba(255,127,14,0.08);
                border-radius: 50%;
            }
            .hero h1 {
                font-size: 38px;
                font-weight: 800;
                color: white;
                margin: 0 0 8px 0;
                letter-spacing: -1px;
            }
            .hero p {
                font-size: 15px;
                color: rgba(255,255,255,0.75);
                margin: 0;
            }

            /* ── Back link ───────────────────────────────────────── */
            .stPageLink a {
                display: inline-flex !important;
                align-items: center !important;
                padding: 7px 16px !important;
                background: white !important;
                border: 1.5px solid #1f77b4 !important;
                border-radius: 8px !important;
                color: #1f77b4 !important;
                font-size: 13px !important;
                font-weight: 600 !important;
                text-decoration: none !important;
                transition: all 0.2s ease !important;
                margin-bottom: 12px !important;
            }
            .stPageLink a:hover {
                background: #1f77b4 !important;
                color: white !important;
                transform: translateX(-3px) !important;
            }

            /* ── Stat cards ──────────────────────────────────────── */
            [data-testid="stMetric"] {
                background: white !important;
                border-radius: 14px !important;
                padding: 20px 16px !important;
                box-shadow: 0 2px 16px rgba(0,0,0,0.06) !important;
                border: none !important;
                position: relative;
                overflow: hidden;
                transition: all 0.25s ease !important;
            }
            [data-testid="stMetric"]:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 8px 28px rgba(31,119,180,0.15) !important;
            }
            [data-testid="stMetricLabel"] p {
                font-size: 12px !important;
                font-weight: 600 !important;
                color: #6c757d !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
            }
            [data-testid="stMetricValue"] {
                font-size: 30px !important;
                font-weight: 800 !important;
                color: #0f2742 !important;
            }
            [data-testid="stMetricDelta"] {
                font-size: 13px !important;
                font-weight: 600 !important;
            }

            /* ── Section heading ─────────────────────────────────── */
            .sec-head {
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 20px;
                font-weight: 700;
                color: #0f2742;
                margin: 0 0 20px 0;
            }
            .sec-head span {
                width: 4px;
                height: 22px;
                background: linear-gradient(180deg, #1f77b4, #ff7f0e);
                border-radius: 4px;
                display: inline-block;
            }

            /* ── About card ──────────────────────────────────────── */
            .about-card {
                background: white;
                border-radius: 16px;
                padding: 28px 32px;
                box-shadow: 0 2px 16px rgba(0,0,0,0.06);
                font-size: 15px;
                color: #495057;
                line-height: 1.9;
                border-left: 5px solid #1f77b4;
            }

            /* ── Churn bar ───────────────────────────────────────── */
            .churn-row {
                background: white;
                padding: 12px 16px;
                border-radius: 10px;
                margin-bottom: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                display: flex;
                align-items: center;
                justify-content: space-between;
                transition: all 0.2s ease;
            }
            .churn-row:hover {
                box-shadow: 0 6px 18px rgba(0,0,0,0.09);
                transform: translateX(4px);
            }

            /* ── RQ cards ────────────────────────────────────────── */
            .rq-card {
                background: white;
                border-radius: 12px;
                padding: 18px 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                margin-bottom: 12px;
                border-top: 3px solid #1f77b4;
                font-size: 14px;
                color: #495057;
                transition: all 0.2s ease;
            }
            .rq-card:hover {
                box-shadow: 0 8px 22px rgba(31,119,180,0.12);
                transform: translateY(-2px);
            }
            .rq-card b { color: #1f77b4; }

            /* ── Model cards ─────────────────────────────────────── */
            .model-card {
                background: white;
                border-radius: 16px;
                padding: 28px 22px;
                text-align: center;
                box-shadow: 0 2px 14px rgba(0,0,0,0.06);
                transition: all 0.25s ease;
                height: 100%;
            }
            .model-card:hover {
                box-shadow: 0 12px 32px rgba(0,0,0,0.11);
                transform: translateY(-4px);
            }
            .model-card .m-icon {
                font-size: 36px;
                margin-bottom: 12px;
            }
            .model-card h4 {
                font-size: 16px;
                font-weight: 700;
                color: #0f2742;
                margin: 0 0 8px 0;
            }
            .model-card p {
                font-size: 13px;
                color: #6c757d;
                line-height: 1.6;
                margin: 0;
            }
            .model-card .tag {
                display: inline-block;
                background: rgba(31,119,180,0.1);
                color: #1f77b4;
                border-radius: 20px;
                padding: 3px 12px;
                font-size: 11px;
                font-weight: 600;
                margin-top: 12px;
            }

            /* ── Pipeline ────────────────────────────────────────── */
            .pipe-step {
                background: white;
                border-radius: 12px;
                padding: 16px 20px;
                margin-bottom: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.04);
                display: flex;
                align-items: flex-start;
                gap: 14px;
                transition: all 0.2s ease;
            }
            .pipe-step:hover {
                box-shadow: 0 6px 20px rgba(31,119,180,0.12);
                transform: translateX(5px);
            }
            .pipe-step .step-num {
                background: linear-gradient(135deg, #1f77b4, #0f2742);
                color: white;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 13px;
                font-weight: 700;
                flex-shrink: 0;
            }
            .pipe-step .step-title {
                font-size: 14px;
                font-weight: 700;
                color: #0f2742;
                margin: 0 0 4px 0;
            }
            .pipe-step .step-desc {
                font-size: 12px;
                color: #6c757d;
                margin: 0;
                line-height: 1.5;
            }

            /* ── Tool cards ──────────────────────────────────────── */
            .tool-card {
                background: white;
                border-radius: 14px;
                padding: 22px 18px;
                text-align: center;
                box-shadow: 0 2px 12px rgba(0,0,0,0.05);
                transition: all 0.2s ease;
            }
            .tool-card:hover {
                box-shadow: 0 8px 24px rgba(0,0,0,0.1);
                transform: translateY(-3px);
            }
            .tool-card .t-icon { font-size: 32px; margin-bottom: 10px; }
            .tool-card h4 { font-size: 14px; font-weight: 700; color: #0f2742; margin: 0 0 6px 0; }
            .tool-card p  { font-size: 12px; color: #6c757d; margin: 0; line-height: 1.5; }

            /* ── Divider ─────────────────────────────────────────── */
            .sec-divider {
                height: 1px;
                background: linear-gradient(90deg, #e9ecef, transparent);
                margin: 28px 0;
            }

            /* ── Media queries ───────────────────────────────────── */
            @media (max-width: 768px) {
                .hero h1    { font-size: 26px !important; }
                .hero        { padding: 28px 20px !important; }
            }
        </style>
    """, unsafe_allow_html=True)