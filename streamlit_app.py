import streamlit as st
import requests
from bs4 import BeautifulSoup
# Rest of the simple code...
# Page configuration
st.set_page_config(
    page_title="URL Scraper & File Analyzer",
    page_icon="🌐",
    layout="wide"
)

def main():
    st.title("🌐 URL Scraper + File Analyzer")
    st.markdown("**पहले URLs से Data Scrape करें, फिर Files Upload करें**")
    
    # Initialize session state
    if 'scraped_data' not in st.session_state:
        st.session_state.scraped_data = []
    
    # Main workflow
    st.header("🚀 Step 1: URLs से Data Scrape करें")
    
    url_input = st.text_area(
        "Website URLs डालें (एक line में एक URL)",
        placeholder="https://example.com\nhttps://example.org",
        height=100
    )
    
    if st.button("🌐 Scrape URLs", type="primary") and url_input:
        urls = [url.strip() for url in url_input.split('\n') if url.strip()]
        
        if urls:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, url in enumerate(urls):
                status_text.text(f"Scraping: {url}")
                
                try:
                    # Simple scraping
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.get(url, headers=headers, timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Remove scripts and styles
                    for element in soup(["script", "style"]):
                        element.decompose()
                    
                    title = soup.find('title')
                    title_text = title.get_text() if title else "No Title"
                    content = soup.get_text()[:2000]  # First 2000 characters
                    
                    st.session_state.scraped_data.append({
                        'url': url,
                        'title': title_text,
                        'content': content,
                        'status': 'success'
                    })
                    
                except Exception as e:
                    st.session_state.scraped_data.append({
                        'url': url,
                        'title': 'Error',
                        'content': f'Scraping failed: {str(e)}',
                        'status': 'error'
                    })
                
                progress_bar.progress((i + 1) / len(urls))
            
            status_text.text("✅ Scraping completed!")
    
    # Show scraping results
    if st.session_state.scraped_data:
        st.subheader("📊 Scraping Results")
        for data in st.session_state.scraped_data:
            if data['status'] == 'success':
                with st.expander(f"✅ {data['title']}"):
                    st.write(f"**URL:** {data['url']}")
                    st.write(f"**Content Preview:** {data['content'][:500]}...")
            else:
                st.error(f"❌ {data['url']} - {data['content']}")
    
    st.markdown("---")
    
    # File upload section
    st.header("📁 Step 2: Files Upload करें")
    
    uploaded_files = st.file_uploader(
        "PDF, CSV, TXT files select करें",
        type=['pdf', 'csv', 'txt'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
        
        for file in uploaded_files:
            with st.expander(f"📄 {file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.write(f"**Type:** {file.type}")
                    st.write(f"**Size:** {file.size / 1024:.1f} KB")
                    
                    if st.button(f"Analyze {file.name}", key=file.name):
                        # Process based on file type
                        if file.type == "application/pdf":
                            try:
                                pdf_reader = PyPDF2.PdfReader(file)
                                text = ""
                                for page in pdf_reader.pages:
                                    text += page.extract_text() + "\n"
                                
                                st.success("PDF content extracted!")
                                st.write(f"**Pages:** {len(pdf_reader.pages)}")
                                st.write(f"**Content Preview:** {text[:500]}...")
                                
                            except Exception as e:
                                st.error(f"PDF Error: {str(e)}")
                        
                        elif file.type == "text/csv":
                            try:
                                df = pd.read_csv(file)
                                st.success("CSV data loaded!")
                                st.write(f"**Rows:** {len(df)}, **Columns:** {len(df.columns)}")
                                st.dataframe(df.head())
                                
                            except Exception as e:
                                st.error(f"CSV Error: {str(e)}")
                        
                        elif file.type == "text/plain":
                            try:
                                raw_data = file.read()
                                encoding = chardet.detect(raw_data)['encoding']
                                file.seek(0)
                                content = file.read().decode(encoding or 'utf-8')
                                
                                st.success("Text content extracted!")
                                st.write(f"**Characters:** {len(content)}")
                                st.write(f"**Preview:** {content[:500]}...")
                                
                            except Exception as e:
                                st.error(f"Text Error: {str(e)}")
                
                with col2:
                    st.write("**File Analysis** - Analyze बटन पर क्लिक करें")

if __name__ == "__main__":
    main()
