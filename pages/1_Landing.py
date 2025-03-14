import streamlit as st
import sqlite3
import bcrypt
import os
from recommend_plan import recommend_plan


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_user_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)"
    )
    conn.commit()
    conn.close()


def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(username, password) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        st.success("Account created successfully! Please login.")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Choose a different one.")
    conn.close()


def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username, ))
    user = c.fetchone()
    conn.close()
    if user and verify_password(password, user[0]):
        return True
    return False


# Check if user is not authenticated
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

st.title("📱 SmartBill Connect")

if not st.session_state.authenticated:
    st.markdown("""
    Welcome to SmartBill Connect! This app helps you:
    - Find the best phone plan for your needs
    - Compare your current plan with available options
    - Analyze your phone bill automatically
    - Get personalized recommendations based on your usage

    Please login or signup to continue.
    """)

    # Login/Signup tabs
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", key="login_button"):
            if validate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()  # Use st.rerun() instead of experimental_rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Create New Account")
        new_username = st.text_input("Username", key="signup_user")
        new_password = st.text_input("Password",
                                     type="password",
                                     key="signup_pass")

        if st.button("Signup", key="signup_button"):
            if new_username and new_password:
                add_user(new_username, new_password)
            else:
                st.error("Please fill in all fields")

else:
    st.success(f"Welcome back, {st.session_state.username}!")
    st.markdown("""
    ### Get Started
    Use the sidebar to navigate to the Analyzer page and start comparing phone plans!
    """)

    if st.button("Logout", key="logout_button"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()  # Use st.rerun() instead of experimental_rerun()

# Initialize database
create_user_table()
