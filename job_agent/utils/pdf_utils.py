import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text from a PDF and returns it as a plain string.
    Preserves basic line breaks and formatting.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()
    return text.strip()