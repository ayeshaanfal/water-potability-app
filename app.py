import streamlit as st
import numpy as np
import joblib

# Load trained model
model = joblib.load("water_model.pkl")

st.title("💧 Water Potability Predictor")

st.write("Enter water quality parameters:")

ph = st.number_input("pH value", 0.0, 14.0, 7.0)
Hardness = st.number_input("Hardness")
Solids = st.number_input("Total Dissolved Solids")
Chloramines = st.number_input("Chloramines")
Sulfate = st.number_input("Sulfate")
Conductivity = st.number_input("Conductivity")
Organic_carbon = st.number_input("Organic Carbon")
Trihalomethanes = st.number_input("Trihalomethanes")
Turbidity = st.number_input("Turbidity")

if st.button("Predict"):
    input_data = np.array([[ph, Hardness, Solids, Chloramines, Sulfate,
                            Conductivity, Organic_carbon,
                            Trihalomethanes, Turbidity]])

    probability = model.predict_proba(input_data)[0][1]
    result = model.predict(input_data)[0]

    st.subheader(f"Probability of Safe Water: {probability*100:.2f}%")

    if result == 1:
        st.success("✅ Water is SAFE to drink")
    else:
        st.error("❌ Water is NOT safe to drink")