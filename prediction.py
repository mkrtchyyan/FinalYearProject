import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import base64

# Set page configuration (MUST BE THE FIRST STREAMLIT COMMAND)
st.set_page_config(page_title="Water Quality Prediction", page_icon="💧", layout="wide")


# Function to set background image
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    bg_css = f"""
    <style>
    .stApp {{
        background: url("data:image/jpg;base64,{encoded_string}") no-repeat center center fixed;
        background-size: cover;
    }}
    h1, h2, h3, h4, h5, h6, p {{
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    }}
    label {{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        font-weight: bold;
    }}
    .stButton button {{
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s;
    }}
    .stButton button:hover {{
        background-color: #45a049;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)


# Set background image
set_background("futuristic-science-lab-background_23-2148505015.jpg")  # Replace with your image file path

# Load the model
try:
    model = joblib.load("svm.pkl")
    #st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Define safe thresholds for each parameter (updated based on Kaggle info)
safe_thresholds = {
    "pH Level": {"min": 6.5, "max": 8.5},  # WHO standard
    "Hardness": {"max": 200},  # No specific WHO limit, but high hardness can affect taste
    "Solids": {"max": 500},  # Desirable limit for TDS
    "Chloramines": {"max": 4},  # Safe level for drinking water
    "Sulfate": {"max": 250},  # Higher concentrations may affect taste
    "Conductivity": {"max": 400},  # WHO standard
    "Organic Carbon": {"max": 4},  # US EPA standard for source water
    "Trihalomethanes": {"max": 80},  # Safe level for drinking water
    "Turbidity": {"max": 5},  # WHO recommended value
}

# Mapping Armenian labels to English safe_threshold keys
armenian_to_english = {
    "pH մակարդակ/թթվայնություն": "pH Level",
    "Կարծրություն": "Hardness",
    "Լուծված պինդ նյութեր": "Solids",
    "Քլորամիններ": "Chloramines",
    "Սուլֆատներ": "Sulfate",
    "Էլեկտրահաղորդականություն": "Conductivity",
    "Օրգանական ածխածին": "Organic Carbon",
    "Տրիալոմեթաններ": "Trihalomethanes",
    "Պղտորություն": "Turbidity"
}


# Function to check unsafe parameters
def check_unsafe_parameters(input_values, safe_thresholds, input_labels, language):
    unsafe_parameters = []
    for i, (param, value) in enumerate(zip(input_labels, input_values)):
        # Convert Armenian labels to English for threshold checking
        param_key = armenian_to_english.get(param, param)  # If not Armenian, keep the same

        if param_key in safe_thresholds:
            thresholds = safe_thresholds[param_key]
            if "min" in thresholds and value < thresholds["min"]:
                reason = f"{param} շատ ցածր է (նվազագույն՝ {thresholds['min']}, ընթացիկ՝ {value})" if language == "Հայերեն" else f"{param} is too low (min: {thresholds['min']}, current: {value})"
                unsafe_parameters.append(reason)
            if "max" in thresholds and value > thresholds["max"]:
                reason = f"{param} շատ բարձր է (առավելագույն՝ {thresholds['max']}, ընթացիկ՝ {value})" if language == "Հայերեն" else f"{param} is too high (max: {thresholds['max']}, current: {value})"
                unsafe_parameters.append(reason)

    return unsafe_parameters


# Language Selection
language = st.radio("🌍 Select Language / Ընտրեք Լեզուն", ("English", "Հայերեն"))

# Define text based on language
if language == "English":
    title = "💧 Water Quality Prediction"
    subtitle = "Check if the water is safe to drink!"
    input_labels = ["pH Level", "Hardness", "Solids", "Chloramines", "Sulfate",
                    "Conductivity", "Organic Carbon", "Trihalomethanes", "Turbidity"]
    predict_button = "Predict Water Quality"
    safe_text = "✅ Safe to drink!"
    unsafe_text = "❌ Unsafe! Do not drink!"
    about_title = "## About us"
    about_text = "### This website predicts water quality based on various parameters. Use the inputs to enter values and click 'Predict Water Quality' to see the result."
    footer_text = "###### Made by Manan Mkrtchyan"
else:
    title = "💧 Ջրի Որակի Կանխատեսում"
    subtitle = "Ստուգեք՝ ջուրը խմելու համար անվտանգ է,թե ոչ։"
    input_labels = ["pH մակարդակ/թթվայնություն", "Կարծրություն", "Լուծված պինդ նյութեր", "Քլորամիններ", "Սուլֆատներ",
                    "Էլեկտրահաղորդականություն", "Օրգանական ածխածին", "Տրիալոմեթաններ", "Պղտորություն"]
    predict_button = "Կանխատեսել Ջրի Որակը"
    safe_text = "✅ Անվտանգ է խմելու համար!"
    unsafe_text = "❌ Վտանգավոր է! Մի խմեք!"
    about_title = "### Մեր Մասին"
    about_text = "#### Այս հավելվածը կանխատեսում է ջրի որակը՝ հիմնվելով տարբեր պարամետրերի վրա։ Մուտքագրեք տվյալները և սեղմեք «Կանխատեսել Ջրի Որակը»՝ արդյունքը տեսնելու համար։"
    footer_text = "###### Ստեղծվել է Մանան Մկրտչյանի կողմից"

# Title and Subtitle
st.markdown(f"<h1 style='text-align: center; font-size: 2.5em;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; font-size: 1.5em;'>{subtitle}</h3>", unsafe_allow_html=True)

# Create input fields in columns with a modern layout
col1, col2 = st.columns(2)

with col1:
    ph = st.number_input(input_labels[0], value=7.0, step=0.1, format="%.2f", key="ph")
    hardness = st.number_input(input_labels[1], value=150.0, step=1.0, format="%.2f", key="hardness")
    solids = st.number_input(input_labels[2], value=300.0, step=1.0, format="%.2f", key="solids")
    chloramines = st.number_input(input_labels[3], value=2.0, step=0.1, format="%.2f", key="chloramines")
    sulfate = st.number_input(input_labels[4], value=200.0, step=1.0, format="%.2f", key="sulfate")

with col2:
    conductivity = st.number_input(input_labels[5], value=500.0, step=1.0, format="%.2f", key="conductivity")
    organicCarbon = st.number_input(input_labels[6], value=3.0, step=0.1, format="%.2f", key="organicCarbon")
    trihalomethanes = st.number_input(input_labels[7], value=50.0, step=1.0, format="%.2f", key="trihalomethanes")
    turbidity = st.number_input(input_labels[8], value=2.0, step=0.1, format="%.2f", key="turbidity")

# Predict button with a sleek design
if st.button(predict_button):
    input_values = [ph, hardness, solids, chloramines, sulfate, conductivity, organicCarbon, trihalomethanes, turbidity]
    try:
        # Scale the input values (if required by the model)
        scaler = StandardScaler()
        input_values_scaled = scaler.fit_transform([input_values])

        # Make prediction
        prediction = model.predict(input_values_scaled)[0]
        if prediction == 1:
            st.success(safe_text)
        else:
            st.error(unsafe_text)
            # Check for unsafe parameters
            unsafe_parameters = check_unsafe_parameters(input_values, safe_thresholds, input_labels, language)
            if unsafe_parameters:
                if language == "English":
                    st.markdown("**Reasons why the water is unsafe:**")
                else:
                    st.markdown("**Ջրի անվտանգ չլինելու պատճառները.**")
                for reason in unsafe_parameters:
                    st.write(f"- {reason}")
    except Exception as e:
        st.error(f"Error making prediction: {e}")

# Footer
st.markdown("---")
st.markdown(about_title)
st.markdown(about_text)
st.markdown(footer_text)
