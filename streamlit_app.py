import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import PyPDF2
import docx
import io
import chardet
from datetime import datetime
import json

# ==================== PAGE CONFIG (SEO Friendly) ====================
st.set_page_config(
    page_title="AI Content Analyzer - Extract Insights from Files & URLs",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/amlivkill/ai-content-analyzer',
        'Report a bug': "https://github.com/amlivkill/ai-content-analyzer/issues",
        'About': "### AI Content Analyzer\nExtract key insights from PDF, CSV, DOCX, TXT files and URLs using advanced AI technology."
    }
)

# ==================== CUSTOM CSS (Better UI) ====================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# ==================== HELPER FUNCTIONS ====================
def extract_text_from_pdf(file):
    """PDF से text extract करें"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"PDF reading error: {str(e)}"

def extract_text_from_txt(file):
    """TXT file से text extract करें"""
    try:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
        file.seek(0)
        return file.read().decode(encoding or 'utf-8')
    except Exception as e:
        return f"TXT reading error: {str(e)}"

def extract_data_from_csv(file):
    """CSV file से data extract करें"""
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        return f"CSV reading error: {str(e)}"

def scrape_website_content(url):
    """Website content scrape करें"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove scripts and styles
        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()
        
        # Get main content
        title = soup.find('title')
        title_text = title.get_text() if title else "No Title"
        
        # Try to get main content
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        text = main_content.get_text(separator='\n', strip=True)
        
        return {
            'title': title_text,
            'content': text[:5000],  # Limit content
            'url': url,
            'status': 'success'
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

# ==================== MOCK AI ANALYSIS (OpenAI API के बिना) ====================
def mock_ai_analysis(content, analysis_type):
    """OpenAI API के बिना mock analysis"""
    if analysis_type == "summary":
        return f"📝 **सारांश:** यह कंटेंट {len(content)} characters का है। मुख्य विचारों में डेटा विश्लेषण, AI तकनीक, और ऑटोमेशन शामिल हैं।"
    
    elif analysis_type == "key_points":
        return "🎯 **मुख्य बिंदु:**\n- डेटा एकत्रीकरण और विश्लेषण\n- स्वचालित रिपोर्ट जनरेशन\n- मल्टी-फॉर्मेट सपोर्ट\n- रियल-टाइम प्रोसेसिंग"
    
    elif analysis_type == "sentiment":
        return "😊 **भावना विश्लेषण:** सकारात्मक - कंटेंट जानकारीपूर्ण और सहायक है"

# ==================== MAIN APP ====================
def main():
    # ==================== HERO SECTION ====================
    st.markdown('<h1 class="main-header">🔍 AI Content Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h3 style='color: #6c757d;'>PDF, CSV, DOCX, TXT Files और Websites से Automatically Insights Extract करें</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # ==================== FEATURES GRID ====================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h4>📄 Multiple Formats</h4>
            <p>PDF, CSV, DOCX, TXT सपोर्ट</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h4>🌐 URL Analysis</h4>
            <p>किसी भी Website का Content Analyze करें</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h4>🤖 AI Powered</h4>
            <p>Smart Summarization और Key Points</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='feature-card'>
            <h4>💾 Export Data</h4>
            <p>Results को Download करें</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=50)
        st.title("Settings")
        
        # API Configuration
        st.subheader("API Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", 
                               help="Get your API key from https://platform.openai.com/")
        
        # Analysis Options
        st.subheader("Analysis Options")
        analysis_types = st.multiselect(
            "Select Analysis Types",
            ["Summary", "Key Points", "Sentiment Analysis", "Word Frequency"],
            default=["Summary", "Key Points"]
        )
        
        # File Size Limit
        max_file_size = st.slider("Max File Size (MB)", 1, 50, 10)
        
        st.markdown("---")
        st.markdown("""
        **How to use:**
        1. File upload करें या URL डालें
        2. Analysis options select करें
        3. Analyze बटन पर क्लिक करें
        4. Results download करें
        """)
    
    # ==================== MAIN CONTENT AREA ====================
    tab1, tab2, tab3 = st.tabs(["📁 File Upload", "🌐 URL Analysis", "📊 Analysis History"])
    
    with tab1:
        st.header("File Upload & Analysis")
        
        uploaded_files = st.file_uploader(
            "Choose files to analyze",
            type=['pdf', 'csv', 'txt', 'docx'],
            accept_multiple_files=True,
            help="Supported formats: PDF, CSV, TXT, DOCX"
        )
        
        if uploaded_files:
            st.markdown(f'<div class="success-box">✅ {len(uploaded_files)} file(s) selected</div>', unsafe_allow_html=True)
            
            for file in uploaded_files:
                with st.expander(f"📄 {file.name}", expanded=True):
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.write(f"**Type:** {file.type}")
                        st.write(f"**Size:** {file.size / 1024:.1f} KB")
                    
                    with col2:
                        if st.button(f"Analyze {file.name}", key=f"btn_{file.name}"):
                            with st.spinner("Analyzing content..."):
                                # File processing based on type
                                if file.type == "application/pdf":
                                    content = extract_text_from_pdf(file)
                                elif file.type == "text/plain":
                                    content = extract_text_from_txt(file)
                                elif file.type == "text/csv":
                                    content = extract_data_from_csv(file)
                                else:
                                    content = "File type processing coming soon..."
                                
                                # Display results
                                if "Summary" in analysis_types:
                                    st.subheader("📝 Summary")
                                    st.write(mock_ai_analysis(content, "summary"))
                                
                                if "Key Points" in analysis_types:
                                    st.subheader("🎯 Key Points")
                                    st.write(mock_ai_analysis(content, "key_points"))
                                
                                # Save to history
                                st.session_state.analysis_history.append({
                                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    'type': 'file',
                                    'name': file.name,
                                    'analysis': 'completed'
                                })
    
    with tab2:
        st.header("Website URL Analysis")
        
        url_input = st.text_input(
            "Enter website URL",
            placeholder="https://example.com",
            help="Enter full URL including http:// or https://"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if url_input:
                if st.button("🌐 Analyze Website", type="primary"):
                    with st.spinner("Scraping and analyzing website content..."):
                        website_data = scrape_website_content(url_input)
                        
                        if website_data['status'] == 'success':
                            st.markdown('<div class="success-box">✅ Website content extracted successfully!</div>', unsafe_allow_html=True)
                            
                            st.subheader("🌐 Website Information")
                            st.write(f"**Title:** {website_data['title']}")
                            st.write(f"**URL:** {website_data['url']}")
                            st.write(f"**Content Length:** {len(website_data['content'])} characters")
                            
                            # Analysis results
                            if "Summary" in analysis_types:
                                st.subheader("📝 Summary")
                                st.write(mock_ai_analysis(website_data['content'], "summary"))
                            
                            if "Key Points" in analysis_types:
                                st.subheader("🎯 Key Points")
                                st.write(mock_ai_analysis(website_data['content'], "key_points"))
                            
                            # Save to history
                            st.session_state.analysis_history.append({
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'type': 'url',
                                'name': url_input,
                                'analysis': 'completed'
                            })
                        else:
                            st.error(f"Error: {website_data['error']}")
    
    with tab3:
        st.header("Analysis History")
        
        if st.session_state.analysis_history:
            for i, history in enumerate(reversed(st.session_state.analysis_history[-10:])):  # Last 10 entries
                with st.expander(f"{history['timestamp']} - {history['name']}"):
                    st.write(f"**Type:** {history['type']}")
                    st.write(f"**Status:** {history['analysis']}")
        else:
            st.info("No analysis history yet. Upload files or analyze URLs to see history here.")
    
    # ==================== FOOTER (SEO Friendly) ====================
    st.markdown("---")
    st.markdown("""
    <div class='footer'>
        <p><strong>AI Content Analyzer</strong> - Extract meaningful insights from your documents and websites</p>
        <p>Built with ❤️ using Streamlit | Support: amlivkill@github</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== RUN APP ====================
if __name__ == "__main__":
    main()
