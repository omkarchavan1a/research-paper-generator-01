from langchain_core.prompts import PromptTemplate, load_prompt
import streamlit as st
from dotenv import load_dotenv
import os
import requests as _requests

load_dotenv()

st.markdown(
    """
    <style>
        .main-header {
            font-size: 2.8rem;
            text-align: center;
            letter-spacing: 2px;
            color: #22223b;
            margin-bottom: 16px;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
        }
        .stTextInput > label, .stSelectbox > label {
            color: black !important;
            font-weight: 500 !important;
            font-size: 1.13rem !important;
        }
        .stSelectbox, .stTextInput {
            padding: 12px;
            border-radius: 10px;
        }
        .stApp {
            background: linear-gradient(120deg, #d1d9e6 40%, #b8c0ff 100%);
            color: black !important;
        }  
        .stButton{
            color:white
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="main-header">AI Research Paper Generator</div>', unsafe_allow_html=True)

paper_input = st.text_input("📄 Enter research paper name", placeholder="e.g. Quantum Computing Applications", key="paper_input")

style_input = st.selectbox(
    "🎨 Select a style",
    [
        "Academic",
        "Technical",
        "Creative",
        "Persuasive",
        "Narrative",
        "Code oriented",
        "Analytical",
        "Expository",
        "Descriptive",
        "Reflective",
        "Comparative",
        "Argumentative",
        "Systematic",
        "Critical",
        "Review",
        "Case Study",
        "Report",
        "Experimental",
        "Theoretical",
        "Interdisciplinary",
        "Practical",
        "Socratic",
        "Didactic",
        "Satirical",
        "Informative",
        "Instructive",
        "Formal",
        "Informal",
        ""
    ],
    index=0,
    key="style_input",
)

length_input = st.selectbox(
    "✍️ Select length",
    ["Short", "Medium", "Long"],
    index=1,
    key="length_input",
)

template = load_prompt("template.json")
# Generate the paper prompt by filling in the template with user inputs
prompt = template.format(
    paper_input=paper_input,
    style_input=style_input,
    length_input=length_input
)

# ---------------------------------------------------------------------------
# Sarvam AI configuration (loaded from .env)
# Provider: Sarvam AI  —  https://api.sarvam.ai
# OpenAI-compatible REST API; models: sarvam-105b, sarvam-30b
# ---------------------------------------------------------------------------
SARVAM_API_KEY  = os.getenv("SARVAM_API_KEY", "")
SARVAM_BASE_URL = os.getenv("SARVAM_BASE_URL", "https://api.sarvam.ai/v1")
SARVAM_MODEL    = os.getenv("SARVAM_MODEL", "sarvam-105b")


def generate_response(prompt_text: str) -> str:
    """Call Sarvam AI's OpenAI-compatible chat completions endpoint.

    Sarvam's reasoning models return their thinking trace in ``reasoning_content``
    and the final answer in ``content``.  We call the API with ``requests``
    directly so we own the parsing logic and avoid any SDK-level content stripping.
    """
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

    # sarvam-105b → final answer is in `content`
    # sarvam-30b  → deep-reasoning model; final answer is in `reasoning_content`,
    #               `content` is null
    content = message.get("content") or ""
    if content.strip():
        return content

    # Fallback for reasoning models: use the last paragraph of reasoning_content
    reasoning = message.get("reasoning_content") or ""
    if reasoning.strip():
        paragraphs = [p.strip() for p in reasoning.strip().split("\n\n") if p.strip()]
        return paragraphs[-1] if paragraphs else reasoning

    return ""


# Button to trigger the generation
if st.button("Generate"):
    prompt_str = str(prompt)
    if not prompt_str.strip():
        st.warning("Please enter a paper type, style, and length before generating.")
    else:
        with st.spinner("Generating your research paper..."):
            try:
                result = generate_response(prompt_str)
                st.write(result)
            except Exception as exc:
                st.error(f"Failed to generate paper: {exc}")