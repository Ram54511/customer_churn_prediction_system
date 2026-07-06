import sys
import base64
from pathlib import Path
import streamlit as st

# path setup
APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))

from app.config import DATASET_DETAIL
from app.pages.header import show_header
from styles.home import apply_home_styles
from footer import show_footer

# card background images (assests folder at project root)
ASSETS_DIR = APP_DIR.parent / "assests"


# read an image and return it as a base64 data uri, or empty string if missing
def img_data_uri(filename: str) -> str:
    path = ASSETS_DIR / filename
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/png;base64,{encoded}"


# hero section with navbar
show_header("Exploratory Data Analysis", DATASET_DETAIL)

# dashboard module cards with image backgrounds, badges, and pill button
def render_modules():
    st.markdown(
        """
<div class="section-title">
    <h2>Dashboard Modules</h2>
    <p>Select a section to analyse the churn prediction system.</p>
</div>
        """,
        unsafe_allow_html=True,
    )

    modules = [
        ("Overview",
         "Dataset summary, churn rate, customer counts, and the key business statistics behind the project.",
         ["Key metrics", "Research questions"],
         "/overview", "card-overview", "Open Overview", "overview.png"),
        ("EDA",
         "Explore customer patterns, service usage, distributions, and churn behaviour across segments.",
         ["10+ charts", "Interactive"],
         "/eda", "card-eda", "Open EDA", "eda.png"),
        ("Model Results",
         "Compare Logistic Regression, Random Forest, and XGBoost with tuned thresholds and SMOTE.",
         ["3 models", "GridSearchCV"],
         "/model", "card-model", "Open Models", "module result.png"),
        ("SHAP Analysis",
         "Understand the main churn drivers using explainable AI, globally and per customer.",
         ["Explainable AI", "Beeswarm"],
         "/shap", "card-shap", "Open SHAP", "SHAP.png"),
        ("Live Prediction",
         "Enter customer details and generate a real-time churn prediction with retention suggestions.",
         ["Real-time", "3-model vote"],
         "/predict", "card-predict", "Open Prediction", "livepreiction.png"),
    ]

    cards = ""
    for title, description, badges, href, card_class, cta, image in modules:
        badge_html = "".join(f'<span class="card-badge">{b}</span>' for b in badges)
        uri = img_data_uri(image)
        # image background if the file exists, otherwise the css gradient fallback shows
        bg_style = f'style="background-image: url({uri});"' if uri else ""
        cards += f"""<a class="nav-card {card_class}" href="{href}" target="_self" {bg_style}>
                <div class="card-body">
                    <h3>{title}</h3>
                    <p>{description}</p>
                    <div class="card-badges">{badge_html}</div>
                    <span class="card-btn">{cta}</span>
                </div>
            </a>"""

    st.markdown(f'<div class="module-grid">{cards}</div>', unsafe_allow_html=True)


# apply page styles first
apply_home_styles()

# handle logout from navbar
if st.query_params.get("logout") == "true":
    st.query_params.clear()
    st.session_state.clear()
    st.switch_page("main.py")

# redirect to login if not logged in
if not st.session_state.get("logged_in"):
    st.switch_page("main.py")

username = st.session_state.get("username", "admin")

# page sections
st.markdown("<br>", unsafe_allow_html=True)
render_modules()
st.markdown("<br><br>", unsafe_allow_html=True)

show_footer()