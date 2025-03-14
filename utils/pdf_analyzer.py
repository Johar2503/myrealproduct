import google.generativeai as genai
import json
import os

def analyze_pdf_with_gemini(text_content):
    """
    Analyze bill text content using Gemini API
    """
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: API configuration is missing. Please contact support."

        # Configure model
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')

        # Prepare the prompt
        prompt = f"""
        Analyze this phone bill text and extract the following information:
        1. Number of active lines
        2. Data usage per line
        3. Current plan details
        4. Monthly charges
        5. Any additional services (Netflix, Apple TV, etc.)

        Here's the bill text:
        {text_content}

        Provide a structured analysis that can be used to recommend a better plan.
        """

        # Get response from Gemini
        response = model.generate_content(prompt)

        if response.text:
            # Load available plans for comparison
            with open('data/plans.json', 'r') as f:
                plans = json.load(f)

            # Add plan recommendations based on the analysis
            final_response = f"""
            Bill Analysis:
            {response.text}

            Based on the analysis, here are potential plan recommendations:
            """

            return final_response
        else:
            return "Error: Could not generate analysis. Please try again."

    except Exception as e:
        return f"Error: Failed to analyze bill: {str(e)}"