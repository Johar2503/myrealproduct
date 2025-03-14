import streamlit as st
import sqlite3
import bcrypt


st.markdown(
    """
    <style>
    body {
        background-color: #D0E9F6;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Function to verify passwords
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# Function to create user table
def create_user_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)")
    conn.commit()
    conn.close()

# Function to add a new user
def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        st.success("Account created successfully! Please login.")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Choose a different one.")
    conn.close()

# Function to validate user credentials
def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user and verify_password(password, user[0]):
        return True
    return False

# Initialize session state for login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

st.title("Login / Signup System")
create_user_table()

if not st.session_state.authenticated:
    menu = ["Signup","Login"]
    choice = st.sidebar.selectbox("Menu", menu)

    # if choice == "Signup":
    #     st.subheader("Create New Account")
    #     new_user = st.text_input("Username")
    #     new_password = st.text_input("Password", type='password')
        
    #     if st.button("Signup"):
    #         if new_user and new_password:
    #             add_user(new_user, new_password)
    #         else:
    #             st.error("Please fill in all fields.")

    if choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            if validate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.page = "dashboard"

            else:
                st.error("Invalid Username or Password")

    elif choice == "Signup":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        
        if st.button("Signup"):
            if new_user and new_password:
                add_user(new_user, new_password)
            else:
                st.error("Please fill in all fields.")
    
else:
    # Redirect to another Streamlit page dynamically
    st.success(f"Welcome {st.session_state.username}!")
    st.switch_page("pages/dashboard.py")  # Ensure the dashboard script is in pages/
