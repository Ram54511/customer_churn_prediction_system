import sys
import os
import pandas as pd
import streamlit as st

# path setup
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)

from config import DATASET_DETAIL
from theme import apply_theme, TEXT_MUTED, PRIMARY, CHURN_COLOR, RETAINED_COLOR
from footer import show_footer
from data_loader import load_data
from calculation.predict_cal import train_models, predict_churn


# load models once and reuse (same tuned pipelines as the Model Results page)
@st.cache_resource(show_spinner=False)
def get_cached_models():
    return train_models(load_data())


# customer input form, returns the raw input dict
def render_input_form() -> dict:
    st.markdown("### Customer Details")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<p style='color:{PRIMARY}; font-weight:bold;'>Personal Info</p>",
                    unsafe_allow_html=True)
        gender         = st.selectbox("Gender",         ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner        = st.selectbox("Partner",        ["Yes", "No"])
        dependents     = st.selectbox("Dependents",     ["No", "Yes"])
        tenure         = st.slider("Tenure (months)",   0, 72, 12)

    with col2:
        st.markdown(f"<p style='color:{PRIMARY}; font-weight:bold;'>Services</p>",
                    unsafe_allow_html=True)
        phone_service   = st.selectbox("Phone Service",     ["Yes", "No"])
        multiple_lines  = st.selectbox("Multiple Lines",    ["No", "Yes", "No phone service"])
        internet        = st.selectbox("Internet Service",  ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security",   ["No", "Yes", "No internet service"])
        online_backup   = st.selectbox("Online Backup",     ["Yes", "No", "No internet service"])
        device_protect  = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        tech_support    = st.selectbox("Tech Support",      ["No", "Yes", "No internet service"])

    with col3:
        st.markdown(f"<p style='color:{PRIMARY}; font-weight:bold;'>Account Info</p>",
                    unsafe_allow_html=True)
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


# overall verdict banner, majority vote at each model's optimised threshold
def render_verdict_banner(results: dict):
    avg_prob    = round(sum(r["probability"] for r in results.values()) / len(results), 1)
    churn_votes = sum(r["will_churn"] for r in results.values())

    if churn_votes >= 2:
        bg, title = CHURN_COLOR, "High Churn Risk"
        detail = f"{churn_votes} of 3 models predict churn (at optimised thresholds)"
    else:
        bg, title = RETAINED_COLOR, "Low Churn Risk"
        detail = f"{3 - churn_votes} of 3 models predict this customer stays"

    st.markdown(
        f"""<div style='background:{bg}; padding:20px; border-radius:10px; text-align:center;'>
            <h2 style='color:white; margin:0;'>{title}</h2>
            <h1 style='color:white; margin:5px 0;'>{avg_prob}%</h1>
            <p style='color:white; margin:0;'>{detail}</p>
        </div>""",
        unsafe_allow_html=True,
    )


# per-model probability cards with their tuned thresholds
def render_model_cards(results: dict):
    st.markdown("### Model Breakdown")
    cols = st.columns(3)

    for col, (model_name, res) in zip(cols, results.items()):
        color   = CHURN_COLOR if res["will_churn"] else RETAINED_COLOR
        verdict = "Churn" if res["will_churn"] else "Stay"
        with col:
            st.markdown(
                f"""<div style='background:white; padding:16px; border-radius:8px;
                            border-top:4px solid {color}; text-align:center;'>
                    <b style='color:{PRIMARY};'>{model_name}</b><br><br>
                    <h2 style='color:{color}; margin:0;'>{res["probability"]}%</h2>
                    <p style='color:{TEXT_MUTED}; font-size:13px; margin:4px 0 0 0;'>
                        Churn probability<br>
                        Verdict: <b style='color:{color};'>{verdict}</b>
                        (threshold {res["threshold"]}%)</p>
                </div>""",
                unsafe_allow_html=True,
            )


# rule-based retention suggestions from known churn drivers
def render_suggestions(inp: dict):
    st.markdown("### Retention Suggestions")
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

    for s in suggestions:
        st.markdown(
            f"""<div style='background:white; padding:10px 14px; border-radius:8px;
                        border-left:4px solid {PRIMARY}; margin-bottom:8px;'>
                {s}
            </div>""",
            unsafe_allow_html=True,
        )


# redirect to login if not logged in
if not st.session_state.get("logged_in"):
    st.switch_page("main.py")

apply_theme()

# back to home
st.page_link("pages/home.py", label="← Back to Home")

# header
st.title("Live Churn Prediction")
st.markdown(
    f"<p style='color:{TEXT_MUTED}; margin-top:-15px;'>"
    f"Enter customer details below to predict churn probability</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# load models (cached, instant after first run)
with st.spinner("Loading models..."):
    trained = get_cached_models()

# input form
input_dict = render_input_form()
st.markdown("<br>", unsafe_allow_html=True)

# predict and show results
if st.button("Predict Churn", use_container_width=True, type="primary"):
    results = predict_churn(input_dict, trained)

    st.markdown("---")
    st.markdown("### Prediction Results")
    render_verdict_banner(results)
    st.markdown("<br>", unsafe_allow_html=True)
    render_model_cards(results)
    st.markdown("<br>", unsafe_allow_html=True)
    render_suggestions(input_dict)

show_footer()