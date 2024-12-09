import streamlit as st

def login():
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        if username == 'user' and password == 'password':
            st.success('Logged in successfully!')
        else:
            st.error('Invalid username or password')

def main():
    st.title('User Login')
    login()

if __name__ == '__main__':
    main()