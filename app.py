# Your Python code here
import streamlit as st
from git import Repo
import os
import shutil

# Repository details
REPO_URL = "https://github.com/Dipenpatel3/Advance-Data-Science"
LOCAL_REPO_PATH = "./Advance-Data-Science"  # Local folder for cloning the repo

# Function to clone the repository if it doesn't exist
def clone_repo(repo_url, local_path):
    try:
        if not os.path.exists(local_path):
            Repo.clone_from(repo_url, local_path)
            return f"Repository cloned to {local_path}"
        else:
            return f"Repository already exists at {local_path}"
    except Exception as e:
        return f"An error occurred during cloning: {e}"

# Function to write code to a file
def write_code_to_file(repo_path, file_name, code_content):
    try:
        file_path = os.path.join(repo_path, file_name)
        with open(file_path, "w") as file:
            file.write(code_content)
        return f"Code written to {file_path}"
    except Exception as e:
        return f"An error occurred while writing to the file: {e}"

# Function to commit and push code to GitHub
def commit_and_push(repo_path, commit_message):
    try:
        # Initialize the repository
        repo = Repo(repo_path)

        # Stage all changes
        repo.git.add(A=True)

        # Commit changes
        repo.index.commit(commit_message)

        # Push to remote repository
        origin = repo.remote(name="origin")
        origin.push()

        return "Changes committed and pushed successfully!"
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.title("Automated GitHub Commit App for Advance Data Science")

st.markdown(f"**Repository:** [{REPO_URL}]({REPO_URL})")

# File name and commit message inputs
file_name = st.text_input("File Name (e.g., app.py)", value="app.py")
commit_message = st.text_input("Commit Message", value="Updated code via Streamlit")

# Code editor
st.subheader("Code Editor")
code_content = st.text_area("Write or edit your code below:", height=300, value="# Your Python code here\n")

# Button to clone, save, commit, and push
if st.button("Save, Commit, and Push"):
    with st.spinner("Processing..."):
        # Step 1: Clone the repository
        clone_result = clone_repo(REPO_URL, LOCAL_REPO_PATH)

        # Step 2: Write the code to a file
        if "cloned" in clone_result or "exists" in clone_result:
            write_result = write_code_to_file(LOCAL_REPO_PATH, file_name, code_content)

            # Step 3: Commit and push changes
            if "written" in write_result.lower():
                commit_result = commit_and_push(LOCAL_REPO_PATH, commit_message)
            else:
                commit_result = write_result
        else:
            commit_result = clone_result

    # Display results
    if "successfully" in commit_result.lower():
        st.success(commit_result)
    else:
        st.error(commit_result)
