import streamlit as st
import requests

def github_css(url):
    """Load CSS from a GitHub-hosted file."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        st.markdown(f"<style>{response.text}</style>", unsafe_allow_html=True)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load CSS from GitHub: {e}")

# URL of the CSS file on GitHub (raw URL)
github_css("https://github.com/jaisai2512/frontend/blob/main/style.css")

# Set page layout
st.set_page_config(layout="wide")

# Create a sidebar for file upload
st.sidebar.header("Upload Your File")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv"])

# Display content on the main page
st.title("File Upload and Display")

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    # Display file details
    st.write("### File Details:")
    file_details = {
        "Filename": uploaded_file.name,
        "Filetype": uploaded_file.type,
        "Filesize (KB)": uploaded_file.size / 1024,
    }
    st.json(file_details)

    # Read and display content if it's a text-based file
    try:
        if uploaded_file.type == "text/csv":
            import pandas as pd

            df = pd.read_csv(uploaded_file)
            st.write("### Preview of Uploaded CSV File:")
            st.dataframe(df)
        elif uploaded_file.type == "application/json":
            import json

            content = json.load(uploaded_file)
            st.write("### Content of Uploaded JSON File:")
            st.json(content)
        elif uploaded_file.type == "text/plain":
            content = uploaded_file.read().decode("utf-8")
            st.write("### Content of Uploaded Text File:")
            st.text(content)
        elif "spreadsheet" in uploaded_file.type:
            import pandas as pd

            df = pd.read_excel(uploaded_file)
            st.write("### Preview of Uploaded Excel File:")
            st.dataframe(df)
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
else:
    st.info("Please upload a file from the sidebar to view its content.")
