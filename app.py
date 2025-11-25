# app.py
import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the trained model and encoders
model = joblib.load('policy_model.pkl')
encoders = joblib.load('encoders.pkl')

st.set_page_config(page_title="Jan Suraksha AI", page_icon="🛡️")

# --- UI Header ---
st.title("🛡️ Jan Suraksha AI")
st.subheader("Micro-Insurance Recommender for Low-Income Groups")
st.markdown("---")

# --- Sidebar Input ---
st.sidebar.header("Enter Beneficiary Details")

age = st.sidebar.slider("Age", 18, 65, 30)
bmi = st.sidebar.slider("BMI", 15.0, 40.0, 24.5)
income = st.sidebar.number_input("Daily Income (INR)", min_value=100, max_value=5000, value=400)
children = st.sidebar.slider("Number of Children", 0, 10, 2)

# For categorical inputs, we need to show text but feed numbers to model
smoker = st.sidebar.selectbox("Smoker?", encoders['smoker'].classes_)
occupation = st.sidebar.selectbox("Occupation", encoders['occupation'].classes_)
medical = st.sidebar.selectbox("Medical History", encoders['medical_history'].classes_)

# --- Prediction Logic ---
if st.sidebar.button("Find Best Policy"):
    # 1. Encode the inputs using the saved encoders
    smoker_enc = encoders['smoker'].transform([smoker])[0]
    occupation_enc = encoders['occupation'].transform([occupation])[0]
    medical_enc = encoders['medical_history'].transform([medical])[0]
    
    # 2. Create input array (order must match training!)
    input_data = np.array([[age, bmi, income, children, smoker_enc, occupation_enc, medical_enc]])
    
    # 3. Predict
    prediction_idx = model.predict(input_data)[0]
    policy_name = encoders['target'].inverse_transform([prediction_idx])[0]
    
    # 4. Display Result
    st.success(f"✅ Recommended Policy: **{policy_name}**")
    
    # 5. Dynamic Explanation (Why this policy?)
    st.markdown("### 💡 Why this policy?")
    
    if "Accidental" in policy_name:
        st.info("Because the user works in a high-risk physical job (Construction/Driver), accidental coverage is prioritized.")
    elif "Govt" in policy_name:
        st.info("Because the daily income is below ₹500, a subsidized government scheme is the most affordable option.")
    elif "Family" in policy_name:
        st.info("Because the user has 3+ children, high death-benefit coverage is required to support the dependents.")
    elif "Critical" in policy_name:
        st.info("Due to health risks (Smoking/BMI/Medical History), a plan covering Critical Illness is essential.")
    else:
        st.info("The user has a stable health and income profile suitable for a standard endowment plan.")

    # 6. Show Input Summary
    with st.expander("See User Profile Summary"):
        st.write({
            "Age": age,
            "Income": f"₹{income}/day",
            "Occupation": occupation,
            "Dependents": children
        })

else:
    st.info("👈 Please enter details in the sidebar to get a recommendation.")