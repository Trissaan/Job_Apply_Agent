from fpdf import FPDF
import os

def save_cover_letter_as_pdf(text, filename="cover_letter.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    os.makedirs("temp_docs", exist_ok=True)
    filepath = os.path.join("temp_docs", filename)
    pdf.output(filepath)
    return filepath
