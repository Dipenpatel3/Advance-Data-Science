import streamlit as st

def login(username, password):
    # You can add your login logic here
    if username == "admin" and password == "password":
        return True
    else:
        return False

st.title("User Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if login(username, password):
        st.success("Login successful!")
    else:
        st.error("Invalid username or password")