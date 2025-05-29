import streamlit as st
import requests
import json
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Bank Churn Prediction", page_icon="🏦")

# Sidebar navigation
PAGES = {
    "Predict Churn": "predict",
    "View Logs": "logs"
}
page = st.sidebar.radio("Select page", list(PAGES.keys()))

API_URL = "http://fastapi:8000/predict"

# --- Sidebar JWT Token Flow ---
st.sidebar.header("Enter JWT Token")

if "jwt_token" not in st.session_state:
    st.session_state["jwt_token"] = ""

jwt_input = st.sidebar.text_input(
    "Paste your JWT token here", type="password", value=st.session_state["jwt_token"]
)

if st.sidebar.button("Submit JWT Token"):
    if not jwt_input.strip():
        st.sidebar.error("Please enter a JWT token.")
    else:
        st.session_state["jwt_token"] = jwt_input.strip()
        st.sidebar.success("JWT Token saved!")

jwt_token = st.session_state["jwt_token"]

if page == "Predict Churn":
    st.title("🏦 Bank Customer Churn Prediction")
    if not jwt_token:
        st.info("🔑 Please enter your JWT token in the sidebar and click 'Submit JWT Token'.")
        st.stop()

    st.header("Enter Customer Details")
    col1, col2 = st.columns(2)
    with col1:
        credit_score = st.number_input("Credit Score", value=650, min_value=300, max_value=900)

        geography_labels = ["France", "Germany", "Spain"]
        geography_selected = st.selectbox("Geography", options=geography_labels)
        geography_map = {"France": 0, "Germany": 1, "Spain": 2}
        geography = geography_map[geography_selected]

        gender_labels = ["Female", "Male"]
        gender_selected = st.selectbox("Gender", options=gender_labels)
        gender_map = {"Female": 0, "Male": 1}
        gender = gender_map[gender_selected]

        age = st.number_input("Age", value=42, min_value=18, max_value=100)
        tenure = st.number_input("Tenure (years as customer)", value=4, min_value=0, max_value=20)
    with col2:
        balance = st.number_input("Balance", value=102000.50, min_value=0.0)
        num_of_products = st.selectbox("Number of Products", options=[1, 2, 3, 4], index=1)

        has_cr_card_labels = ["No", "Yes"]
        has_cr_card_selected = st.selectbox("Has Credit Card?", options=has_cr_card_labels)
        has_cr_card_map = {"No": 0, "Yes": 1}
        has_cr_card = has_cr_card_map[has_cr_card_selected]

        is_active_member_labels = ["No", "Yes"]
        is_active_member_selected = st.selectbox("Is Active Member?", options=is_active_member_labels)
        is_active_member_map = {"No": 0, "Yes": 1}
        is_active_member = is_active_member_map[is_active_member_selected]

        est_salary = st.number_input("Estimated Salary", value=80000.00, min_value=0.0)

    features = [
        float(credit_score),
        float(geography),
        float(gender),
        float(age),
        float(tenure),
        float(balance),
        float(num_of_products),
        float(has_cr_card),
        float(is_active_member),
        float(est_salary)
    ]
    if st.button("Predict Churn"):
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        payload = {"features": features}
        with st.spinner("Contacting the Churn Prediction API..."):
            try:
                response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
                if response.status_code == 200:
                    result = response.json()
                    if result.get("customer_status") == "CHURN":
                        st.error("⚠️ This customer is at HIGH RISK of churn!")
                    else:
                        st.success("✅ This customer is likely to be retained.")
                    st.json(result)
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to the API. Details: {str(e)}")
    st.markdown("""
    ---
    **How to get a JWT token:**  
    In your terminal or Python shell, run:
    ```python
    from app.jwt import create_token
    print(create_token("alice"))
    ```
    """)

elif page == "View Logs":
    st.title("📋 View Churn Prediction Logs")
    engine = create_engine("sqlite:///./churn_logs.db")
    try:
        df = pd.read_sql("SELECT * FROM prediction_logs ORDER BY timestamp DESC", con=engine)
        df["features"] = df["features"].apply(lambda x: ", ".join([str(val) for val in json.loads(x)]))
        st.dataframe(df, use_container_width=True)
        st.success(f"Loaded {len(df)} predictions from churn_logs.db")
        with st.expander("Show column description"):
            st.write("""
                - **user_id**: JWT token user.
                - **features**: Customer features (ordered list).
                - **prediction**: "CHURN" or "RETAIN".
                - **timestamp**: Time of prediction.
            """)
    except Exception as e:
        st.warning(f"Could not load logs: {str(e)}")
        st.info("Make some predictions first to see logs here.")
