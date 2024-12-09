import streamlit as st

def login(username, password):
    # Check if username and password are correct
    if username == "admin" and password == "password":
        return True
    else:
        return False

def main():
    st.title("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()