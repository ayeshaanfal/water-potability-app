import streamlit as st
import numpy as np
import joblib
from water_rules import rule_based_check

# Load model
model = joblib.load("water_model.pkl")

st.title("💧 AI Smart Water Quality Advisor")

st.write("Enter key water quality parameters:")

# Inputs with proper units
ph = st.number_input("pH (0–14 scale)", 0.0, 14.0, 7.0)
Solids = st.number_input("Total Dissolved Solids – TDS (mg/L)")
Chloramines = st.number_input("Chloramines (mg/L)")
Organic_carbon = st.number_input("Organic Carbon (mg/L)")
Turbidity = st.number_input("Turbidity (NTU)")

# Info box (looks professional in demo)
st.info("""
Typical Safe Limits:
• pH: 6.5 – 8.5  
• TDS: < 500 mg/L  
• Chloramines: < 4 mg/L  
• Organic Carbon: < 5 mg/L  
• Turbidity: < 1 NTU
""")

if st.button("Check Water Safety"):

    # ML still expects 9 inputs → fill unused with 0
    input_data = np.array([[ph, 0, Solids, Chloramines, 0, 0,
                            Organic_carbon, 0, Turbidity]])

    probability = model.predict_proba(input_data)[0][1]
    risk_score = round((1 - probability) * 100, 2)

    user_data = {
        "ph": ph,
        "Solids": Solids,
        "Chloramines": Chloramines,
        "Organic_carbon": Organic_carbon,
        "Turbidity": Turbidity
    }

    violations = rule_based_check(user_data)

    # Output scores
    st.subheader(f"Safe Water Probability: {probability*100:.2f} %")
    st.subheader(f"Health Risk Score: {risk_score:.2f} %")
    st.progress(int(probability * 100))

    # Water Quality Grade
    if probability >= 0.90:
        grade = "A"
    elif probability >= 0.85:
        grade = "B"
    elif probability >= 0.70:
        grade = "C"
    else:
        grade = "D"

    st.subheader(f"Water Quality Grade: {grade}")

    # Final decision
    if len(violations) > 0:
        st.error("🚨 UNSAFE WATER")
        st.write("Issues detected:")
        for v in violations:
            st.write("•", v)

        # Treatment suggestions
        st.write("Recommended Treatment:")
        if "Unsafe pH" in violations:
            st.write("• Use Neutralizing Filter")
        if "High TDS" in violations:
            st.write("• Use Reverse Osmosis (RO) Filter")
        if "High Chloramines" in violations:
            st.write("• Use Activated Carbon Filter")
        if "High Organic Carbon" in violations:
            st.write("• Use UV or RO Purifier")
        if "High Turbidity" in violations:
            st.write("• Use Sediment Filter")

    elif probability >= 0.85:
        st.success("✅ SAFE TO DRINK")

    else:
        st.warning("⚠️ NEEDS TREATMENT")

st.markdown("---")
st.write("This AI system combines Machine Learning with WHO safety standards.")