from langchain_core.prompts import load_prompt
import streamlit as st
from dotenv import load_dotenv
import os
import requests as _requests
import re

# Load environment variables
load_dotenv()

# Streamlit Page Configuration - must be the first streamlit call
st.set_page_config(
    page_title="AI Research Paper Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look & Feel
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Apply font and background */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .main-header {
            font-size: 2.8rem;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, #1e293b 0%, #4f46e5 50%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            padding-top: 10px;
        }
        
        .sub-header {
            font-size: 1.15rem;
            text-align: center;
            color: #64748b;
            margin-bottom: 32px;
            font-weight: 400;
        }
        
        /* Input section styling in sidebar */
        .sidebar-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Card container for the paper */
        .paper-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05), 0 2px 8px -1px rgba(0, 0, 0, 0.03);
            margin-top: 24px;
            margin-bottom: 24px;
            color: #334155;
            line-height: 1.8;
        }
        
        /* Welcome card */
        .welcome-card {
            background-color: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 12px;
            padding: 48px;
            text-align: center;
            color: #64748b;
            margin-top: 40px;
        }
        
        .welcome-icon {
            font-size: 3rem;
            margin-bottom: 16px;
        }
        
        /* Custom generate button */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            color: white !important;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
            margin-top: 10px;
        }
        
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #4338ca 0%, #2563eb 100%);
            box-shadow: 0 6px 16px rgba(79, 70, 229, 0.35);
            transform: translateY(-1px);
        }
        
        /* Metrics panel */
        .metric-box {
            background-color: #f1f5f9;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        
        .metric-val {
            font-size: 1.6rem;
            font-weight: 700;
            color: #4f46e5;
        }
        
        .metric-lbl {
            font-size: 0.85rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
    </style>
    """, unsafe_allow_html=True
)

# Initialize Session State to persist generated content across reruns
if "generated_paper" not in st.session_state:
    st.session_state.generated_paper = ""
if "paper_name" not in st.session_state:
    st.session_state.paper_name = ""

# Sidebar Configuration
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Paper Parameters</div>', unsafe_allow_html=True)
    
    paper_input = st.text_input(
        "📄 Research Paper Topic / Name", 
        value=st.session_state.paper_name if st.session_state.paper_name else "",
        placeholder="e.g. Quantum Computing in Modern Cryptography", 
        key="paper_input_widget"
    )
    
    style_input = st.selectbox(
        "🎨 Writing Style",
        [
            "Academic", "Technical", "Creative", "Persuasive", "Narrative", 
            "Code oriented", "Analytical", "Expository", "Descriptive", 
            "Reflective", "Comparative", "Argumentative", "Systematic", 
            "Critical", "Review", "Case Study", "Report", "Experimental", 
            "Theoretical", "Interdisciplinary", "Practical", "Socratic", 
            "Didactic", "Satirical", "Informative", "Instructive", "Formal", 
            "Informal", ""
        ],
        index=0,
        key="style_input_widget"
    )
    
    length_input = st.selectbox(
        "✍️ Desired Length",
        ["Short", "Medium", "Long"],
        index=1,
        key="length_input_widget"
    )
    
    st.markdown("---")
    st.caption("Powered by **Sarvam AI** & **LangChain**")

# Main Panel
st.markdown('<div class="main-header">AI Research Paper Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Draft publication-ready, fully-detailed academic research papers in seconds</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sarvam AI configuration (loaded from .env)
# ---------------------------------------------------------------------------
SARVAM_API_KEY  = os.getenv("SARVAM_API_KEY", "")
SARVAM_BASE_URL = os.getenv("SARVAM_BASE_URL", "https://api.sarvam.ai/v1")
SARVAM_MODEL    = os.getenv("SARVAM_MODEL", "sarvam-105b")

def generate_response(prompt_text: str) -> str:
    """Call Sarvam AI's OpenAI-compatible chat completions endpoint."""
    url = f"{SARVAM_BASE_URL}/chat/completions"
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "model": SARVAM_MODEL,
        "messages": [{"role": "user", "content": prompt_text}],
        "temperature": 0.7,
    }

    response = _requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    message = data["choices"][0]["message"]

    content = message.get("content") or ""
    if content.strip():
        return content

    # Fallback for reasoning models: use the last paragraph of reasoning_content
    reasoning = message.get("reasoning_content") or ""
    if reasoning.strip():
        paragraphs = [p.strip() for p in reasoning.strip().split("\n\n") if p.strip()]
        return paragraphs[-1] if paragraphs else reasoning

    return ""

# Generate Trigger Button (in the Sidebar)
with st.sidebar:
    generate_btn = st.button("Generate Paper")

if generate_btn:
    if not paper_input.strip():
        st.warning("Please enter a research paper topic/name before generating.")
    else:
        with st.spinner("Writing and structure planning in progress... (this might take up to 2 minutes)"):
            try:
                # Load the newly improved prompt template from template.json
                template = load_prompt("template.json")
                prompt = template.format(
                    paper_input=paper_input,
                    style_input=style_input,
                    length_input=length_input
                )
                
                # Call LLM
                result = generate_response(str(prompt))
                
                # Save results in session state
                st.session_state.generated_paper = result
                st.session_state.paper_name = paper_input
                st.rerun()  # Rerun to render output with proper download button & metrics
                
            except Exception as exc:
                st.error(f"Failed to generate research paper: {exc}")

# Display Section
if st.session_state.generated_paper:
    # 1. Calculate Metrics
    text_content = st.session_state.generated_paper
    word_count = len(text_content.split())
    char_count = len(text_content)
    reading_time = max(1, round(word_count / 200)) # ~200 words per minute average reading speed
    
    # 2. Display Metrics Dashboard
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f'<div class="metric-box"><div class="metric-val">{word_count:,}</div><div class="metric-lbl">Words</div></div>',
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f'<div class="metric-box"><div class="metric-val">{char_count:,}</div><div class="metric-lbl">Characters</div></div>',
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f'<div class="metric-box"><div class="metric-val">{reading_time} min</div><div class="metric-lbl">Est. Reading Time</div></div>',
            unsafe_allow_html=True
        )
        
    # 3. Download / Export Options
    clean_filename = re.sub(r'[^a-zA-Z0-9_-]', '_', st.session_state.paper_name.strip())
    if not clean_filename:
        clean_filename = "research_paper"
        
    st.markdown(" ") # Spacer
    st.download_button(
        label="📥 Download Research Paper (.md)",
        data=st.session_state.generated_paper,
        file_name=f"research_paper_{clean_filename}.md",
        mime="text/markdown"
    )
    
    # 4. Display the Generated Paper inside a styled card
    st.markdown('<div class="paper-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.generated_paper)
    st.markdown('</div>', unsafe_allow_html=True)
    
else:
    # Welcome / Instruction Area
    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-icon">📝</div>
            <h3>Ready to Generate Your Research Paper</h3>
            <p>Fill in the research paper topic, select a writing style and desired length in the sidebar, and click <b>Generate Paper</b>.</p>
            <p>The system will output a comprehensive, structured paper matching standard academic formats (APA/IEEE) complete with abstracts, literature review, findings, and references.</p>
        </div>
        """,
        unsafe_allow_html=True
    )