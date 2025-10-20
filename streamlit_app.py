import streamlit as st
import requests
from bs4 import BeautifulSoup

# Rest of the simple code...

st.set_page_config(
    page_title="URL Scraper & File Analyzer",
    page_icon="🌐",
    layout="wide"
)

def main():
    st.title("🌐 URL Scraper + File Analyzer")
    st.success("App is working! Now adding features...")
    
    # Simple URL input
    st.header("Step 1: Enter URLs")
    url = st.text_input("Website URL")
    if url:
        st.info(f"URL entered: {url}")
    
    # Simple file upload
    st.header("Step 2: Upload Files")
    uploaded_file = st.file_uploader("Choose a file", type=['txt'])
    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")

if __name__ == "__main__":
    main()
