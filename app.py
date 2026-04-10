import streamlit as st
import numpy as np
import joblib
from water_rules import rule_based_check

# Load model
model = joblib.load("water_model.pkl")

st.title("💧 AI Water Safety Checker")

st.write("Enter key water quality parameters:")

ph = st.number_input("pH value", 0.0, 14.0, 7.0)
Solids = st.number_input("Total Dissolved Solids (TDS)")
Chloramines = st.number_input("Chloramines")
Organic_carbon = st.number_input("Organic Carbon")
Turbidity = st.number_input("Turbidity")

if st.button("Check Water Safety"):

    # ML still expects 9 inputs → fill unused with 0
    input_data = np.array([[ph, 0, Solids, Chloramines, 0, 0,
                            Organic_carbon, 0, Turbidity]])

    probability = model.predict_proba(input_data)[0][1]

    user_data = {
        "ph": ph,
        "Solids": Solids,
        "Chloramines": Chloramines,
        "Organic_carbon": Organic_carbon,
        "Turbidity": Turbidity
    }

    violations = rule_based_check(user_data)
    risk_score = round((1 - probability) * 100, 2)

    st.subheader(f"Safe Water Probability: {probability*100:.2f}%")
    st.subheader(f"Health Risk Score: {risk_score}%")

    # Final decision
    if len(violations) > 0:
        st.error("🚨 UNSAFE WATER")
        st.write("Issues detected:")
        for v in violations:
            st.write("•", v)

    elif probability >= 0.70:
        st.success("✅ SAFE TO DRINK")

    else:
        st.warning("⚠️ NEEDS TREATMENT")