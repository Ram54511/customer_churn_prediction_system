import sys
import os
import streamlit as st

# path setup
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)

from styles.predict import (apply_predict_styles, PAGE_BG, CARD_BG,
                             TEAL, CHURN_COLOR, RETAINED_COLOR, AMBER)
from header import show_header
from footer import show_footer
from data_loader import load_data
from auth.guard import require_login
from calculation.predict_cal import train_models, predict_churn


@st.cache_resource(show_spinner=False)
def get_cached_models():
    return train_models(load_data())


def section(title: str):
    st.markdown(f"<p class='pr-section'>{title}</p>", unsafe_allow_html=True)


def divider():
    st.markdown("<div class='pr-divider'></div>", unsafe_allow_html=True)


# three-column input form
def render_input_form() -> dict:
    section("Customer Details")
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("<p class='pr-col-title'>Personal Info</p>", unsafe_allow_html=True)
        gender         = st.selectbox("Gender",         ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner        = st.selectbox("Partner",        ["Yes", "No"])
        dependents     = st.selectbox("Dependents",     ["No", "Yes"])
        tenure         = st.slider("Tenure (months)",   0, 72, 12)

    with col2:
        st.markdown("<p class='pr-col-title'>Services</p>", unsafe_allow_html=True)
        phone_service   = st.selectbox("Phone Service",     ["Yes", "No"])
        multiple_lines  = st.selectbox("Multiple Lines",    ["No", "Yes", "No phone service"])
        internet        = st.selectbox("Internet Service",  ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security",   ["No", "Yes", "No internet service"])
        online_backup   = st.selectbox("Online Backup",     ["Yes", "No", "No internet service"])
        device_protect  = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        tech_support    = st.selectbox("Tech Support",      ["No", "Yes", "No internet service"])

    with col3:
        st.markdown("<p class='pr-col-title'>Account Info</p>", unsafe_allow_html=True)
        streaming_tv     = st.selectbox("Streaming TV",      ["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies",  ["No", "Yes", "No internet service"])
        contract         = st.selectbox("Contract",          ["Month-to-month", "One year", "Two year"])
        paperless        = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment          = st.selectbox("Payment Method", [
                               "Electronic check",
                               "Mailed check",
                               "Bank transfer (automatic)",
                               "Credit card (automatic)"])
        monthly_charges  = st.number_input("Monthly Charges ($)", 0.0, 200.0, 65.0, step=0.5)
        total_charges    = st.number_input("Total Charges ($)", 0.0, 10000.0,
                                           round(monthly_charges * tenure, 2), step=1.0)

    return {
        "gender":           gender,
        "SeniorCitizen":    1 if senior_citizen == "Yes" else 0,
        "Partner":          partner,
        "Dependents":       dependents,
        "tenure":           tenure,
        "PhoneService":     phone_service,
        "MultipleLines":    multiple_lines,
        "InternetService":  internet,
        "OnlineSecurity":   online_security,
        "OnlineBackup":     online_backup,
        "DeviceProtection": device_protect,
        "TechSupport":      tech_support,
        "StreamingTV":      streaming_tv,
        "StreamingMovies":  streaming_movies,
        "Contract":         contract,
        "PaperlessBilling": paperless,
        "PaymentMethod":    payment,
        "MonthlyCharges":   monthly_charges,
        "TotalCharges":     total_charges,
    }


# large verdict banner with majority vote
def render_verdict_banner(results: dict):
    section("Prediction Results")
    avg_prob    = round(sum(r["probability"] for r in results.values()) / len(results), 1)
    churn_votes = sum(r["will_churn"] for r in results.values())

    if churn_votes >= 2:
        bg     = f"rgba(226,75,74,0.15)"
        border = CHURN_COLOR
        title  = "High Churn Risk"
        detail = f"{churn_votes} of 3 models predict churn (at optimised thresholds)"
        color  = CHURN_COLOR
    else:
        bg     = f"rgba(29,158,117,0.15)"
        border = RETAINED_COLOR
        title  = "Low Churn Risk"
        detail = f"{3 - churn_votes} of 3 models predict this customer stays"
        color  = RETAINED_COLOR

    st.markdown(
        f'<div class="pr-verdict" style="background:{bg};border:1px solid {border}30;">'
        f'<p class="pr-verdict-title">{title}</p>'
        f'<p class="pr-verdict-value" style="color:{color};">{avg_prob}%</p>'
        f'<p class="pr-verdict-detail">{detail}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


# three model cards
def render_model_cards(results: dict):
    section("Model Breakdown")

    cards_html = '<div class="pr-model-grid">'
    for model_name, res in results.items():
        color   = CHURN_COLOR if res["will_churn"] else RETAINED_COLOR
        verdict = "Churn" if res["will_churn"] else "Stay"
        prob    = res["probability"]
        cards_html += (
            f'<div class="pr-model-card" style="border-top:3px solid {color};">'
            f'<p class="pr-model-name">{model_name}</p>'
            f'<p class="pr-model-prob" style="color:{color};">{prob}%</p>'
            f'<p class="pr-model-verdict" style="color:{color};">{verdict}</p>'
            f'<p class="pr-model-threshold">threshold {res["threshold"]}%</p>'
            f'<div class="pr-model-bar">'
            f'<div class="pr-model-fill" style="width:{prob}%;background:{color};"></div>'
            f'</div>'
            f'</div>'
        )
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


# retention suggestions
def render_suggestions(inp: dict):
    section("Retention Suggestions")
    suggestions = []

    if inp["Contract"] == "Month-to-month":
        suggestions.append("Offer a discounted <b>one or two year contract</b> to increase loyalty.")
    if inp["InternetService"] == "Fiber optic":
        suggestions.append("Provide <b>service quality assurance</b> or a loyalty discount for Fiber optic users.")
    if inp["PaymentMethod"] == "Electronic check":
        suggestions.append("Encourage switching to <b>automatic payment</b> for a smoother experience.")
    if inp["tenure"] < 12:
        suggestions.append("Offer <b>new customer loyalty rewards</b> to improve early retention.")
    if inp["MonthlyCharges"] > 70:
        suggestions.append("Consider a <b>personalised discount</b> to reduce monthly charges.")
    if not suggestions:
        suggestions.append("This customer appears stable. Maintain current service quality.")

    html = "".join(
        f'<div class="pr-suggestion">{s}</div>'
        for s in suggestions
    )
    st.markdown(html, unsafe_allow_html=True)


# guard and render
require_login()
apply_predict_styles()
show_header(back=True)

with st.spinner("Loading models..."):
    trained = get_cached_models()

input_dict = render_input_form()
st.markdown("<br>", unsafe_allow_html=True)

if st.button("Predict Churn", use_container_width=True, type="primary"):
    results = predict_churn(input_dict, trained)

    st.markdown("<br>", unsafe_allow_html=True)
    render_verdict_banner(results)
    st.markdown("<br>", unsafe_allow_html=True)
    render_model_cards(results)
    st.markdown("<br>", unsafe_allow_html=True)
    render_suggestions(input_dict)

show_footer()