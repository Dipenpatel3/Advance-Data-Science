import streamlit as st
from git import Repo
import os
import shutil

# Function to clone or pull the repository
def clone_or_pull_repo(repo_url, local_path):
    try:
        if not os.path.exists(local_path):
            # Clone repository if it doesn't exist locally
            Repo.clone_from(repo_url, local_path)
            return f"Repository cloned to {local_path}"
        else:
            # Pull latest changes if the repository exists
            repo = Repo(local_path)
            origin = repo.remote(name="origin")
            origin.pull()
            return f"Repository updated at {local_path}"
    except Exception as e:
        return f"An error occurred during cloning or pulling: {e}"

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

# Function to clean up the local repository
def cleanup_local_repo(local_path):
    try:
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
            return f"Local repository at {local_path} deleted successfully."
        else:
            return "Local repository not found for cleanup."
    except Exception as e:
        return f"An error occurred during cleanup: {e}"

# Streamlit UI
st.title("Automated GitHub Commit App with Cleanup")

# Input field for repository URL
repo_url = st.text_input("Enter GitHub Repository URL")
file_name = st.text_input("File Name (e.g., app.py)")
commit_message = st.text_input("Commit Message")

# Code editor
st.subheader("Code Editor")
code_content = st.text_area("Write or edit your code below:", height=300, value="# Your Python code here\n")

# Button to clone, save, commit, and push
if st.button("Save, Commit, and Push"):
    with st.spinner("Processing..."):
        if not repo_url:
            st.error("Please provide a valid GitHub repository URL.")
        else:
            # Step 1: Define the local path based on the repository name
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            local_repo_path = os.path.join(os.getcwd(), repo_name)

            # Step 2: Clone or pull the repository
            clone_result = clone_or_pull_repo(repo_url, local_repo_path)

            # Step 3: Write the code to a file
            if "cloned" in clone_result or "updated" in clone_result:
                write_result = write_code_to_file(local_repo_path, file_name, code_content)

                # Step 4: Commit and push changes
                if "written" in write_result.lower():
                    commit_result = commit_and_push(local_repo_path, commit_message)
                else:
                    commit_result = write_result
            else:
                commit_result = clone_result

            # Step 5: Cleanup local repository
            cleanup_result = cleanup_local_repo(local_repo_path)

        # Display results
        if "successfully" in commit_result.lower():
            st.success(commit_result)
            # st.info(cleanup_result)
        else:
            st.error(commit_result)
            st.warning(cleanup_result)
# Your Python code here