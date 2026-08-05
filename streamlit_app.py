import streamlit as st
import PyPDF2
from docx import Document
from groq import Groq

# -----------------------------
# Streamlit Page
# -----------------------------
st.set_page_config(page_title="AI Document Summarizer")

st.title("📄 AI Document Summarizer")
st.write("Upload a PDF, DOCX or TXT file and get an AI-generated summary using Groq.")

# -----------------------------
# Load Groq Client
# -----------------------------
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------
# Read PDF
# -----------------------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

# -----------------------------
# Read DOCX
# -----------------------------
def read_docx(file):
    doc = Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text

# -----------------------------
# Read TXT
# -----------------------------
def read_txt(file):
    return file.read().decode("utf-8")

# -----------------------------
# Upload File
# -----------------------------
uploaded_file = st.file_uploader(
    "Choose a document",
    type=["pdf", "docx", "txt"]
)

summary_length = st.selectbox(
    "Summary Length",
    ["Short", "Medium", "Detailed"]
)

# -----------------------------
# Generate Summary
# -----------------------------
if uploaded_file is not None:

    if uploaded_file.name.endswith(".pdf"):
        text = read_pdf(uploaded_file)

    elif uploaded_file.name.endswith(".docx"):
        text = read_docx(uploaded_file)

    else:
        text = read_txt(uploaded_file)

    st.subheader("Extracted Text")

    st.text_area(
        "",
        text[:3000],
        height=200
    )

    if st.button("Generate Summary"):

        with st.spinner("Generating Summary..."):

            prompt = f"""
You are an expert document summarizer.

Summarize the following document.

Summary Length: {summary_length}

Document:

{text[:12000]}
"""

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            summary = response.choices[0].message.content

        st.subheader("AI Summary")

        st.write(summary)

        st.download_button(
            "Download Summary",
            summary,
            file_name="summary.txt"
        )
