import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import base64

# Set page configuration
st.set_page_config(page_title="Water Quality Prediction", page_icon="💧", layout="wide")


# Background image and custom CSS
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
    .parameter-display {{
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }}
    .unsafe-reason {{
        background-color: rgba(139, 0, 0, 0.7);
        padding: 8px;
        border-radius: 6px;
        margin: 5px 0;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)


# Set background
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

english_to_armenian = {v: k for k, v in armenian_to_english.items()}


# Unsafe reason checker with proper Armenian parameter names
def check_unsafe_parameters(input_values, safe_thresholds, input_labels, language):
    unsafe_parameters = []
    for i, (param, value) in enumerate(zip(input_labels, input_values)):
        param_key = armenian_to_english.get(param, param)
        label = param if language == "Հայերեն" else param_key
        if param_key in safe_thresholds:
            thresholds = safe_thresholds[param_key]
            if "min" in thresholds and value < thresholds["min"]:
                param_name = english_to_armenian.get(param_key, param_key) if language == "Հայերեն" else param_key
                reason = f"{param_name} շատ ցածր է (նվազագույն՝ {thresholds['min']}, ձեր արժեքը՝ {value:.2f})" if language == "Հայերեն" else f"{param_name} is too low (min: {thresholds['min']}, your value: {value:.2f})"
                unsafe_parameters.append(reason)
            if "max" in thresholds and value > thresholds["max"]:
                param_name = english_to_armenian.get(param_key, param_key) if language == "Հայերեն" else param_key
                reason = f"{param_name} շատ բարձր է (առավելագույն՝ {thresholds['max']}, ձեր արժեքը՝ {value:.2f})" if language == "Հայերեն" else f"{param_name} is too high (max: {thresholds['max']}, your value: {value:.2f})"
                unsafe_parameters.append(reason)
    return unsafe_parameters


# Language selection
language = st.radio("🌍 Select Language / Ընտրեք Լեզուն", ("English", "Հայերեն"), horizontal=True)

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
    manual_download_label = "📥 Download Manual Results"
    column_warning = "Error: CSV must contain exactly 9 numeric columns"
    numeric_warning = "Error: All values must be numbers"
    file_error = "File processing error. Please check:"
    file_requirements = [
        "- Exactly 9 columns",
        "- Numeric values only",
        "- UTF-8 or Latin-1 encoding",
        "- No header row or matching column names"
    ]
    potability_col_name = "Potability"
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
    manual_download_label = "📥 Ներբեռնել Ձեռքով Մուտքագրված Արդյունքները"
    column_warning = "Սխալ․ CSV ֆայլը պետք է պարունակի ճիշտ 9 թվային սյունակ"
    numeric_warning = "Սխալ․ Բոլոր արժեքները պետք է լինեն թվեր"
    file_error = "Ֆայլի մշակման սխալ։ Ստուգեք՝"
    file_requirements = [
        "- Ճիշտ 9 սյունակ",
        "- Միայն թվային արժեքներ",
        "- UTF-8 կամ Latin-1 կոդավորում",
        "- Առանց վերնագրի տողի կամ համապատասխան սյունակների անունների"
    ]
    potability_col_name = "Պիտանիություն"

# Title and Subtitle
st.markdown(f"<h1 style='text-align: center; font-size: 2.5em;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; font-size: 1.5em;'>{subtitle}</h3>", unsafe_allow_html=True)

# Manual Input UI with black background
col1, col2 = st.columns(2)
with col1:
    with st.container():
        st.markdown('<div class="parameter-display">', unsafe_allow_html=True)
        ph = st.number_input(input_labels[0], value=0.0, step=0.1, format="%.2f")
        hardness = st.number_input(input_labels[1], value=0.0, step=1.0, format="%.2f")
        solids = st.number_input(input_labels[2], value=0.0, step=1.0, format="%.2f")
        chloramines = st.number_input(input_labels[3], value=0.0, step=0.1, format="%.2f")
        sulfate = st.number_input(input_labels[4], value=0.0, step=1.0, format="%.2f")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="parameter-display">', unsafe_allow_html=True)
        conductivity = st.number_input(input_labels[5], value=0.0, step=1.0, format="%.2f")
        organicCarbon = st.number_input(input_labels[6], value=0.0, step=0.1, format="%.2f")
        trihalomethanes = st.number_input(input_labels[7], value=0.0, step=1.0, format="%.2f")
        turbidity = st.number_input(input_labels[8], value=0.0, step=0.1, format="%.2f")
        st.markdown('</div>', unsafe_allow_html=True)

manual_results = None

if st.button(predict_button):
    input_values = [ph, hardness, solids, chloramines, sulfate,
                    conductivity, organicCarbon, trihalomethanes, turbidity]
    try:
        input_values_scaled = scaler.transform([input_values])
        prediction = model.predict(input_values_scaled)[0]

        # Create a DataFrame for the manual input results
        manual_results = pd.DataFrame([input_values], columns=input_labels)
        manual_results[potability_col_name] = [prediction]

        if prediction == 1:
            st.success(safe_text)
        else:
            st.error(unsafe_text)
            reasons = check_unsafe_parameters(input_values, safe_thresholds, input_labels, language)
            for r in reasons:
                st.markdown(f'<div class="unsafe-reason">- {r}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Prediction error: {e}")

# Add download button for manual results if available
if manual_results is not None:
    # Convert to Armenian column names if needed
    if language == "Հայերեն":
        manual_results.columns = [english_to_armenian.get(col, col) for col in manual_results.columns[:-1]] + [
            potability_col_name]

    csv_output = manual_results.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button(
        label=manual_download_label,
        data=csv_output,
        file_name="manual_water_quality_results.csv",
        mime='text/csv'
    )

# CSV Upload Section
st.markdown(f"### {upload_label}")
uploaded_file = st.file_uploader(upload_help, type=["csv"])

if uploaded_file is not None:
    try:
        # Attempt to read CSV with explicit encoding
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='utf-8')

        # Validate shape
        if df.shape[1] != 9:
            st.error(column_warning)
            st.stop()

        # Validate numeric
        if not all([pd.api.types.is_numeric_dtype(df[col]) for col in df.columns]):
            st.error(numeric_warning)
            st.stop()

        # Save original column names for reasons
        original_columns = df.columns.tolist()
        mapped_columns = [armenian_to_english.get(col, col) for col in original_columns]
        df.columns = mapped_columns

        # Predict
        scaled_data = scaler.transform(df)
        preds = model.predict(scaled_data)

        # Show results row by row with Armenian display
        for i, row in df.iterrows():
            # Display parameters with black background
            with st.container():
                st.markdown('<div class="parameter-display">', unsafe_allow_html=True)
                row_display = ", ".join([f"{original_columns[j]}: {row[mapped_columns[j]]:.2f}" for j in range(9)])
                st.markdown(f"**{i + 1}.** {row_display}")
                st.markdown('</div>', unsafe_allow_html=True)

                if preds[i] == 1:
                    st.success(safe_text)
                else:
                    st.error(unsafe_text)
                    reasons = check_unsafe_parameters(row.values, safe_thresholds, original_columns, language)
                    for reason in reasons:
                        st.markdown(f'<div class="unsafe-reason">- {reason}</div>', unsafe_allow_html=True)
                st.markdown("---")

        # Final DataFrame for download with proper encoding
        download_df = df.copy()
        download_df[potability_col_name] = preds  # 0 or 1 values

        # Convert back to Armenian column names if needed
        if language == "Հայերեն":
            reverse_column_map = {
                "pH Level": "pH մակարդակ/թթվայնություն",
                "Hardness": "Կարծրություն",
                "Solids": "Լուծված պինդ նյութեր",
                "Chloramines": "Քլորամիններ",
                "Sulfate": "Սուլֆատներ",
                "Conductivity": "Էլեկտրահաղորդականություն",
                "Organic Carbon": "Օրգանական ածխածին",
                "Trihalomethanes": "Տրիալոմեթաններ",
                "Turbidity": "Պղտորություն"
            }
            download_df.columns = [reverse_column_map.get(col, col) for col in download_df.columns[:-1]] + [
                potability_col_name]

        # Ensure proper encoding for Armenian characters in CSV
        csv_output = download_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
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
