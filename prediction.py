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
set_background("vedrana-filipovic-ohrhLVISJ1o-unsplash.jpg")

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
    about_title = "### About This App"
    about_text = "##### This app predicts water quality based on various parameters. Use the inputs to enter values and click 'Predict Water Quality' to see the result."
    footer_text = "##### Made by Manan Mkrtchyan"
else:
    title = "💧 Ջրի Որակի Գուշակություն"
    subtitle = "Ստուգեք՝ ջուրը խմելու համար անվտանգ է թե ոչ։"
    input_labels = ["pH մակարդակ", "Կարծրություն", "Լուծված պինդ նյութեր", "Քլորամիններ", "Սուլֆատներ",
                    "Էլեկտրահաղորդականություն", "Օրգանական ածխածին", "Տրիալոմեթաններ", "Պղտորություն"]
    predict_button = "Կանխատեսել Ջրի Որակը"
    safe_text = "✅ Անվտանգ է խմելու համար!"
    unsafe_text = "❌ Վտանգավոր է! Մի խմեք!"
    issue_text = "Պատճառները, թե ինչու է ջուրը վտանգավոր:"
    about_title = "### Այս Հավելվածի Մասին"
    about_text = "##### Այս հավելվածը կանխատեսում է ջրի որակը՝ հիմնվելով տարբեր պարամետրերի վրա։ Մուտքագրեք տվյալները և սեղմեք «Կանխատեսել Ջրի Որակը»՝ արդյունքը տեսնելու համար։"
    footer_text = "##### Ստեղծվել է Մանան Մկրտչյանի կողմից"

# Title and Subtitle
st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>{subtitle}</h3>", unsafe_allow_html=True)

# Create input fields
input_values = []
for label in input_labels:
    input_values.append(st.number_input(label, value=0.0))

# Define safe ranges (use keys matching exactly with the input labels)
safe_ranges = {
    "pH Level": (6.5, 8.5),
    "Hardness": (0, 500),
    "Solids": (0, 1000),
    "Chloramines": (0, 4),
    "Sulfate": (0, 250),
    "Conductivity": (0, 500),
    "Organic Carbon": (0, 5),
    "Trihalomethanes": (0, 80),
    "Turbidity": (0, 5),
    "pH մակարդակ": (6.5, 8.5),
    "Կարծրություն": (0, 500),
    "Լուծված պինդ նյութեր": (0, 1000),
    "Քլորամիններ": (0, 4),
    "Սուլֆատներ": (0, 250),
    "Էլեկտրահաղորդականություն": (0, 500),
    "Օրգանական ածխածին": (0, 5),
    "Տրիալոմեթաններ": (0, 80),
    "Պղտորություն": (0, 5)
}

# Predict button
if st.button(predict_button):
    prediction = model.predict([input_values])[0]
    reasons = []

    # Check which parameters are unsafe
   for i, label in enumerate(input_labels):
        min_val, max_val = safe_ranges[label]
        if not (min_val <= input_values[i] <= max_val):
            if language == "English":
                reasons.append(f"{label} is out of range ({min_val}-{max_val})")
            else:
                # Armenian translation for out of range messages
                if label == "pH Level":
                    reasons.append(f"pH մակարդակը դուրս է սահմաններից ({min_val}-{max_val})")
                elif label == "Hardness":
                    reasons.append(f"Կարծրությունը դուրս է սահմաններից ({min_val}-{max_val})")
                elif label == "Solids":
                    reasons.append(f"Լուծված պինդ նյութերը դուրս են սահմաններից ({min_val}-{max_val})")
                elif label == "Chloramines":
                    reasons.append(f"Քլորամինները դուրս են սահմաններից ({min_val}-{max_val})")
                elif label == "Sulfate":
                    reasons.append(f"Սուլֆատները դուրս են սահմաններից ({min_val}-{max_val})")
                elif label == "Conductivity":
                    reasons.append(f"Էլեկտրահաղորդականությունը դուրս է սահմաններից ({min_val}-{max_val})")
                elif label == "Organic Carbon":
                    reasons.append(f"Օրգանական ածխածինը դուրս է սահմաններից ({min_val}-{max_val})")
                elif label == "Trihalomethanes":
                    reasons.append(f"Տրիալոմեթանները դուրս են սահմաններից ({min_val}-{max_val})")
                elif label == "Turbidity":
                    reasons.append(f"Պղտորությունը դուրս է սահմաններից ({min_val}-{max_val})")

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
            <div style="text-align: center; font-size: 22px; font-weight: bold; color: red;">
                {issue_text}
            </div>
            """
            st.markdown(styled_text, unsafe_allow_html=True)

            reason_list = "".join([f"<li style='font-size: 20px; color: white;'>{reason}</li>" for reason in reasons])
            reason_html = f"<ul style='text-align: center; list-style-position: inside;'>{reason_list}</ul>"

            st.markdown(reason_html, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(about_title)
st.markdown(about_text)
st.markdown(footer_text)
