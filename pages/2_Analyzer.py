import streamlit as st
import os
import json
from recommend_plan import recommend_plan
from utils.pdf_analyzer import analyze_pdf_with_gemini
import PyPDF2

# Check authentication
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    st.stop()

# Page config
st.title("Plan Analyzer")

# Create tabs for different analysis methods
tab1, tab2 = st.tabs(["Manual Input", "Bill Upload"])

with tab1:
    st.header("Manual Plan Analysis")

    # Form inputs
    with st.form("plan_form"):
        num_lines = st.number_input("Number of active phone lines", 
                                min_value=1, max_value=4, value=1)

        premium_data = st.number_input("Premium data needed (GB)", 
                                    min_value=0, value=50)

        apple_tv_netflix = st.selectbox(
            "Apple TV/Netflix subscription needed?",
            options=["yes", "no", "conditions"]
        )

        upgrade_ready = st.selectbox(
            "Device upgrade status",
            options=["no", "1", "2"]
        )

        hulu_ads = st.selectbox(
            "Hulu with ads?",
            options=["yes", "no"]
        )

        submit_button = st.form_submit_button("Analyze Plan Options")

    if submit_button:
        with st.spinner("Analyzing plans..."):
            try:
                st.subheader("Recommendations")
                recommendation = recommend_plan(
                    num_lines, 
                    premium_data, 
                    apple_tv_netflix, 
                    upgrade_ready, 
                    hulu_ads
                )
                st.success(recommendation)
            except Exception as e:
                st.error(f"Error analyzing plans: {str(e)}")

with tab2:
    st.header("Bill Upload Analysis")
    uploaded_file = st.file_uploader("Upload your phone bill (PDF)", type="pdf")

    if uploaded_file:
        with st.spinner("Analyzing your bill..."):
            try:
                # Read PDF content
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text()

                if not text_content.strip():
                    st.error("Could not extract text from the PDF. Please ensure it's not scanned or protected.")
                    st.stop()

                # Analyze with Gemini
                st.subheader("Bill Analysis")
                analysis_result = analyze_pdf_with_gemini(text_content)
                if analysis_result.startswith("Error:"):
                    st.error(analysis_result)
                else:
                    st.write(analysis_result)

            except Exception as e:
                st.error(f"Error processing the bill: {str(e)}")
