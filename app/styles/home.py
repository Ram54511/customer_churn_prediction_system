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

    /* module cards: image backgrounds with dark overlay, only button clickable */
    .module-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 22px;
    }

    .nav-card {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        min-height: 340px;
        border-radius: 26px;
        overflow: hidden;
        position: relative;
        box-shadow: 0 14px 32px rgba(15, 23, 42, 0.14);
        transition: all 0.25s ease;
        background-size: cover !important;
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
        text-decoration: none !important;
    }

    .nav-card p {
        margin: 0 0 14px 0;
        color: rgba(255, 255, 255, 0.85) !important;
        font-size: 14px;
        line-height: 1.55;
        text-decoration: none !important;
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
        text-decoration: none !important;
    }

    /* the only clickable element on the card */
    .card-btn {
        display: block;
        background: white;
        color: #0f172a !important;
        text-decoration: none !important;
        text-align: center;
        padding: 12px 16px;
        border-radius: 999px;
        font-size: 15px;
        font-weight: 800;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .card-btn:hover {
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
    @media screen and (max-width: 600px) {
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