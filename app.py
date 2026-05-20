import streamlit as st
import numpy as np
import joblib
from water_rules import rule_based_check

# ================= LOAD MODEL =================
model = joblib.load("water_model.pkl")

# ================= PAGE TITLE =================
st.title("💧 AI Smart Water Quality Advisor")

st.write("Enter water quality parameters:")

# ================= USER INPUTS =================
ph = st.number_input("pH", 0.0, 14.0, 7.0)

TDS = st.number_input("TDS (mg/L)", 0.0, 5000.0, 200.0)

Hardness = st.number_input("Total Hardness (mg/L)", 0.0, 1000.0, 150.0)

Nitrate = st.number_input("Nitrate (mg/L)", 0.0, 200.0, 20.0)

Fluoride = st.number_input("Fluoride (mg/L)", 0.0, 10.0, 0.8)

Turbidity = st.number_input("Turbidity (NTU)", 0.0, 100.0, 2.0)

# ================= SAFE LIMITS INFO =================
st.info("""
WHO Drinking Water Guidelines:

• pH: 6.5 – 8.5  
• TDS: < 500 mg/L  
• Total Hardness: < 200 mg/L  
• Nitrate: < 45 mg/L  
• Fluoride: 0.6 – 1.5 mg/L  
• Turbidity: < 5 NTU
""")

# ================= BUTTON =================
if st.button("Check Water Safety"):

    # ================= ML INPUT =================
    input_data = np.array([[
        ph,
        TDS,
        Hardness,
        Nitrate,
        Fluoride,
        Turbidity
    ]])

    # ================= ML PREDICTION =================
    probability = model.predict_proba(input_data)[0][1]

    # ================= RULE CHECK =================
    user_data = {
        "ph": ph,
        "TDS": TDS,
        "Hardness": Hardness,
        "Nitrate": Nitrate,
        "Fluoride": Fluoride,
        "Turbidity": Turbidity
    }

    violations = rule_based_check(user_data)

    # ================= SMART CALIBRATION =================

    # Unsafe water → reduce confidence
    if len(violations) > 0:
        probability = probability * 0.4

    # Excellent water → very high confidence
    elif (
        6.8 <= ph <= 8.0 and
        TDS < 300 and
        Hardness < 180 and
        Nitrate < 30 and
        0.7 <= Fluoride <= 1.2 and
        Turbidity < 3
    ):
        probability = max(probability, 0.95)

    # Safe water → strong confidence
    elif (
        6.5 <= ph <= 8.5 and
        TDS < 500 and
        Hardness < 200 and
        Nitrate < 45 and
        0.6 <= Fluoride <= 1.5 and
        Turbidity < 5
    ):
        probability = max(probability, 0.88)

    # ================= RISK SCORE =================
    risk_score = round((1 - probability) * 100, 2)

    # ================= FINAL STATUS =================
    if len(violations) > 0:
        status = "UNSAFE"
        grade = "D"

    else:
        status = "SAFE"

        if probability >= 0.90:
            grade = "A"

        elif probability >= 0.75:
            grade = "B"

        else:
            grade = "C"

    # ================= OUTPUT =================
    st.subheader(f"Safe Water Probability: {probability*100:.2f}%")

    st.subheader(f"Health Risk Score: {risk_score:.2f}%")

    st.progress(int(probability * 100))

    st.subheader(f"Water Quality Grade: {grade}")

    # ================= SAFE RESULT =================
    if status == "SAFE":

        st.success("✅ SAFE TO DRINK")

        st.write("### ✅ Water Quality Summary")

        st.write("All major parameters are within WHO safe limits.")

    # ================= UNSAFE RESULT =================
    else:

        st.error("🚨 UNSAFE WATER")

        st.write("### Issues Detected")

        for v in violations:
            st.write(f"• {v}")

        # ================= RISK ANALYSIS =================
        st.subheader("⚠️ Risk Analysis & Health Effects")

        # ================= pH =================
        if "Unsafe pH" in violations:

            if ph < 6.5:

                st.write("🔴 pH is LOW → Water is acidic")

                st.write("Possible Effects:")
                st.write("• Pipe corrosion")
                st.write("• Metallic taste")
                st.write("• Stomach irritation")

            else:

                st.write("🔴 pH is HIGH → Water is alkaline")

                st.write("Possible Effects:")
                st.write("• Bitter taste")
                st.write("• Skin irritation")

            st.write("✅ Suggested Solution:")
            st.write("• Use pH Neutralizer")

        # ================= TDS =================
        if "High TDS" in violations:

            st.write("🔴 High TDS detected")

            st.write("Possible Effects:")
            st.write("• Salty or unpleasant taste")
            st.write("• Kidney stress")
            st.write("• Pipe scaling")

            st.write("✅ Suggested Solution:")
            st.write("• Use Reverse Osmosis (RO) Filter")

        # ================= HARDNESS =================
        if "High Hardness" in violations:

            st.write("🔴 Water hardness is HIGH")

            st.write("Possible Effects:")
            st.write("• Scale formation")
            st.write("• Soap inefficiency")
            st.write("• Pipe blockage")

            st.write("✅ Suggested Solution:")
            st.write("• Install Water Softener")

        # ================= NITRATE =================
        if "High Nitrate" in violations:

            st.write("🔴 High nitrate detected")

            st.write("Possible Effects:")
            st.write("• Harmful for infants")
            st.write("• Blue baby syndrome risk")

            st.write("✅ Suggested Solution:")
            st.write("• Use RO or Ion Exchange Treatment")

        # ================= FLUORIDE =================
        if "Unsafe Fluoride" in violations:

            if Fluoride > 1.5:

                st.write("🔴 Fluoride level is TOO HIGH")

                st.write("Possible Effects:")
                st.write("• Dental fluorosis")
                st.write("• Bone problems")

            else:

                st.write("🟠 Fluoride level is TOO LOW")

                st.write("Possible Effects:")
                st.write("• Reduced dental protection")

            st.write("✅ Suggested Solution:")
            st.write("• Use Activated Alumina Filter")

        # ================= TURBIDITY =================
        if "High Turbidity" in violations:

            st.write("🔴 High turbidity detected")

            st.write("Possible Effects:")
            st.write("• Suspended particles")
            st.write("• Possible microbial contamination")

            st.write("✅ Suggested Solution:")
            st.write("• Use Sediment Filter")

# ================= FOOTER =================
st.markdown("---")

st.write("AI system combining Machine Learning + WHO Water Quality Standards")