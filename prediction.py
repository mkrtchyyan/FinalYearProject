import streamlit as st
import joblib
import base64

# Load the model
model = joblib.load("svm.pkl")

# Set page configuration
st.set_page_config(page_title="Water Quality Prediction", page_icon="💧", layout="wide")

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
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# Set background image
set_background("water-839590_1280.jpg")

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
    about_title = "### About This App"
    about_text = "##### This app predicts water quality based on various parameters. Use the inputs to enter values and click 'Predict Water Quality' to see the result."
    footer_text = "##### Made by Manan Mkrtchyan"
else:
    title = "💧 Ջրի Որակի Գուշակություն"
    subtitle = "Ստուգեք՝ ջուրը խմելու համար անվտանգ է թե ոչ։"
    input_labels = ["pH մակարդակ/թթվայնություն", "Կարծրություն", "Լուծված պինդ նյութեր", "Քլորամիններ", "Սուլֆատներ",
                    "էլեկտրահաղորդականություն", "Օրգանական ածխածին", "Տրիալոմեթաններ", "պղտորություն"]
    predict_button = "Կանխատեսել Ջրի Որակը"
    safe_text = "✅ Անվտանգ է խմելու համար!"
    unsafe_text = "❌ Վտանգավոր է! Մի խմեք!"
    about_title = "### Այս Հավելվածի Մասին"
    about_text = "##### Այս հավելվածը կանխատեսում է ջրի որակը՝ հիմնվելով տարբեր պարամետրերի վրա։ Մուտքագրեք տվյալները և սեղմեք «Կանխատեսել Ջրի Որակը»՝ արդյունքը տեսնելու համար։"
    footer_text = "##### Ստեղծվել է Մանան Մկրտչյանի կողմից"

# Title and Subtitle
st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>{subtitle}</h3>", unsafe_allow_html=True)

# Create input fields in columns
col1, col2 = st.columns(2)

with col1:
    ph = st.number_input(input_labels[0], value=0.29)
    hardness = st.number_input(input_labels[1], value=1.23)
    solids = st.number_input(input_labels[2], value=-0.03)
    chloramines = st.number_input(input_labels[3], value=-0.33)
    sulfate = st.number_input(input_labels[4], value=2.03)

with col2:
    conductivity = st.number_input(input_labels[5], value=-1.57)
    organicCarbon = st.number_input(input_labels[6], value=1.95)
    trihalomethanes = st.number_input(input_labels[7], value=0.12)
    turbidity = st.number_input(input_labels[8], value=0.35)

# Predict button
if st.button(predict_button):
    input_values = [ph, hardness, solids, chloramines, sulfate, conductivity, organicCarbon, trihalomethanes, turbidity]

    # Make prediction
    prediction = model.predict([input_values])[0]
    prediction_text = safe_text if prediction == 1 else unsafe_text

    # Display result
    if prediction == 1:
        st.success(prediction_text)
    else:
        st.error(prediction_text)

    # Add animation or GIF
    if prediction == 1:
        st.image("21111safewater.gif", width=500)
        st.markdown(
            f"<p style='font-size: 20px; font-weight: bold; text-align: center;'>"
            f"<span style='background-color: rgba(0, 0, 0, 0.5); padding: 5px; border-radius: 3px;'>{safe_text}</span>"
            "</p>",
            unsafe_allow_html=True
        )
    else:
        st.image("unsafe2.gif", width=500)
        st.markdown(
            f"<p style='font-size: 20px; font-weight: bold; text-align: center;'>"
            f"<span style='background-color: rgba(0, 0, 0, 0.5); padding: 5px; border-radius: 3px;'>{unsafe_text}</span>"
            "</p>",
            unsafe_allow_html=True
        )

# Footer
st.markdown("---")
st.markdown(about_title)
st.markdown(about_text)
st.markdown(footer_text)
