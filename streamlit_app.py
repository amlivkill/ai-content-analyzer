import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="AI Content Analyzer",
    page_icon="🔍",
    layout="wide"
)

def main():
    st.title("🔍 AI Content Analyzer")
    st.markdown("Upload files for analysis - URL features coming soon!")
    
    # File upload
    uploaded_files = st.file_uploader(
        "Choose CSV, TXT files",
        type=['csv', 'txt'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
        
        for file in uploaded_files:
            with st.expander(f"📄 {file.name}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Type:** {file.type}")
                    st.write(f"**Size:** {file.size / 1024:.1f} KB")
                
                with col2:
                    if st.button(f"Analyze {file.name}", key=file.name):
                        # Simple analysis for CSV files
                        if file.type == "text/csv":
                            df = pd.read_csv(file)
                            st.write("**Data Preview:**")
                            st.dataframe(df.head())
                            
                            st.write("**Basic Statistics:**")
                            st.write(f"- Rows: {len(df)}")
                            st.write(f"- Columns: {len(df.columns)}")
                            st.write(f"- Column names: {', '.join(df.columns)}")
                        
                        # Simple analysis for TXT files
                        elif file.type == "text/plain":
                            content = file.read().decode("utf-8")
                            st.write("**Text Analysis:**")
                            st.write(f"- Characters: {len(content)}")
                            st.write(f"- Words: {len(content.split())}")
                            st.write(f"- Lines: {len(content.splitlines())}")
                        
                        st.success("✅ Basic analysis completed!")

    # Coming soon message for URLs
    st.markdown("---")
    st.info("🌐 **URL Analysis Feature** - Coming soon in the next update!")

if __name__ == "__main__":
    main()
