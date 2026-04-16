import streamlit as st
import numpy as np
import joblib
from water_rules import rule_based_check

# Load model (5-feature trained model)
model = joblib.load("water_model.pkl")

st.title("💧 AI Smart Water Quality Advisor")
st.write("Enter key water quality parameters:")

# ---------------- INPUTS ----------------
ph = st.number_input("pH (0–14 scale)", 0.0, 14.0, 7.0)
Solids = st.number_input("Total Dissolved Solids (TDS)")
Chloramines = st.number_input("Chloramines (mg/L)")
Organic_carbon = st.number_input("Organic Carbon (mg/L)")
Turbidity = st.number_input("Turbidity (NTU)")

# ---------------- UNIT SELECTORS ----------------
st.subheader("Optional Unit Selection")
tds_unit = st.selectbox("TDS Unit", ["mg/L", "ppm"])
carbon_unit = st.selectbox("Organic Carbon Unit", ["mg/L", "g/L"])
turbidity_unit = st.selectbox("Turbidity Unit", ["NTU", "FNU"])

# ---------------- INFO BOX ----------------
st.info("""
Typical Safe Limits:
• pH: 6.5 – 8.5  
• TDS: < 500 mg/L  
• Chloramines: < 4 mg/L  
• Organic Carbon: < 5 mg/L  
• Turbidity: < 1 NTU
""")

# ---------------- UNIT CONVERSION ----------------
def convert_inputs(ph, tds, chloramines, organic_carbon, turbidity,
                   tds_unit, carbon_unit, turbidity_unit):

    # ppm ≈ mg/L (no change needed)
    if tds_unit == "ppm":
        tds = tds

    # g/L → mg/L
    if carbon_unit == "g/L":
        organic_carbon = organic_carbon * 1000

    return ph, tds, chloramines, organic_carbon, turbidity


# ================= PREDICTION =================
if st.button("Check Water Safety"):

    # Convert units
    ph, Solids, Chloramines, Organic_carbon, Turbidity = convert_inputs(
        ph, Solids, Chloramines, Organic_carbon, Turbidity,
        tds_unit, carbon_unit, turbidity_unit
    )

    # ML input (5 features)
    input_data = np.array([[ph, Solids, Chloramines, Organic_carbon, Turbidity]])

    # -------- ML BASE PREDICTION --------
    probability = model.predict_proba(input_data)[0][1]

    # -------- RULE CHECK --------
    user_data = {
        "ph": ph,
        "Solids": Solids,
        "Chloramines": Chloramines,
        "Organic_carbon": Organic_carbon,
        "Turbidity": Turbidity
    }
    violations = rule_based_check(user_data)

    # ===== SMART PROBABILITY CALIBRATION =====

    # Case 1 — Unsafe water → strong penalty
    if len(violations) > 0:
        probability = probability * 0.4

    # Case 2 — PERFECT water → strong boost
    elif (6.5 <= ph <= 8.5 and
          Solids < 300 and
          Chloramines < 3 and
          Organic_carbon < 3 and
          Turbidity < 0.5):
        probability = min(probability + 0.35, 0.99)

    # Case 3 — GOOD water → small boost
    elif (6.5 <= ph <= 8.5 and
          Solids < 500 and
          Chloramines < 4 and
          Organic_carbon < 5 and
          Turbidity < 1):
        probability = min(probability + 0.20, 0.95)

    # Final risk score
    risk_score = round((1 - probability) * 100, 2)

    # ===== FINAL DECISION =====
    if len(violations) > 0:
        status = "UNSAFE"
        grade = "D"

    elif probability >= 0.85:
        status = "SAFE"
        grade = "A"

    elif probability >= 0.70:
        status = "NEEDS TREATMENT"
        grade = "C"

    else:
        status = "NEEDS TREATMENT"
        grade = "D"

    # ================= OUTPUT =================
    st.subheader(f"Safe Water Probability: {probability*100:.2f} %")
    st.subheader(f"Health Risk Score: {risk_score:.2f} %")
    st.progress(int(probability * 100))
    st.subheader(f"Water Quality Grade: {grade}")

    # ===== RESULT DISPLAY =====
    if status == "UNSAFE":
        st.error("🚨 UNSAFE WATER")
        st.write("Issues detected:")
        for v in violations:
            st.write("•", v)

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

    elif status == "SAFE":
        st.success("✅ SAFE TO DRINK")

    else:
        st.warning("⚠️ NEEDS TREATMENT")

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("AI system combining Machine Learning + WHO Water Quality Safety Rules")