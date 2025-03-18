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
set_background("water.webp")

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
    issue_text = "Reasons why the water is unsafe:"
else:
    title = "💧 Ջրի Որակի Գուշակություն"
    subtitle = "Ստուգեք՝ ջուրը խմելու համար անվտանգ է թե ոչ։"
    input_labels = ["pH մակարդակ", "Կարծրություն", "Լուծված պինդ նյութեր", "Քլորամիններ", "Սուլֆատներ",
                    "Էլեկտրահաղորդականություն", "Օրգանական ածխածին", "Տրիալոմեթաններ", "Պղտորություն"]
    predict_button = "Կանխատեսել Ջրի Որակը"
    safe_text = "✅ Անվտանգ է խմելու համար!"
    unsafe_text = "❌ Վտանգավոր է! Մի խմեք!"
    issue_text = "Պատճառները, թե ինչու է ջուրը վտանգավոր:"

# Title and Subtitle
st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>{subtitle}</h3>", unsafe_allow_html=True)

# Create input fields
input_values = []
for label in input_labels:
    input_values.append(st.number_input(label, value=0.0))

# Define safe ranges
safe_ranges = {
    "pH Level": (6.5, 8.5),
    "Hardness": (0, 500),
    "Solids": (0, 1000),
    "Chloramines": (0, 4),
    "Sulfate": (0, 250),
    "Conductivity": (0, 500),
    "Organic Carbon": (0, 5),
    "Trihalomethanes": (0, 80),
    "Turbidity": (0, 5)
}

# Predict button
if st.button(predict_button):
    prediction = model.predict([input_values])[0]
    reasons = []

    # Check which parameters are unsafe
    for i, label in enumerate(input_labels):
        min_val, max_val = safe_ranges[label]
        if not (min_val <= input_values[i] <= max_val):
            reasons.append(f"{label} is out of range ({min_val}-{max_val})")

    # Display result
    if prediction == 1:
        st.success(safe_text)
        st.image("21111safewater.gif", width=500)
        st.markdown(
            f"<p style='font-size: 20px; font-weight: bold; text-align: center;'>"
            f"<span style='background-color: rgba(0, 0, 0, 0.5); padding: 5px; border-radius: 3px;'>{safe_text}</span>"
            "</p>",
            unsafe_allow_html=True
        )
    else:
        st.error(unsafe_text)
        st.image("unsafe2.gif", width=500)
        st.markdown(
            f"<p style='font-size: 20px; font-weight: bold; text-align: center;'>"
            f"<span style='background-color: rgba(0, 0, 0, 0.5); padding: 5px; border-radius: 3px;'>{unsafe_text}</span>"
            "</p>",
            unsafe_allow_html=True
        )
        if reasons:
            styled_text = f"""
            <div style="text-align: center; font-size: 24px; font-weight: bold; color: red;
                        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.7);">
                {issue_text}
            </div>
            """
            st.markdown(styled_text, unsafe_allow_html=True)
        
            reason_list = "".join([
                f"<li style='font-size: 22px; color: white; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);'>{reason}</li>" 
                for reason in reasons
            ])
            reason_html = f"<ul style='text-align: center; list-style-position: inside;'>{reason_list}</ul>"
            
            st.markdown(reason_html, unsafe_allow_html=True)
