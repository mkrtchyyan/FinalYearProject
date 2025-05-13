import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import base64
from datetime import datetime
import pytz  # For timezone handling

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


# Language selection
language = st.radio("🌍 Select Language / Ընտրեք Լեզուն", ("English", "Հայերեն"))

# Country selection
country = st.selectbox(
    "🌎 Select Country / Ընտրեք Երկիրը",
    ["Armenia", "USA", "Canada", "UK", "Germany", "France", "Other"],
    index=0
)

# Localized UI content
if language == "English":
    title = "💧 Water Quality Prediction"
    subtitle = "Check if the water is safe to drink!"
    input_labels = ["pH Level", "Hardness", "Solids", "Chloramines", "Sulfate",
                    "Conductivity", "Organic Carbon", "Trihalomethanes", "Turbidity"]
    predict_button = "Predict Water Quality"
    safe_text = "✅ Safe to drink!"
    unsafe_text = "❌ Unsafe! Do not drink!"
    upload_label = "📁 Upload CSV File"
    upload_help = "Upload a CSV file with 9 columns of water quality parameters"
    download_label = "📥 Download Results"
    column_warning = "Error: CSV must contain exactly 9 numeric columns"
    numeric_warning = "Error: All values must be numbers"
    success_label = "✅ Prediction completed!"
    file_error = "File processing error. Please check:"
    file_requirements = [
        "- Exactly 9 columns",
        "- Numeric values only",
        "- UTF-8 or Latin-1 encoding",
        "- No header row or matching column names"
    ]
else:
    title = "💧 Ջրի Որակի Կանխատեսում"
    subtitle = "Ստուգեք՝ ջուրը խմելու համար անվտանգ է, թե ոչ։"
    input_labels = ["pH մակարդակ/թթվայնություն", "Կարծրություն", "Լուծված պինդ նյութեր", "Քլորամիններ", "Սուլֆատներ",
                    "Էլեկտրահաղորդականություն", "Օրգանական ածխածին", "Տրիալոմեթաններ", "Պղտորություն"]
    predict_button = "Կանխատեսել Ջրի Որակը"
    safe_text = "✅ Անվտանգ է խմելու համար!"
    unsafe_text = "❌ Վտանգավոր է! Մի խմեք!"
    upload_label = "📁 CSV Ֆայլ Վերբեռնել"
    upload_help = "Վերբեռնեք ջրի որակի 9 պարամետրեր պարունակող CSV ֆայլ"
    download_label = "📥 Արդյունքները Ներբեռնել"
    column_warning = "Սխալ․ CSV ֆայլը պետք է պարունակի ճիշտ 9 թվային սյունակ"
    numeric_warning = "Սխալ․ Բոլոր արժեքները պետք է լինեն թվեր"
    success_label = "✅ Կանխատեսումը հաջողված է!"
    file_error = "Ֆայլի մշակման սխալ։ Ստուգեք՝"
    file_requirements = [
        "- Ճիշտ 9 սյունակ",
        "- Միայն թվային արժեքներ",
        "- UTF-8 կամ Latin-1 կոդավորում",
        "- Առանց վերնագրի տողի կամ համապատասխան սյունակների անունների"
    ]

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
        
        # Create result dictionary preserving original format
        result_data = {
            input_labels[0]: [ph],
            input_labels[1]: [hardness],
            input_labels[2]: [solids],
            input_labels[3]: [chloramines],
            input_labels[4]: [sulfate],
            input_labels[5]: [conductivity],
            input_labels[6]: [organicCarbon],
            input_labels[7]: [trihalomethanes],
            input_labels[8]: [turbidity],
            'Prediction': ['✅ ' + safe_text.split('✅ ')[1] if prediction == 1 else '❌ ' + unsafe_text.split('❌ ')[1]],
            'Timestamp': [datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S %Z')],
            'Country': [country]
        }
        
        result_df = pd.DataFrame(result_data)
        
        if prediction == 1:
            st.success(safe_text)
        else:
            st.error(unsafe_text)
            reasons = check_unsafe_parameters(input_values, safe_thresholds, input_labels, language)
            for r in reasons:
                st.write(f"- {r}")
        
        st.dataframe(result_df)
        
        csv_output = result_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label=download_label,
            data=csv_output,
            file_name="water_quality_results.csv",
            mime='text/csv'
        )
        
    except Exception as e:
        st.error(f"Prediction error: {e}")


# CSV Upload Section
st.markdown(f"### {upload_label}")
uploaded_file = st.file_uploader(upload_help, type=["csv"])

if uploaded_file is not None:
    try:
        # Try multiple encodings while preserving original data
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='latin1')

        # Validate shape without modifying original data
        if df.shape[1] != 9:
            st.error(column_warning)
            st.stop()

        # Process data while keeping original columns intact
        original_columns = df.columns.tolist()
        scaled_data = scaler.transform(df)
        preds = model.predict(scaled_data)
        
        # Add new columns without modifying existing ones
        results_df = df.copy()
        results_df['Prediction'] = ['✅ ' + safe_text.split('✅ ')[1] if p == 1 else '❌ ' + unsafe_text.split('❌ ')[1] for p in preds]
        results_df['Timestamp'] = datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
        results_df['Country'] = country
        
        st.success(success_label)
        st.dataframe(results_df)

        # Download with original column names preserved
        csv_output = results_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label=download_label,
            data=csv_output,
            file_name="water_quality_results.csv",
            mime='text/csv'
        )

    except Exception as e:
        st.error(file_error)
        for req in file_requirements:
            st.error(req)
        st.error(f"Technical details: {str(e)}")
