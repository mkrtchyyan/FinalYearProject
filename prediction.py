import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import base64

# Set page configuration
st.set_page_config(page_title="Water Quality Prediction", page_icon="💧", layout="wide")

# Background image
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

set_background("futuristic-science-lab-background_23-2148505015.jpg")

# Load model and scaler
try:
    model = joblib.load("svm.pkl")
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    st.error(f"Error loading model or scaler: {e}")
    st.stop()

# Safe thresholds
safe_thresholds = {
    "pH Level": {"min": 6.5, "max": 8.5},
    "Hardness": {"max": 200},
    "Solids": {"max": 500},
    "Chloramines": {"max": 4},
    "Sulfate": {"max": 250},
    "Conductivity": {"max": 400},
    "Organic Carbon": {"max": 4},
    "Trihalomethanes": {"max": 80},
    "Turbidity": {"max": 5},
}

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

def check_unsafe_parameters(input_values, safe_thresholds, input_labels, language):
    unsafe_parameters = []
    for i, (param, value) in enumerate(zip(input_labels, input_values)):
        param_key = armenian_to_english.get(param, param)
        if param_key in safe_thresholds:
            thresholds = safe_thresholds[param_key]
            if "min" in thresholds and value < thresholds["min"]:
                reason = f"{param} շատ ցածր է (նվազագույն՝ {thresholds['min']}, ընթացիկ՝ {value})" if language == "Հայերեն" else f"{param} is too low (min: {thresholds['min']}, current: {value})"
                unsafe_parameters.append(reason)
            if "max" in thresholds and value > thresholds["max"]:
                reason = f"{param} շատ բարձր է (առավելագույն՝ {thresholds['max']}, ընթացիկ՝ {value})" if language == "Հայերեն" else f"{param} is too high (max: {thresholds['max']}, current: {value})"
                unsafe_parameters.append(reason)
    return unsafe_parameters

# Language
language = st.radio("🌍 Select Language / Ընտրեք Լեզուն", ("English", "Հայերեն"))

# Localized UI content
if language == "English":
    title = "💧 Water Quality Prediction"
    subtitle = "Check if the water is safe to drink!"
    input_labels = ["pH Level", "Hardness", "Solids", "Chloramines", "Sulfate",
                    "Conductivity", "Organic Carbon", "Trihalomethanes", "Turbidity"]
    predict_button = "Predict Water Quality"
    safe_text = "✅ Safe to drink!"
    unsafe_text = "❌ Unsafe! Do not drink!"
    upload_label = "📁 Or Upload CSV File"
    download_label = "📥 Download Results as CSV"
    column_warning = "CSV must contain exactly 9 columns."
    success_label = "✅ Prediction Completed:"
else:
    title = "💧 Ջրի Որակի Կանխատեսում"
    subtitle = "Ստուգեք՝ ջուրը խմելու համար անվտանգ է, թե ոչ։"
    input_labels = ["pH մակարդակ/թթվայնություն", "Կարծրություն", "Լուծված պինդ նյութեր", "Քլորամիններ", "Սուլֆատներ",
                    "Էլեկտրահաղորդականություն", "Օրգանական ածխածին", "Տրիալոմեթաններ", "Պղտորություն"]
    predict_button = "Կանխատեսել Ջրի Որակը"
    safe_text = "✅ Անվտանգ է խմելու համար!"
    unsafe_text = "❌ Վտանգավոր է! Մի խմեք!"
    upload_label = "📁 Կամ վերբեռնեք CSV ֆայլ"
    download_label = "📥 Ներբեռնել արդյունքները CSV ֆորմատով"
    column_warning = "CSV ֆայլը պետք է ունենա ճիշտ 9 սյունակ։"
    success_label = "✅ Կանխատեսումը ավարտված է։"

# Title and Subtitle
st.markdown(f"<h1 style='text-align: center; font-size: 2.5em;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; font-size: 1.5em;'>{subtitle}</h3>", unsafe_allow_html=True)

# Manual Input UI
col1, col2 = st.columns(2)
with col1:
    ph = st.number_input(input_labels[0], value=0.0, step=0.1, format="%.2f")
    hardness = st.number_input(input_labels[1], value=0.0, step=1.0, format="%.2f")
    solids = st.number_input(input_labels[2], value=0.0, step=1.0, format="%.2f")
    chloramines = st.number_input(input_labels[3], value=0.0, step=0.1, format="%.2f")
    sulfate = st.number_input(input_labels[4], value=0.0, step=1.0, format="%.2f")
with col2:
    conductivity = st.number_input(input_labels[5], value=0.0, step=1.0, format="%.2f")
    organicCarbon = st.number_input(input_labels[6], value=0.0, step=0.1, format="%.2f")
    trihalomethanes = st.number_input(input_labels[7], value=0.0, step=1.0, format="%.2f")
    turbidity = st.number_input(input_labels[8], value=0.0, step=0.1, format="%.2f")

if st.button(predict_button):
    input_values = [ph, hardness, solids, chloramines, sulfate,
                    conductivity, organicCarbon, trihalomethanes, turbidity]
    try:
        input_values_scaled = scaler.transform([input_values])
        prediction = model.predict(input_values_scaled)[0]
        if prediction == 1:
            st.success(safe_text)
        else:
            st.error(unsafe_text)
            reasons = check_unsafe_parameters(input_values, safe_thresholds, input_labels, language)
            for r in reasons:
                st.write(f"- {r}")
    except Exception as e:
        st.error(f"Prediction error: {e}")

# CSV Upload Section
st.markdown(f"### {upload_label}")
uploaded_file = st.file_uploader("", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if df.shape[1] != 9:
            st.error(column_warning)
        else:
            st.dataframe(df)
            scaled_data = scaler.transform(df)
            preds = model.predict(scaled_data)
            df['Prediction'] = ['✅ Safe' if p == 1 else '❌ Unsafe' for p in preds]
            st.success(success_label)
            st.dataframe(df)
            csv_output = df.to_csv(index=False).encode('utf-8')
            st.download_button(label=download_label, data=csv_output, file_name="results.csv", mime='text/csv')
    except Exception as e:
        st.error(f"File processing error: {e}")
