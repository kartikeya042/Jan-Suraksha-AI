# app.py (Indian Edition 🇮🇳)
import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the trained model (You must re-run train_model.py first!)
try:
    model = joblib.load('policy_model.pkl')
    encoders = joblib.load('encoders.pkl')
except FileNotFoundError:
    st.error("Please run 'train_model.py' to generate the Indian model first!")
    st.stop()

st.set_page_config(page_title="Jan Suraksha AI", page_icon="🇮🇳")

# --- UI Header ---
st.title("🇮🇳 Jan Suraksha AI")
st.caption("Smart Policy Recommender for Bharat (Micro-Insurance)")
st.markdown("---")

# --- Input Form ---
st.sidebar.header("Beneficiary Details (लाभार्थी विवरण)")

age = st.sidebar.slider("Age (आयु)", 18, 60, 35)
income = st.sidebar.number_input("Daily Income in ₹ (दैनिक आय)", min_value=150, max_value=2000, value=400)
children = st.sidebar.slider("Dependents (Children)", 0, 6, 2)
bmi = st.sidebar.slider("BMI (Approx Health)", 15.0, 35.0, 24.0)

# Dropdowns using the Indian categories
occ_options = encoders['occupation'].classes_
occupation = st.sidebar.selectbox("Occupation (व्यवसाय)", occ_options)

tobacco = st.sidebar.radio("Consumes Tobacco/Smoking?", ["No", "Yes"])
tobacco_val = 1 if tobacco == "Yes" else 0

# City Tier (Mocked for input as we didn't train heavily on it, but good for UI)
city = st.sidebar.selectbox("Location", ["Rural (Village)", "Tier-2 City", "Tier-1 (Metro)"])

# --- Prediction ---
if st.sidebar.button("Find Best Scheme (योजना खोजें)"):
    
    # Encode inputs
    try:
        occ_enc = encoders['occupation'].transform([occupation])[0]
        # We need to match the feature columns exactly as they were trained
        # Features: [age, bmi, daily_income_inr, children, smoker_tobacco(encoded), occupation(encoded), tier_city(encoded)]
        # Note: If you changed features in generate_data, ensure train_model matches. 
        # For simplicity here, I am assuming the basic columns are used.
        
        # Simplify input array for the demo (Make sure this matches train_model.py X columns!)
        # Let's assume we trained on: age, bmi, income, children, smoker, occupation
        # We need to encode 'tobacco' properly if it was text in training.
        
        # Quick fix for demo logic: We will rebuild the input based on the 'smoker' encoder
        tobacco_enc = encoders['smoker_tobacco'].transform([tobacco])[0]
        
        # Dummy value for Tier City if not used in model, or encode if used
        tier_enc = encoders['tier_city'].transform(['Rural' if 'Rural' in city else 'Tier-2'])[0]

        input_data = pd.DataFrame(
            [[age, bmi, income, children, tobacco_enc, occ_enc, tier_enc]],
            columns=['age', 'bmi', 'daily_income_inr', 'children', 'smoker_tobacco', 'occupation', 'tier_city']
        )
        
        prediction_idx = model.predict(input_data)[0]
        policy_name = encoders['target'].inverse_transform([prediction_idx])[0]
        
        # --- Display Result ---
        st.success(f"✅ Recommended Scheme: **{policy_name}**")
        
        # --- Contextual Explanation ---
        st.markdown("### 📋 Why this scheme? (क्यों?)")
        
        if "PMSBY" in policy_name:
            st.info(f"The user is a **{occupation}**. Since this job has high physical risk, the **Pradhan Mantri Suraksha Bima Yojana** (Accidental Cover) is best. It costs only ₹20/year.")
        elif "PMJJBY" in policy_name:
            st.info(f"With a daily income of ₹{income}, **PMJJBY** provides a pure life cover of ₹2 Lakhs for just ₹436/year. Ideal for securing the family.")
        elif "Gramin" in policy_name:
            st.info("Since the user profile suggests a rural background (Farmer/Village), **Postal Life Insurance** offers high bonuses with low premiums.")
        elif "Saral" in policy_name:
            st.info("The user has a slightly higher income stability. **Saral Jeevan Bima** is a standard term plan regulated by IRDAI for better coverage.")
        else:
            st.warning("A standard micro-savings plan is recommended to build a corpus.")
            
    except Exception as e:
        st.error(f"Error in processing: {e}. Please re-train model with new data.")

else:
    st.info("👈 Enter details to get a Government/Private scheme recommendation.")