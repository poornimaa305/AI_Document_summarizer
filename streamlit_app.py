import streamlit as st
import PyPDF2
from docx import Document
from transformers import pipeline

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Document Summarizer",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------
# Load AI Model
# ---------------------------------------------------

@st.cache_resource
def load_model():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )

summarizer = load_model()

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("📄 AI Document Summarizer")

summary_length = st.sidebar.selectbox(
    "Summary Length",
    ["Short", "Medium", "Long"]
)

st.sidebar.markdown("---")

st.sidebar.write("Supported Formats")

st.sidebar.success("TXT")

st.sidebar.success("PDF")

st.sidebar.success("DOCX")

st.sidebar.markdown("---")

st.sidebar.info(
    "Upload any document and generate an AI-powered summary."
)

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("📄 AI Document Summarizer")

st.write(
    "Upload TXT, PDF or DOCX documents and generate an AI summary."
)

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["txt", "pdf", "docx"]
)

# ---------------------------------------------------
# Read Document
# ---------------------------------------------------

if uploaded_file:

    text = ""

    try:

        if uploaded_file.type == "text/plain":

            text = uploaded_file.read().decode("utf-8")

        elif uploaded_file.type == "application/pdf":

            pdf = PyPDF2.PdfReader(uploaded_file)

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:

                    text += extracted + "\n"

        elif uploaded_file.name.endswith(".docx"):

            doc = Document(uploaded_file)

            for para in doc.paragraphs:

                text += para.text + "\n"

    except Exception as e:

        st.error(f"Unable to read file.\n\n{e}")

    # ---------------------------------------------------

    if len(text) > 0:

        st.success("Document Uploaded Successfully!")

        # -----------------------------------------

        st.subheader("Document Information")

        col1, col2, col3 = st.columns(3)

        col1.metric("Characters", len(text))

        col2.metric("Words", len(text.split()))

        col3.metric("Lines", len(text.splitlines()))

        # -----------------------------------------

        with st.expander("View Extracted Document"):

            st.text_area(
                "Document",
                text,
                height=350
            )

        # -----------------------------------------

        if summary_length == "Short":

            max_length = 60
            min_length = 20

        elif summary_length == "Medium":

            max_length = 120
            min_length = 50

        else:

            max_length = 200
            min_length = 80

        # -----------------------------------------

        st.subheader("Generating Summary")

        progress = st.progress(0)

        progress.progress(20)

        with st.spinner("AI is reading the document..."):

            progress.progress(40)

            summary = summarizer(
                text[:3000],
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )

            progress.progress(80)

        progress.progress(100)

        summary_text = summary[0]["summary_text"]

        st.success("Summary Generated Successfully!")

        st.subheader("AI Summary")

        st.write(summary_text)

        # -----------------------------------------
        # Download Button
        # -----------------------------------------

        st.download_button(
            label="📥 Download Summary",
            data=summary_text,
            file_name="summary.txt",
            mime="text/plain"
        )

        # -----------------------------------------
        # Copy Option
        # -----------------------------------------

        st.code(summary_text)
