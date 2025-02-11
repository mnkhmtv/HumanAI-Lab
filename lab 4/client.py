import streamlit as st
import requests
from PIL import Image
from io import BytesIO

API_URL = "http://localhost:8000/predict/"
REPORT_URL = "http://localhost:8000/report/"

st.title("Cat vs Dog Classifier")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert image to bytes
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()

    # Send to FastAPI server
    with st.spinner("Classifying..."):
        response = requests.post(
            API_URL, files={"file": (uploaded_file.name, img_bytes, uploaded_file.type)}
        )

    if response.status_code == 200:
        result = response.json()
        label, confidence = result["label"], result["confidence"]

        st.write(f"### Prediction: {label} ({confidence:.2f} confidence)")

        if confidence < 0.6:
            st.write("There might be neither a dog nor a cat in the image.")

        # Reporting feature
        st.write("### Report Incorrect Classification")
        report_option = st.selectbox(
            "What should the correct label be?", ["Cat", "Dog", "Neither"]
        )

        if st.button("Report"):
            ...
            # TODO: report an image