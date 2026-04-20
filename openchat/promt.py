from langchain_nvidia_ai_endpoints import ChatNVIDIA
from pydantic_core.core_schema import ModelSchema
from requests import models
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate,load_prompt

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

llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct")

template = load_prompt("template.json")
# Generate the paper prompt by filling in the template with user inputs
prompt = template.format(
    paper_input=paper_input,
    style_input=style_input,
    length_input=length_input
)

# Set up the language model is now handled above based on selection

def generate_response(prompt_text: str) -> str:
    """Generate a response from the LLM given a prompt string."""
    response = llm.invoke(prompt_text)
    # The response content can be a string or a list (for streaming outputs)
    if isinstance(response.content, list):
        # Concatenate all text parts if it's a list
        return "".join(part.get("text", "") for part in response.content)
    return response.content or ""

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