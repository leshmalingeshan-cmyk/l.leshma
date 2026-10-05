import io
import re
from docx import Document
from docx.shared import Inches, Pt
from fpdf import FPDF
from PIL import Image

def sanitize_text(text: str) -> str:
    """Removes non-latin/special characters and standardizes quote marks."""
    if not text:
        return ""
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    return text

def format_docx(text: str, doc_type: str, logo_path: str = None) -> bytes:
    """Formats document into DOCX with logo, titles, table for terms, and footers."""
    doc = Document()
    
    # Header / Logo
    if logo_path:
        try:
            doc.add_picture(logo_path, width=Inches(1.5))
        except Exception:
            pass

    # Document Title
    heading = doc.add_heading(doc_type, level=0)
    
    # Body Content
    lines = text.split('\n')
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        if line_str.startswith("## ") or line_str.startswith("# "):
            clean_h = line_str.replace("#", "").strip()
            doc.add_heading(clean_h, level=1)
        elif line_str.startswith("- ") or line_str.startswith("* "):
            p = doc.add_paragraph(style='List Bullet')
            p.add_run(line_str[2:].strip())
        else:
            doc.add_paragraph(line_str)

    # Footer
    section = doc.sections[0]
    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.text = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

def format_pdf(text: str, doc_type: str, logo_path: str = None) -> bytes:
    """Generates PDF output with header, logo, and footer using FPDF."""
    class LegalPDF(FPDF):
        def header(self):
            if logo_path:
                try:
                    self.image(logo_path, 10, 8, 33)
                except Exception:
                    pass
            self.set_font('Helvetica', 'B', 14)
            self.cell(0, 10, doc_type, border=0, ln=1, align='C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.cell(0, 10, 'LegalEase Inc. | contact@legalease.com | All Rights Reserved.', align='C')

    pdf = LegalPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)

    clean_text = sanitize_text(text)
    for line in clean_text.split('\n'):
        line_str = line.strip()
        if not line_str:
            pdf.ln(4)
            continue
        if line_str.startswith('#'):
            pdf.set_font("Helvetica", 'B', 12)
            pdf.multi_cell(0, 6, line_str.replace('#', '').strip())
            pdf.set_font("Helvetica", size=10)
        else:
            pdf.multi_cell(0, 5, line_str)
            
    buffer = io.BytesIO()
    pdf_output = pdf.output(dest='S')
    if isinstance(pdf_output, str):
        buffer.write(pdf_output.encode('latin1', errors='replace'))
    else:
        buffer.write(bytes(pdf_output))
    buffer.seek(0)
    return buffer.getvalue()

def format_html_preview(text: str) -> str:
    """Converts markdown output to basic styled HTML."""
    html = text.replace('\n', '<br>')
    html = re.sub(r'##\s*(.*?)(<br>|$)', r'<h3>\1</h3>', html)
    html = re.sub(r'#\s*(.*?)(<br>|$)', r'<h2>\1</h2>', html)
    return html
