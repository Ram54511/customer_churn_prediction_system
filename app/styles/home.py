import streamlit as st


def apply_home_styles():
    st.markdown(
        """
<style>
    /* hide streamlit sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    div[data-testid="collapsedControl"] {
        display: none !important;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* full-width fluid layout instead of a fixed centered column */
    div[data-testid="stMainBlockContainer"],
    section[data-testid="stMain"] .block-container,
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3vw !important;
        padding-right: 3vw !important;
        max-width: 100% !important;
        width: 100% !important;
    }

    /* hero background */
    .hero-section {
        background:
            radial-gradient(circle at top right, rgba(59, 130, 246, 0.45), transparent 35%),
            linear-gradient(135deg, #020617 0%, #0f172a 45%, #1e3a8a 100%);
        padding: 22px 28px 42px 28px;
        border-radius: 30px;
        color: white;
        box-shadow: 0 22px 55px rgba(15, 23, 42, 0.28);
        position: relative;
        overflow: hidden;
    }

    /* navbar inside hero */
    .top-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        padding: 12px 14px;
        margin-bottom: 38px;
        background: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        backdrop-filter: blur(14px);
    }

    .nav-brand {
        display: flex;
        align-items: center;
        gap: 9px;
        color: white;
        font-size: 16px;
        font-weight: 850;
        white-space: nowrap;
    }

    .brand-dot {
        color: #38bdf8;
        font-size: 16px;
    }

    .nav-links {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        flex: 1;
    }

    .nav-links a {
        color: rgba(255, 255, 255, 0.82) !important;
        text-decoration: none !important;
        font-size: 14px;
        font-weight: 700;
        padding: 10px 13px;
        border-radius: 12px;
        transition: all 0.2s ease;
    }

    .nav-links a:hover {
        background: rgba(255, 255, 255, 0.16);
        color: white !important;
    }

    .logout-btn {
        background: #ef4444;
        color: white !important;
        text-decoration: none !important;
        padding: 10px 16px;
        border-radius: 13px;
        font-size: 14px;
        font-weight: 800;
        transition: all 0.2s ease;
        box-shadow: 0 10px 24px rgba(239, 68, 68, 0.28);
        white-space: nowrap;
    }

    .logout-btn:hover {
        background: #dc2626;
        transform: translateY(-2px);
    }

    /* hero content */
    .hero-content {
        padding-left: 10px;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: rgba(255, 255, 255, 0.9);
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 18px;
    }

    .welcome-text {
        margin: 0 0 8px 0;
        color: rgba(255, 255, 255, 0.72);
        font-size: 14px;
        font-weight: 500;
    }

    .hero-section h1 {
        margin: 0;
        color: white;
        font-size: clamp(28px, 4.5vw, 48px);
        font-weight: 850;
        letter-spacing: -1px;
        line-height: 1.12;
    }

    .hero-subtitle {
        margin-top: 15px;
        margin-bottom: 0;
        max-width: 780px;
        color: rgba(255, 255, 255, 0.82);
        font-size: clamp(14px, 1.6vw, 16px);
        line-height: 1.65;
    }

    /* section title */
    .section-title {
        margin-bottom: 18px;
    }

    .section-title h2 {
        margin: 0;
        color: #0f172a;
        font-size: 28px;
        font-weight: 850;
    }

    .section-title p {
        margin-top: 6px;
        color: #64748b;
        font-size: 15px;
    }

    /* module cards: image backgrounds with dark overlay, badges, pill button */
    .module-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 22px;
    }

    a.nav-card,
    a.nav-card:hover,
    a.nav-card:visited,
    a.nav-card:active {
        text-decoration: none !important;
    }

    .nav-card h3,
    .nav-card p,
    .nav-card .card-badge,
    .nav-card .card-btn {
        text-decoration: none !important;
    }

    .nav-card {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        min-height: 340px;
        border-radius: 26px;
        overflow: hidden;
        position: relative;
        cursor: pointer;
        box-shadow: 0 14px 32px rgba(15, 23, 42, 0.14);
        transition: all 0.25s ease;
        background-size: contain !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-color: #0f172a;
    }

    .nav-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 26px 55px rgba(15, 23, 42, 0.24);
    }

    /* dark overlay that fades up from the bottom, keeps text readable on images */
    .nav-card::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(
            to top,
            rgba(2, 6, 23, 0.88) 0%,
            rgba(2, 6, 23, 0.55) 45%,
            rgba(2, 6, 23, 0.15) 75%,
            rgba(2, 6, 23, 0.05) 100%
        );
    }

    .card-body {
        position: relative;
        z-index: 1;
        padding: 22px;
    }

    .nav-card h3 {
        margin: 0 0 8px 0;
        color: white !important;
        font-size: 24px;
        font-weight: 800;
    }

    .nav-card p {
        margin: 0 0 14px 0;
        color: rgba(255, 255, 255, 0.85) !important;
        font-size: 14px;
        line-height: 1.55;
    }

    .card-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 16px;
    }

    .card-badge {
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.14);
        backdrop-filter: blur(8px);
        color: rgba(255, 255, 255, 0.92) !important;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }

    .card-btn {
        display: block;
        background: white;
        color: #0f172a !important;
        text-align: center;
        padding: 12px 16px;
        border-radius: 999px;
        font-size: 15px;
        font-weight: 800;
        transition: all 0.2s ease;
    }

    .nav-card:hover .card-btn {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(2, 6, 23, 0.35);
    }

    /* per-module gradient fallbacks (show if an image file is missing) */
    .card-overview {
        background-image:
            radial-gradient(circle at 20% 15%, rgba(96, 165, 250, 0.55), transparent 50%),
            linear-gradient(160deg, #1d4ed8 0%, #1e3a8a 55%, #172554 100%);
    }

    .card-eda {
        background-image:
            radial-gradient(circle at 80% 10%, rgba(103, 232, 249, 0.5), transparent 50%),
            linear-gradient(160deg, #0e7490 0%, #155e75 55%, #164e63 100%);
    }

    .card-model {
        background-image:
            radial-gradient(circle at 25% 12%, rgba(196, 181, 253, 0.5), transparent 50%),
            linear-gradient(160deg, #7c3aed 0%, #5b21b6 55%, #3b0764 100%);
    }

    .card-shap {
        background-image:
            radial-gradient(circle at 75% 15%, rgba(253, 186, 116, 0.5), transparent 50%),
            linear-gradient(160deg, #ea580c 0%, #c2410c 55%, #7c2d12 100%);
    }

    .card-predict {
        background-image:
            radial-gradient(circle at 30% 10%, rgba(134, 239, 172, 0.5), transparent 50%),
            linear-gradient(160deg, #16a34a 0%, #15803d 55%, #14532d 100%);
    }

    /* responsive */
    @media screen and (max-width: 900px) {
        .top-navbar {
            flex-direction: column;
            align-items: stretch;
            gap: 12px;
        }

        .nav-brand {
            justify-content: center;
        }

        .nav-links {
            flex-wrap: wrap;
            justify-content: center;
        }

        .logout-btn {
            text-align: center;
        }

        .hero-content {
            padding-left: 0;
        }
    }

    @media screen and (max-width: 600px) {
        div[data-testid="stMainBlockContainer"],
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .hero-section {
            padding: 18px 18px 30px 18px;
            border-radius: 22px;
        }

        .top-navbar {
            margin-bottom: 24px;
        }

        .nav-links a {
            font-size: 13px;
            padding: 8px 10px;
        }

        .module-grid {
            gap: 14px;
        }

        .nav-card {
            min-height: 300px;
            border-radius: 22px;
        }

        .nav-card h3 {
            font-size: 21px;
        }
    }
</style>
        """,
        unsafe_allow_html=True,
    )