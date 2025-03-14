import streamlit as st

# Page config
st.set_page_config(page_title="SmartBill Connect",
                   page_icon="📱",
                   layout="wide")

# Initialize session state if not exists
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

# Redirect to landing page
st.title("📱 SmartBill Connect")
st.markdown("Welcome to SmartBill Connect!")
st.switch_page("pages/1_Landing.py")
