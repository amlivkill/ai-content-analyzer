import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import PyPDF2
import docx
import io
import chardet
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="URL Scraper & File Analyzer",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .url-section {
        background-color: #e7f3ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .file-section {
        background-color: #f0f8f0;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def scrape_website(url):
    """Website content scrape करें"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        # Get title and content
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No Title Found"
        
        # Get main content
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        text_content = main_content.get_text(separator='\n', strip=True) if main_content else "No content found"
        
        # Clean extra whitespace
        lines = (line.strip() for line in text_content.splitlines())
        text_content = '\n'.join(line for line in lines if line)
        
        return {
            'success': True,
            'title': title_text,
            'content': text_content[:10000],  # Limit content
            'url': url,
            'content_length': len(text_content)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }

def extract_pdf_content(file):
    """PDF file से content extract करें"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return {'success': True, 'content': text, 'pages': len(pdf_reader.pages)}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def extract_txt_content(file):
    """TXT file से content extract करें"""
    try:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
        file.seek(0)
        content = file.read().decode(encoding or 'utf-8')
        return {'success': True, 'content': content}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def extract_csv_content(file):
    """CSV file से data extract करें"""
    try:
        df = pd.read_csv(file)
        return {'success': True, 'dataframe': df, 'rows': len(df), 'columns': len(df.columns)}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    st.markdown('<h1 class="main-header">🌐 URL Scraper + File Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### पहले URLs से Data Scrape करें, फिर Files Upload करें")
    
    # Initialize session state
    if 'scraped_data' not in st.session_state:
        st.session_state.scraped_data = []
    if 'uploaded_files_data' not in st.session_state:
        st.session_state.uploaded_files_data = []
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["🌐 URL Scraping", "📁 File Upload", "📊 Combined Results"])
    
    # TAB 1: URL SCRAPING
    with tab1:
        st.markdown('<div class="url-section">', unsafe_allow_html=True)
        st.header("Step 1: URLs से Data Scrape करें")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            urls_input = st.text_area(
                "URLs डालें (एक line में एक URL)",
                placeholder="https://example.com\nhttps://example.org",
                height=100
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            scrape_clicked = st.button("🚀 Scrape URLs", type="primary")
        
        if scrape_clicked and urls_input:
            urls_list = [url.strip() for url in urls_input.split('\n') if url.strip()]
            
            if urls_list:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, url in enumerate(urls_list):
                    status_text.text(f"Scraping: {url}")
                    result = scrape_website(url)
                    st.session_state.scraped_data.append(result)
                    progress_bar.progress((i + 1) / len(urls_list))
                
                status_text.text("✅ Scraping completed!")
                
                # Show results
                st.subheader("Scraping Results")
                for result in st.session_state.scraped_data:
                    if result['success']:
                        with st.expander(f"✅ {result['title']}", expanded=False):
                            st.write(f"**URL:** {result['url']}")
                            st.write(f"**Content Length:** {result['content_length']} characters")
                            st.write(f"**Preview:** {result['content'][:500]}...")
                    else:
                        st.error(f"❌ Failed: {result['url']} - {result['error']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 2: FILE UPLOAD
    with tab2:
        st.markdown('<div class="file-section">', unsafe_allow_html=True)
        st.header("Step 2: Files Upload करें")
        
        uploaded_files = st.file_uploader(
            "PDF, CSV, TXT, DOCX files select करें",
            type=['pdf', 'csv', 'txt', 'docx'],
            accept_multiple_files=True,
            help="Multiple files select कर सकते हैं"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) selected")
            
            for file in uploaded_files:
                with st.expander(f"📄 {file.name}", expanded=True):
                    st.write(f"**File Type:** {file.type}")
                    st.write(f"**Size:** {file.size / 1024:.1f} KB")
                    
                    if st.button(f"Analyze {file.name}", key=f"analyze_{file.name}"):
                        with st.spinner(f"Analyzing {file.name}..."):
                            
                            # Process based on file type
                            if file.type == "application/pdf":
                                result = extract_pdf_content(file)
                                if result['success']:
                                    st.success("PDF content extracted successfully!")
                                    st.write(f"**Pages:** {result['pages']}")
                                    st.write(f"**Content Preview:** {result['content'][:500]}...")
                                else:
                                    st.error(f"Error: {result['error']}")
                            
                            elif file.type == "text/csv":
                                result = extract_csv_content(file)
                                if result['success']:
                                    st.success("CSV data loaded successfully!")
                                    st.write(f"**Rows:** {result['rows']}, **Columns:** {result['columns']}")
                                    st.dataframe(result['dataframe'].head())
                                else:
                                    st.error(f"Error: {result['error']}")
                            
                            elif file.type == "text/plain":
                                result = extract_txt_content(file)
                                if result['success']:
                                    st.success("Text content extracted successfully!")
                                    st.write(f"**Content Length:** {len(result['content'])} characters")
                                    st.write(f"**Preview:** {result['content'][:500]}...")
                                else:
                                    st.error(f"Error: {result['error']}")
                            
                            else:
                                st.info("DOCX support coming soon!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 3: COMBINED RESULTS
    with tab3:
        st.header("📊 All Scraped & Uploaded Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌐 Scraped URLs")
            if st.session_state.scraped_data:
                for i, data in enumerate(st.session_state.scraped_data):
                    if data['success']:
                        st.write(f"**{i+1}. {data['title']}**")
                        st.write(f"URL: {data['url']}")
                        st.write(f"Content: {data['content_length']} chars")
                        st.write("---")
            else:
                st.info("No URLs scraped yet")
        
        with col2:
            st.subheader("📁 Uploaded Files")
            if uploaded_files:
                for file in uploaded_files:
                    st.write(f"📄 {file.name}")
                    st.write(f"Type: {file.type}")
                    st.write(f"Size: {file.size / 1024:.1f} KB")
                    st.write("---")
            else:
                st.info("No files uploaded yet")
        
        # Export options
        if st.session_state.scraped_data or uploaded_files:
            st.subheader("📤 Export Data")
            
            export_data = ""
            if st.session_state.scraped_data:
                export_data += "=== SCRAPED URLS ===\n\n"
                for data in st.session_state.scraped_data:
                    if data['success']:
                        export_data += f"Title: {data['title']}\n"
                        export_data += f"URL: {data['url']}\n"
                        export_data += f"Content: {data['content'][:1000]}...\n\n"
            
            if export_data:
                st.download_button(
                    label="📥 Download Scraped Data as TXT",
                    data=export_data,
                    file_name="scraped_data.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
