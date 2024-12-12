import streamlit as st
from backend import generate_code, get_openai_key

# Sidebar for OpenAI API Key
st.sidebar.header('Settings')
openai_key = st.sidebar.text_input('OpenAI API Key', type='password')

# Main application title
st.title('Code Generation Assistant')

# User input for requirements
user_input = st.text_area('Enter your programming requirements:')

if st.button('Generate Code'):
    if openai_key:
        # Call the backend function to generate code
        code, documentation, explanation = generate_code(user_input, openai_key)
        st.subheader('Generated Code')
        st.code(code, language='python')
        st.subheader('Documentation')
        st.write(documentation)
        st.subheader('Explanation')
        st.write(explanation)
    else:
        st.error('Please enter your OpenAI API Key.')