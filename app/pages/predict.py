import sys
import os
import pandas as pd
import streamlit as st

# ── Path setup ─────────────────────────────────────────────────────────────────
_APP_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_APP_DIR)
sys.path.insert(0, _APP_DIR)
sys.path.insert(0, _ROOT_DIR)


from config import DATASET_PATH, DATASET_DETAIL
from theme import apply_theme, TEXT_MUTED, PRIMARY, CHURN_COLOR, RETAINED_COLOR, ACCENT
from footer import show_footer
from calculation.predict_cal import train_models, predict_churn

# ── Guard ──────────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("login.py")

# ── Apply theme ────────────────────────────────────────────────────────────────
apply_theme()

# ── Load & train ───────────────────────────────────────────────────────────────
df = pd.read_csv(DATASET_PATH)

with st.spinner("⏳ Training models... please wait"):
    trained = train_models(df)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"<h4 style='color:white;'>👤 {st.session_state.get('username', 'admin')}</h4>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("<p style='color:white;'>📌 Navigation</p>", unsafe_allow_html=True)
    st.page_link("pages/home.py",     label="🏠 Home")
    st.page_link("pages/overview.py", label="📊 Overview")
    st.page_link("pages/eda.py",      label="🔍 EDA")
    st.page_link("pages/model.py",    label="🤖 Model Results")
    st.page_link("pages/shap.py",     label="🧠 SHAP Analysis")
    st.page_link("pages/predict.py",  label="🎯 Live Predict")
    for _ in range(10):
        st.write("")
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("login.py")

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🎯 Live Churn Prediction")
st.markdown(
    f"<p style='color:{TEXT_MUTED}; margin-top:-15px;'>"
    f"Enter customer details below to predict churn probability</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ── Input Form ────────────────────────────────────────────────────────────────
st.markdown("### 👤 Customer Details")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<p style='color:{PRIMARY}; font-weight:bold;'>Personal Info</p>", unsafe_allow_html=True)
    gender          = st.selectbox("Gender",          ["Male", "Female"])
    senior_citizen  = st.selectbox("Senior Citizen",  ["No", "Yes"])
    partner         = st.selectbox("Partner",         ["Yes", "No"])
    dependents      = st.selectbox("Dependents",      ["No", "Yes"])
    tenure          = st.slider("Tenure (months)",    0, 72, 12)

with col2:
    st.markdown(f"<p style='color:{PRIMARY}; font-weight:bold;'>Services</p>", unsafe_allow_html=True)
    phone_service   = st.selectbox("Phone Service",      ["Yes", "No"])
    multiple_lines  = st.selectbox("Multiple Lines",     ["No", "Yes", "No phone service"])
    internet        = st.selectbox("Internet Service",   ["DSL", "Fiber optic", "No"])
    online_security = st.selectbox("Online Security",    ["No", "Yes", "No internet service"])
    online_backup   = st.selectbox("Online Backup",      ["Yes", "No", "No internet service"])
    device_protect  = st.selectbox("Device Protection",  ["No", "Yes", "No internet service"])
    tech_support    = st.selectbox("Tech Support",       ["No", "Yes", "No internet service"])

with col3:
    st.markdown(f"<p style='color:{PRIMARY}; font-weight:bold;'>Account Info</p>", unsafe_allow_html=True)
    streaming_tv    = st.selectbox("Streaming TV",       ["No", "Yes", "No internet service"])
    streaming_movies= st.selectbox("Streaming Movies",   ["No", "Yes", "No internet service"])
    contract        = st.selectbox("Contract",           ["Month-to-month", "One year", "Two year"])
    paperless       = st.selectbox("Paperless Billing",  ["Yes", "No"])
    payment         = st.selectbox("Payment Method",     [
                                    "Electronic check",
                                    "Mailed check",
                                    "Bank transfer (automatic)",
                                    "Credit card (automatic)"])
    monthly_charges = st.number_input("Monthly Charges ($)", 0.0, 200.0, 65.0, step=0.5)
    total_charges   = st.number_input("Total Charges ($)",   0.0, 10000.0,
                                       round(monthly_charges * tenure, 2), step=1.0)

st.markdown("<br>", unsafe_allow_html=True)

# ── Predict Button ────────────────────────────────────────────────────────────
predict_btn = st.button("🎯 Predict Churn", use_container_width=True, type="primary")

if predict_btn:
    input_dict = {
        "gender":            gender,
        "SeniorCitizen":     1 if senior_citizen == "Yes" else 0,
        "Partner":           partner,
        "Dependents":        dependents,
        "tenure":            tenure,
        "PhoneService":      phone_service,
        "MultipleLines":     multiple_lines,
        "InternetService":   internet,
        "OnlineSecurity":    online_security,
        "OnlineBackup":      online_backup,
        "DeviceProtection":  device_protect,
        "TechSupport":       tech_support,
        "StreamingTV":       streaming_tv,
        "StreamingMovies":   streaming_movies,
        "Contract":          contract,
        "PaperlessBilling":  paperless,
        "PaymentMethod":     payment,
        "MonthlyCharges":    monthly_charges,
        "TotalCharges":      total_charges,
    }

    results = predict_churn(input_dict, trained)

    st.markdown("---")
    st.markdown("### 📊 Prediction Results")

    # ── Average probability ───────────────────────────────────────────────────
    avg_prob = round(sum(results.values()) / len(results), 1)

    if avg_prob >= 50:
        st.markdown(
            f"""<div style='background:{CHURN_COLOR}; padding:20px; border-radius:10px; text-align:center;'>
                <h2 style='color:white; margin:0;'>⚠️ High Churn Risk</h2>
                <h1 style='color:white; margin:5px 0;'>{avg_prob}%</h1>
                <p style='color:white; margin:0;'>This customer is likely to churn</p>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div style='background:{RETAINED_COLOR}; padding:20px; border-radius:10px; text-align:center;'>
                <h2 style='color:white; margin:0;'>✅ Low Churn Risk</h2>
                <h1 style='color:white; margin:5px 0;'>{avg_prob}%</h1>
                <p style='color:white; margin:0;'>This customer is likely to stay</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Per model results ─────────────────────────────────────────────────────
    st.markdown("### 🤖 Model Breakdown")
    col1, col2, col3 = st.columns(3)

    for col, (model_name, prob) in zip([col1, col2, col3], results.items()):
        color = CHURN_COLOR if prob >= 50 else RETAINED_COLOR
        with col:
            st.markdown(
                f"""<div style='background:white; padding:16px; border-radius:8px;
                            border-top:4px solid {color}; text-align:center;'>
                    <b style='color:{PRIMARY};'>{model_name}</b><br><br>
                    <h2 style='color:{color}; margin:0;'>{prob}%</h2>
                    <p style='color:{TEXT_MUTED}; font-size:13px; margin:4px 0 0 0;'>Churn Probability</p>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Retention Suggestions ─────────────────────────────────────────────────
    st.markdown("### 💡 Retention Suggestions")
    suggestions = []

    if contract == "Month-to-month":
        suggestions.append("📋 Offer a discounted **One or Two year contract** to increase loyalty.")
    if internet == "Fiber optic":
        suggestions.append("🌐 Provide **service quality assurance** or loyalty discount for Fiber optic users.")
    if payment == "Electronic check":
        suggestions.append("💳 Encourage switching to **automatic payment** for smoother experience.")
    if tenure < 12:
        suggestions.append("🎁 Offer **new customer loyalty rewards** to improve early retention.")
    if monthly_charges > 70:
        suggestions.append("💰 Consider a **personalised discount** to reduce monthly charges.")
    if not suggestions:
        suggestions.append("✅ This customer appears stable. Maintain current service quality.")

    for s in suggestions:
        st.markdown(
            f"""<div style='background:white; padding:10px 14px; border-radius:8px;
                        border-left:4px solid {PRIMARY}; margin-bottom:8px;'>
                {s}
            </div>""",
            unsafe_allow_html=True,
        )

# ── Footer ────────────────────────────────────────────────────────────────────
show_footer()