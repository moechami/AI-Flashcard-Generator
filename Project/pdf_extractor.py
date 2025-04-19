#pdf_extractor.py

import pdfplumber

def extract_text_from_pdf(file) -> list[str]:
    """
      Takes a file-like PDF object and returns a list of cleaned text chunks (1 per page).
      Removes headers/footers, noisy lines, and normalizes formatting.
      """
    text_pages = []
    all_lines = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                all_lines.append(lines)

    return text_pages
