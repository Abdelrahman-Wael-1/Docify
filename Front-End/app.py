import streamlit as st
import requests
import json
from pathlib import Path
import time
import base64

# Page configuration
st.set_page_config(
    page_title="Docify - AI Documentation Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .upload-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        animation: fadeIn 0.5s;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    .assistant-message {
        background: #f0f2f6;
        color: #333;
        margin-right: 20%;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .status-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid;
    }
    .status-success {
        background: #d4edda;
        border-color: #28a745;
        color: #155724;
    }
    .status-error {
        background: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }
    .status-info {
        background: #d1ecf1;
        border-color: #17a2b8;
        color: #0c5460;
    }
    h1 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Supported languages
LANGUAGES = {
    'python': ['.py'], 
    'javascript': ['.js', '.jsx'], 
    'typescript': ['.ts', '.tsx'],
    'java': ['.java'], 
    'c++': ['.cpp', '.hpp', '.cc'], 
    'c': ['.c', '.h'],
    'c#': ['.cs'], 
    'go': ['.go'], 
    'rust': ['.rs'], 
    'php': ['.php'],
    'ruby': ['.rb'],
    'swift': ['.swift'],
    'kotlin': ['.kt']
}

def detect_language(filename):
    """Auto-detect language from file extension"""
    ext = Path(filename).suffix.lower()
    for lang, extensions in LANGUAGES.items():
        if ext in extensions:
            return lang
    return None

def call_api(prompt, max_length=300):
    """Call the Kaggle API via ngrok"""
    try:
        api_url = st.session_state.get('api_url', '')
        api_key = st.session_state.get('api_key', '')
        
        if not api_url or not api_key:
            return "⚠️ Please configure API settings in the sidebar first!"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "max_length": max_length
        }
        
        with st.spinner('🤖 AI is thinking...'):
            response = requests.post(
                f"{api_url}/generate",
                headers=headers,
                json=data,
                timeout=120
            )
        
        if response.status_code == 200:
            return response.json().get('response', 'No response')
        elif response.status_code == 401:
            return "❌ Authentication failed. Check your API key."
        else:
            return f"❌ Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. The model might be processing a long response."
    except requests.exceptions.ConnectionError:
        return "🔌 Connection error. Make sure your ngrok URL is correct and Kaggle kernel is running."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'code_content' not in st.session_state:
    st.session_state.code_content = None
if 'filename' not in st.session_state:
    st.session_state.filename = None
if 'language' not in st.session_state:
    st.session_state.language = None
if 'api_url' not in st.session_state:
    st.session_state.api_url = ''
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/source-code.png", width=150)
    st.markdown("## ⚙️ API Configuration")
    
    api_url = st.text_input(
        "🌐 Ngrok URL",
        value=st.session_state.api_url,
        placeholder="https://xxxx-xx-xx-xx-xx.ngrok-free.app",
        help="Enter your ngrok public URL from Kaggle"
    )
    
    api_key = st.text_input(
        "🔑 API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="secret123",
        help="Enter your API key (default: secret123)"
    )
    
    if st.button("💾 Save Settings"):
        st.session_state.api_url = api_url.rstrip('/')
        st.session_state.api_key = api_key
        st.success("✅ Settings saved!")
    
    st.markdown("---")
    
    # Test connection
    if st.button("🔍 Test Connection"):
        if api_url and api_key:
            try:
                response = call_api("Hello, test connection", max_length=50)
                if "Error" in response or "⚠️" in response or "❌" in response:
                    st.error("❌ Connection failed!")
                    st.error(response)
                else:
                    st.success("✅ Connected successfully!")
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")
        else:
            st.warning("Please enter API URL and Key first")
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    st.metric("Messages Sent", len(st.session_state.chat_history))
    if st.session_state.code_content:
        st.metric("Code Lines", len(st.session_state.code_content.split('\n')))
    
    st.markdown("---")
    st.markdown("### 🎯 Quick Actions")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    if st.button("🔄 Reset All"):
        st.session_state.chat_history = []
        st.session_state.code_content = None
        st.session_state.filename = None
        st.session_state.language = None
        st.rerun()

# Main content
st.markdown("<h1>✨ Docify</h1>", unsafe_allow_html=True)
st.markdown("### Transform your code into beautiful documentation, instantly!")

# File upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader(
        "📁 Drop your code file here",
        type=list(set([ext.replace('.', '') for exts in LANGUAGES.values() for ext in exts])),
        help="Supported: Python, JavaScript, TypeScript, Java, C++, C, C#, Go, Rust, PHP, Ruby, Swift, Kotlin"
    )

with col2:
    language_options = ["Auto-Detect"] + sorted([lang.upper() for lang in LANGUAGES.keys()])
    selected_language = st.selectbox(
        "🔤 Language",
        language_options,
        help="Select language or use auto-detect"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Process uploaded file
if uploaded_file is not None:
    # Read file content
    code_content = uploaded_file.read().decode('utf-8')
    filename = uploaded_file.name
    
    # Detect language
    if selected_language == "Auto-Detect":
        detected_lang = detect_language(filename)
        if detected_lang:
            language = detected_lang
            st.markdown(f'<div class="status-box status-success">✅ File uploaded: <b>{filename}</b><br>✅ Detected language: <b>{language.upper()}</b></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-box status-error">❌ Could not detect language for <b>{filename}</b>. Please select manually.</div>', unsafe_allow_html=True)
            language = None
    else:
        language = selected_language.lower()
        st.markdown(f'<div class="status-box status-success">✅ File uploaded: <b>{filename}</b><br>✅ Language: <b>{language.upper()}</b></div>', unsafe_allow_html=True)
    
    # Store in session state
    st.session_state.code_content = code_content
    st.session_state.filename = filename
    st.session_state.language = language
    
    # Show code preview
    with st.expander("👀 Preview Code", expanded=False):
        st.code(code_content, language=language if language else 'text')

# Main interface tabs
if st.session_state.code_content and st.session_state.language:
    tab1, tab2 = st.tabs(["💬 Chat with AI", "📄 Generate Documentation"])
    
    # Chat tab
    with tab1:
        st.markdown("### 💬 Ask questions about your code")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for idx, (role, message) in enumerate(st.session_state.chat_history):
                if role == "user":
                    st.markdown(f'<div class="chat-message user-message">👤 <b>You:</b><br>{message}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message assistant-message">🤖 <b>AI:</b><br>{message}</div>', unsafe_allow_html=True)
        
        # Chat input
        col1, col2 = st.columns([5, 1])
        with col1:
            user_message = st.text_input(
                "Your question",
                placeholder="E.g., What does this function do? Can you explain the main logic?",
                key="chat_input",
                label_visibility="collapsed"
            )
        with col2:
            send_button = st.button("📤 Send", use_container_width=True)
        
        # Quick question buttons
        st.markdown("##### 🎯 Quick Questions:")
        quick_cols = st.columns(4)
        quick_questions = [
            "Explain the main purpose",
            "List all functions",
            "Find potential bugs",
            "Suggest improvements"
        ]
        
        for idx, col in enumerate(quick_cols):
            with col:
                if st.button(quick_questions[idx], use_container_width=True):
                    user_message = quick_questions[idx]
                    send_button = True
        
        # Process message
    if (send_button or user_message) and user_message:
        # Validate inputs
        if not st.session_state.api_url or not st.session_state.api_key:
            st.error("⚠️ Please configure API settings in the sidebar first!")
        else:
            # Show processing indicator
            with st.spinner('🤖 AI is analyzing your code...'):
                try:
                    headers = {
                        "Authorization": f"Bearer {st.session_state.api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    # Limit code size to prevent token issues
                    code_snippet = st.session_state.code_content[:3000] if len(st.session_state.code_content) > 3000 else st.session_state.code_content
                    
                    data = {
                        "message": user_message,
                        "code_content": code_snippet,
                        "language": st.session_state.language
                    }
                    
                    response = requests.post(
                        f"{st.session_state.api_url}/chat",
                        headers=headers,
                        json=data,
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        ai_response = result.get('response', '').strip()
                        
                        # Validate response
                        if not ai_response or len(ai_response) < 10:
                            ai_response = "❌ I couldn't generate a proper response. Please try rephrasing your question or ask something more specific about the code."
                        
                        # Add to history
                        st.session_state.chat_history.append(("user", user_message))
                        st.session_state.chat_history.append(("assistant", ai_response))
                        
                        # Rerun to update display
                        st.rerun()
                        
                    elif response.status_code == 401:
                        st.error("❌ Authentication failed. Check your API key.")
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Connection error. Make sure your ngrok URL is correct and Kaggle kernel is running.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Documentation tab
    with tab2:
        st.markdown("### 📄 Generate Professional Documentation")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            max_tokens = st.slider("📏 Documentation Length", 500, 2000, 1200, 100)
        with col2:
            include_examples = st.checkbox("💡 Include Examples", value=True)
        with col3:
            detailed = st.checkbox("🔍 Detailed Analysis", value=True)
        
        if st.button("🎯 Generate Documentation", use_container_width=True):
            try:
                api_url = st.session_state.get('api_url', '')
                api_key = st.session_state.get('api_key', '')
                
                if not api_url or not api_key:
                    st.error("⚠️ Please configure API settings in the sidebar first!")
                else:
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    data = {
                        "code_content": st.session_state.code_content,
                        "filename": st.session_state.filename,
                        "language": st.session_state.language
                    }
                    
                    with st.spinner('🤖 Generating documentation...'):
                        response = requests.post(
                            f"{api_url}/documentation",
                            headers=headers,
                            json=data,
                            timeout=180
                        )
                    
                    if response.status_code == 200:
                        result = response.json()
                        documentation = result.get('documentation', '')
                        file_base64 = result.get('file_base64', '')
                        
                        # Display documentation
                        st.markdown("---")
                        st.markdown("### 📋 Generated Documentation")
                        st.markdown(documentation)
                        
                        # Decode the Word file from base64
                        if file_base64:
                            doc_bytes = base64.b64decode(file_base64)
                            
                            # Create download button with actual Word file
                            st.download_button(
                                label="📥 Download Professional Documentation (.docx)",
                                data=doc_bytes,
                                file_name=f"{Path(st.session_state.filename).stem}_Documentation.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )
                            
                            st.success("✅ Documentation generated successfully!")
                        else:
                            st.warning("⚠️ Word file not generated. Showing text only.")
                            
                            # Fallback: download as markdown
                            st.download_button(
                                label="📥 Download as Markdown (.md)",
                                data=documentation,
                                file_name=f"{Path(st.session_state.filename).stem}_Documentation.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                    
                    elif response.status_code == 401:
                        st.error("❌ Authentication failed. Check your API key.")
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
            
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The documentation generation is taking longer than expected.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Connection error. Make sure your ngrok URL is correct and Kaggle kernel is running.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h2>👋 Welcome!</h2>
        <p style="font-size: 1.2rem; color: #666;">
            Get started by:
        </p>
        <ol style="text-align: left; max-width: 500px; margin: 2rem auto; font-size: 1.1rem;">
            <li>Configure your API settings in the sidebar 🔧</li>
            <li>Upload your code file above 📁</li>
            <li>Chat with AI about your code 💬</li>
            <li>Generate professional documentation 📄</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Show example
    with st.expander("📖 See Example"):
        st.markdown("""
        **Example workflow:**
        
        1. **Upload** a Python file (`app.py`)
        2. **Ask** questions like:
           - "What does the main function do?"
           - "Are there any security issues?"
           - "How can I optimize this code?"
        3. **Generate** professional documentation with one click
        4. **Download** formatted documentation
        """)

# Footer
# Around line 423:
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>✨ <b>Docify</b> | Powered by Mistral AI</p>
</div>
""", unsafe_allow_html=True)