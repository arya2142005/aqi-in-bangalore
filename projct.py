import streamlit as st
import numpy as np
import pickle

# Page setup
st.set_page_config(page_title="AQI Predictor 🌿", page_icon="🌿", layout="centered")

# Title
st.markdown("""
    <h1 style='text-align: center; color: #2c3e50; font-size: 3em;'>🌿 AQI Predictor</h1>
    <p style='text-align: center; color: #34495e;'>Check the air quality around you and stay safe!</p>
""", unsafe_allow_html=True)

# Inputs
pm25 = st.number_input("Enter PM2.5", min_value=0.0, format="%.2f")
pm10 = st.number_input("Enter PM10", min_value=0.0, format="%.2f")
no2 = st.number_input("Enter NO2", min_value=0.0, format="%.2f")
so2 = st.number_input("Enter SO2", min_value=0.0, format="%.2f")
co = st.number_input("Enter CO", min_value=0.0, format="%.2f")
o3 = st.number_input("Enter O3", min_value=0.0, format="%.2f")

# Load model
try:
    with open("aqi.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("🚫 Model not found! Please save your model as `aqi.pkl`.")
    st.stop()

# Category mapper
def get_aqi_info(aqi):
    if aqi <= 50:
        return "Good", "#00e400", "✅ Air quality is good."
    elif aqi <= 100:
        return "Moderate", "#ffff00", "😐 Acceptable air quality for most."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "#ff7e00", "⚠️ Risky for sensitive people."
    elif aqi <= 200:
        return "Unhealthy", "#ff0000", "❌ Everyone may be affected."
    elif aqi <= 300:
        return "Very Unhealthy", "#8f3f97", "❌ Serious effects for everyone."
    else:
        return "Hazardous", "#7e0023", "🚨 Emergency conditions!"

# Predict and show output
if st.button("🌍 Predict AQI"):
    features = np.array([[pm25, pm10, no2, so2, co, o3]])
    prediction = model.predict(features)[0]
    category, color, message = get_aqi_info(prediction)
    
    st.markdown(f"<h2 style='text-align:center;'>Predicted AQI: {int(prediction)}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center; color:{color};'>{category}</h3>", unsafe_allow_html=True)
    st.info(message)

    # Map AQI to angle (0-180 deg)
    angle = int((prediction / 500) * 180)

    # Analog meter styling
    st.markdown(f"""
    <style>
    .meter-container {{
        width: 300px;
        height: 180px;
        margin: auto;
        margin-top: 30px;
        background: rgba(255,255,255,0.1);
        border-radius: 150px 150px 0 0;
        position: relative;
        box-shadow: inset 0 4px 20px rgba(0,0,0,0.2), 0 8px 30px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }}
    .needle {{
        width: 4px;
        height: 90px;
        background: #000;
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: rotate({angle}deg);
        transform-origin: bottom;
        transition: transform 1s ease-in-out;
    }}
    .label {{
        position: absolute;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 13px;
        color: #2c3e50;
    }}
    .ticks {{
        position: absolute;
        top: 60%;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        display: flex;
        justify-content: space-between;
        padding: 0 10px;
        font-weight: bold;
        font-size: 12px;
    }}
    </style>
    <div class="meter-container">
        <div class="needle"></div>
        <div class="ticks">
            <div>0</div><div>100</div><div>200</div><div>300</div><div>400</div><div>500</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
