import os
import sys
import requests
import streamlit as st

# Setup Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.generator import sanitize_text, format_docx, format_pdf, format_html_preview

LOGO_PATH = os.path.join("Image", "Logo.png")

st.set_page_config(page_title="LegalEase", layout="centered")

# Header section with Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center;'>⚖️ LegalEase</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)

# User Input Fields
document_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)", placeholder="Freelance Work Contract")
parties = st.text_area("Parties Involved", placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)", placeholder="Work must be delivered by May 15, 2025; Payment within 7 days")
dates = st.text_input("Effective Date", placeholder="April 15, 2025")

# Generation Action
if st.button("Generate Document"):
    if not document_type or not parties:
        st.error("Please fill in the required fields: Document Type and Parties Involved.")
    else:
        with st.spinner("Generating legal document via Gemini AI..."):
            try:
                payload = {
                    "document_type": document_type,
                    "parties": parties,
                    "terms": terms,
                    "dates": dates
                }
                res = requests.post("http://localhost:8000/generate", json=payload)
                if res.status_code == 200:
                    generated_raw = res.json().get("document", "")
                    st.session_state["generated_text"] = sanitize_text(generated_raw)
                    st.success("Document Generated Successfully!")
                else:
                    st.error(f"API Error: {res.status_code}")
            except Exception as e:
                st.error(f"Failed to connect to backend server: {e}")

# Live Preview, Edit & Download Options
if "generated_text" in st.session_state:
    generated_text = st.session_state["generated_text"]

    # Styled HTML Preview Card
    styled_html = format_html_preview(generated_text)
    st.markdown(
        f"<div style='background-color: #1e1e1e; padding: 20px; border-radius: 8px; color: #ffffff;'>{styled_html}</div>",
        unsafe_allow_html=True
    )
    
    st.write("")
    
    # Toggle Edit Mode
    if st.checkbox("Click to Edit Document"):
        edited_text = st.text_area("Edit Document Below:", value=generated_text, height=300)
        st.session_state["generated_text"] = edited_text
        generated_text = edited_text

    st.subheader("Download Options")
    file_prefix = document_type.replace(' ', '_').lower() if document_type else "document"

    col_txt, col_docx, col_pdf = st.columns(3)

    # 1. Plain Text Export
    with col_txt:
        st.download_button(
            label="Download as .TXT",
            data=generated_text,
            file_name=f"{file_prefix}.txt",
            mime="text/plain"
        )

    # 2. DOCX Export
    with col_docx:
        docx_bytes = format_docx(generated_text, document_type, LOGO_PATH if os.path.exists(LOGO_PATH) else None)
        st.download_button(
            label="Download as .DOCX",
            data=docx_bytes,
            file_name=f"{file_prefix}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    # 3. PDF Export
    with col_pdf:
        pdf_bytes = format_pdf(generated_text, document_type, LOGO_PATH if os.path.exists(LOGO_PATH) else None)
        st.download_button(
            label="Download as .PDF",
            data=pdf_bytes,
            file_name=f"{file_prefix}.pdf",
            mime="application/pdf"
        )
