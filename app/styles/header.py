import streamlit as st


def apply_header_styles():
    st.markdown(
        """
<style>
    /* hide streamlit chrome */
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    div[data-testid="collapsedControl"] {
        display: none !important;
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* full-width container with side padding */
    div[data-testid="stMainBlockContainer"],
    section[data-testid="stMain"] .block-container,
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem !important;
        padding-left: 3vw !important;
        padding-right: 3vw !important;
        max-width: 100% !important;
        width: 100% !important;
    }

    /* slim header bar, breaks out of container padding to touch screen edges */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin: 0 -3vw 22px -3vw;
        padding: 0 3vw;
        height: 58px;
        background: linear-gradient(135deg, #020617 0%, #0f172a 55%, #1e3a8a 100%);
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.22);
        position: relative;
        z-index: 100;
    }

    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        color: white !important;
        text-decoration: none !important;
        font-size: 15px;
        font-weight: 850;
        white-space: nowrap;
    }

    .brand-logo {
        height: 32px;
        width: 32px;
        object-fit: contain;
        border-radius: 8px;
    }

    .brand-dot {
        color: #38bdf8;
        font-size: 15px;
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 12px;
        position: relative;
    }

    .logout-btn {
        background: #ef4444;
        color: white !important;
        text-decoration: none !important;
        padding: 7px 14px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
        transition: all 0.2s ease;
        white-space: nowrap;
    }

    .logout-btn:hover {
        background: #dc2626;
    }

    /* hamburger button (css-only, checkbox trick) */
    .nav-toggle {
        display: none;
    }

    .hamburger {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 5px;
        width: 40px;
        height: 40px;
        padding: 8px;
        border-radius: 10px;
        cursor: pointer;
        background: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: background 0.2s ease;
    }

    .hamburger:hover {
        background: rgba(255, 255, 255, 0.18);
    }

    .hamburger span {
        display: block;
        height: 2px;
        width: 100%;
        background: white;
        border-radius: 2px;
        transition: all 0.25s ease;
    }

    /* hamburger turns into an X when open */
    .nav-toggle:checked ~ .hamburger span:nth-child(1) {
        transform: translateY(7px) rotate(45deg);
    }

    .nav-toggle:checked ~ .hamburger span:nth-child(2) {
        opacity: 0;
    }

    .nav-toggle:checked ~ .hamburger span:nth-child(3) {
        transform: translateY(-7px) rotate(-45deg);
    }

    /* dropdown menu */
    .nav-menu {
        position: absolute;
        top: 52px;
        right: 0;
        min-width: 200px;
        display: flex;
        flex-direction: column;
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 8px;
        box-shadow: 0 18px 40px rgba(2, 6, 23, 0.45);
        opacity: 0;
        visibility: hidden;
        transform: translateY(-8px);
        transition: all 0.2s ease;
    }

    .nav-toggle:checked ~ .nav-menu {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }

    .nav-menu a {
        color: rgba(255, 255, 255, 0.85) !important;
        text-decoration: none !important;
        font-size: 14px;
        font-weight: 700;
        padding: 11px 14px;
        border-radius: 10px;
        transition: all 0.15s ease;
    }

    .nav-menu a:hover {
        background: rgba(255, 255, 255, 0.12);
        color: white !important;
    }

    /* page heading under the bar */
    .page-heading {
        margin: 4px 0 18px 0;
    }

    .page-heading h1 {
        margin: 0;
        color: #0f172a;
        font-size: clamp(24px, 3vw, 32px);
        font-weight: 850;
        letter-spacing: -0.5px;
    }

    /* back to home button under the header bar */
    .back-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin: 0 0 14px 0;
        padding: 8px 14px;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 999px;
        color: #0f172a !important;
        text-decoration: none !important;
        font-size: 13px;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
        transition: all 0.2s ease;
    }

    .back-btn:hover {
        border-color: #2563eb;
        color: #2563eb !important;
        transform: translateX(-2px);
    }

    .page-heading p {
        margin: 6px 0 0 0;
        color: #64748b;
        font-size: 14px;
    }

    /* responsive */
    @media screen and (max-width: 600px) {
        div[data-testid="stMainBlockContainer"],
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .app-header {
            margin: 0 -1rem 18px -1rem;
            padding: 0 1rem;
        }

        .nav-brand {
            font-size: 14px;
        }
    }
</style>
        """,
        unsafe_allow_html=True,
    )