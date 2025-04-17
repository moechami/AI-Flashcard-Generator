#pdf_extractor.py

import pdfplumber

def extract_text_from_pdf(file) -> list[str]:
    """
    Takes a file-like PDF object and returns a list of text chunks (1 per page).
    """
    text_pages = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_pages.append(text.strip())

    return text_pages
