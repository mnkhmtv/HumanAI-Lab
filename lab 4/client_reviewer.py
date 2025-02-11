import streamlit as st
import requests
from PIL import Image
import base64
from io import BytesIO

GET_REPORTS_URL = "http://localhost:8000/reports/"
REVIEW_REPORT_URL = "http://localhost:8000/review_report/"

st.title("Review Reports")

# Initialize session state variables if not set
if "reports" not in st.session_state:
    st.session_state.reports = []

if "review_choices" not in st.session_state:
    st.session_state.review_choices = {}

# Load reports when the button is clicked, and clear previous reports
if st.button("Load Reports"):
    # Clear existing reports before fetching new ones
    st.session_state.reports = []

    # TODO: load reports into st.session_state.reports 

# Show reports if they exist
if st.session_state.reports:
    for report_id, report_data in st.session_state.reports.items():
        st.write(f"Report ID: {report_id}")
        st.write(f"Reported Label: {report_data['label']}")

        # Decode base64 image
        image_data = base64.b64decode(report_data["image"])
        image = Image.open(BytesIO(image_data))
        st.image(image, caption="Reported Image", use_container_width=True)

        review_option = st.radio(
            f"Is this report correct? ({report_id})",
            ["True", "False"],
            key=report_id,
        )
        st.session_state.review_choices[report_id] = review_option

        if st.button(f"Submit Review ({report_id})"):
            ...
            # TODO: review a report