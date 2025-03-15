# Standard library imports
import os
import hashlib
import json
import io

# Third-party imports
import streamlit as st
import google.generativeai as genai
import pandas as pd
import PyPDF2
from dotenv import load_dotenv
import boto3


# ======================
# Configuration Settings
# ======================

# Load environment variables from .env file
load_dotenv()

# Configure Google's Generative AI (Gemini) with API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Configure AWS S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION'),
    verify=True,  # Enable SSL verification
    use_ssl=True,  # Use SSL/TLS for connections
    config=boto3.session.Config(
        signature_version='s3v4',
        retries={'max_attempts': 3},
    )
)
S3_BUCKET = os.getenv('S3_BUCKET_NAME')
S3_USERS_KEY = 'users/credentials.json'

# ======================
# Security Functions
# ======================

def hash_password(password: str) -> str:
    """
    Convert a plain text password into a hashed version using SHA-256.

    Args:
        password (str): The plain text password to hash

    Returns:
        str: The hexadecimal representation of the hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()

# ======================
# S3 Utility Functions
# ======================

def get_users_from_s3() -> dict:
    """
    Load user credentials from S3.
    
    Returns:
        dict: Dictionary containing username-password pairs
    """
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_USERS_KEY)
        users_data = json.loads(response['Body'].read().decode('utf-8'))
        return users_data
    except s3_client.exceptions.NoSuchKey:
        # If file doesn't exist, return empty dict
        return {}
    except Exception as e:
        st.error(f"Error accessing S3: {str(e)}")
        return {}

def save_users_to_s3(users_data: dict) -> bool:
    """
    Save user credentials to S3.
    
    Args:
        users_data (dict): Dictionary containing username-password pairs
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        users_json = json.dumps(users_data)
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=S3_USERS_KEY,
            Body=users_json
        )
        return True
    except Exception as e:
        st.error(f"Error saving to S3: {str(e)}")
        return False

# ======================
# User Management Functions
# ======================

def save_user(username: str, password: str) -> bool:
    """
    Save a new user with a hashed password to S3.

    Args:
        username (str): The user's chosen username
        password (str): The user's plain text password (will be hashed before saving)
        
    Returns:
        bool: True if successful, False otherwise
    """
    users = get_users_from_s3()
    if username not in users:
        users[username] = hash_password(password)
        return save_users_to_s3(users)
    return False

def authenticate(username: str, password: str) -> bool:
    """
    Verify user credentials against S3 stored credentials.

    Args:
        username (str): The username to verify
        password (str): The plain text password to verify

    Returns:
        bool: True if credentials are valid, False otherwise
    """
    users = get_users_from_s3()
    hashed_password = hash_password(password)
    return username in users and users[username] == hashed_password


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
