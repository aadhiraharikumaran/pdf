import streamlit as st
import pdfplumber
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

def initialize_llm(model_type):
    return Groq(model=model_type, api_key=api_key)

def summarize_text(llm, text, summary_type):
    if summary_type == "Long Summary":
        prompt = f"Give a summary of the text: {text}"
    elif summary_type == "Short Summary":
        prompt = f"Give a 100-word summary of the text: {text}"
    elif summary_type == "Creative Summary":
        prompt = f"Give a creative summary of the text: {text}"
    elif summary_type == "Bullet Point Summary":
        prompt = f"Give a summary of the text in 3 bullet points: {text}"

    response = llm.complete(prompt)

    # Ensure response is valid and extract the actual summary text
    if isinstance(response, dict) and 'text' in response:
        return response['text'].strip()
    elif hasattr(response, 'text'):
        return response.text.strip()
    else:
        return "Error: Could not retrieve clean summary."

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""  # Handle cases where text extraction fails
    return text.strip()

# Streamlit app
st.title("📄 Text Summarizer 🤖")

# File uploader for PDF
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Extract text from the uploaded PDF
if uploaded_file:
    extracted_text = extract_text_from_pdf(uploaded_file)
else:
    extracted_text = ""

# Display extracted text in a non-editable text area
text_area = st.text_area("Extracted text from PDF", value=extracted_text, height=300, disabled=True)

# Dropdown for summary type
summary_type = st.selectbox(
    "Select Summary Type",
    ("Long Summary", "Short Summary", "Creative Summary", "Bullet Point Summary")
)

# Dropdown for model type
model_type = st.selectbox(
    "Select Model Type",
    ("Gemma-7b-It", "llama3-70b-8192", "Mixtral-8x7b-32768")
)

# Initialize the selected model
llm = initialize_llm(model_type)

# Button to generate summary
if st.button("Generate Summary"):
    if extracted_text:
        summary = summarize_text(llm, extracted_text, summary_type)
        st.write(f"### {summary_type} using {model_type}")
        st.write(summary)
    else:
        st.warning("Please upload a PDF to summarize.")

# Footer
st.markdown("---")
st.markdown("Made by Aadhira")
