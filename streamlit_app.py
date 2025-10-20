import streamlit as st

st.title("🔍 AI Content Analyzer")
st.write("This is a simple version. More features coming soon!")

# File upload
uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'txt', 'csv'])
if uploaded_file:
    st.success(f"File {uploaded_file.name} uploaded!")

# URL input
url = st.text_input("Enter URL")
if url:
    st.info(f"URL added: {url}")
