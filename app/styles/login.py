import streamlit as st


def apply_login_styles():
    """
    Injects all CSS styles for the login page.
    """
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

            /*Hide sidebar & toolbar only*/
            [data-testid="stSidebar"]        { display: none !important; }
            [data-testid="collapsedControl"]  { display: none !important; }
            [data-testid="stToolbar"]         { display: none !important; }
            [data-testid="stDecoration"]      { display: none !important; }
            [data-testid="stStatusWidget"]    { display: none !important; }
            .stAppDeployButton                { display: none !important; }
            #MainMenu                         { display: none !important; }
            footer                            { display: none !important; }

                
            /* Remove top padding only*/
            .block-container {
                padding-top: 1rem !important;
            }

            /* Global font*/
            html, body, .stApp {
                font-family: 'Poppins', sans-serif;
            }

            /*Full page gradient background */
            .stApp {
                background: linear-gradient(135deg, #0f2742 0%, #1f77b4 60%, #ff7f0e 100%);
                min-height: 100vh;
            }

            /* Login card */
            .login-card {
                padding: 50px 50px;
                
            }

            /* Title */
            .login-title {
                font-size: 48px;
                font-weight: 700;
                color: #0f2742;
                margin: 0;
                line-height: 1.1;
                letter-spacing: -0.5px;
            }

            /* Media queries for smaller screens */
            @media (max-width: 1200px) {
                .login-title { font-size: 40px !important; }
            }
            @media (max-width: 900px) {
                .login-title { font-size: 32px !important; }
                .login-card  { padding: 30px 28px !important; }
            }
            @media (max-width: 600px) {
                .login-title { font-size: 22px !important; }
                .login-card  { padding: 20px 16px !important; border-radius: 12px !important; }
            }
            @media (max-width: 400px) {
                .login-title { font-size: 18px !important; }
                .login-card  { padding: 16px 12px !important; }
            }


            /*  Divider */
            .login-divider {
                border: none;
                border-top: 1px solid white;
                margin: 20px 0;

            }

            /* Section heading */
            .login-heading {
                font-size: 18px;
                font-weight: 600;
                color: #212529;
                margin-bottom: 16px;
            }

            /*Input fields */
            .stTextInput > div > div > input {
                border-radius: 8px !important;
                border: 1.5px solid #dee2e6 !important;
                padding: 10px 14px !important;
                font-family: 'Poppins', sans-serif !important;
                font-size: 14px !important;
            }
            .stTextInput > div > div > input:focus {
                border-color: #1f77b4 !important;
                box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.15) !important;
            }

            /* Login button */
            .stButton > button {
                background: linear-gradient(90deg, #1f77b4, #0f2742) !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px !important;
                font-size: 15px !important;
                font-weight: 600 !important;
                font-family: 'Poppins', sans-serif !important;
                box-shadow: 0 4px 14px rgba(31, 119, 180, 0.4) !important;
                transition: all 0.2s ease !important;
            }
            .stButton > button:hover {
                background: linear-gradient(90deg, #ff7f0e, #e05c00) !important;
                box-shadow: 0 6px 20px rgba(255, 127, 14, 0.45) !important;
                transform: translateY(-1px) !important;
            }

            /* Footer */
            .login-footer {
                text-align: center;
                font-size: 11px;
                color: #adb5bd;
                margin-top: 8px;
            }
        </style>
    """, unsafe_allow_html=True)