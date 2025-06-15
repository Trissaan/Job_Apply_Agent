import os
import pdfkit
from pdfminer.high_level import extract_text

WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

def generate_pdf_from_text(resume_text: str, filename: str = "resume.pdf", out_dir: str = "./temp") -> str:
    os.makedirs(out_dir, exist_ok=True)

    # Save as temporary HTML
    html_path = os.path.join(out_dir, "temp_resume.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head><meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; font-size: 12pt; white-space: pre-wrap; padding: 2em; }}
        </style>
        </head>
        <body><pre>{resume_text}</pre></body>
        </html>
        """)

    pdf_path = os.path.join(out_dir, filename)

    # ✅ Move config inside function
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    pdfkit.from_file(html_path, pdf_path, configuration=config)

    return pdf_path

def save_resume_as_text(resume_text: str, filename: str = "resume.txt", out_dir: str = "./temp") -> str:
    os.makedirs(out_dir, exist_ok=True)
    txt_path = os.path.join(out_dir, filename)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(resume_text)
    return txt_path


def extract_text_from_pdf(file_path: str) -> str:
    try:
        return extract_text(file_path).strip()
    except Exception as e:
        print(f" Failed to extract text from PDF: {e}")
        return ""