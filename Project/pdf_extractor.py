#pdf_extractor.py

import pdfplumber
import re
from collections import Counter

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
        # Detect common headers/footers (top/bottom lines seen on multiple pages)
        line_counts = Counter()
        for lines in all_lines:
            if len(lines) >= 2:
                line_counts[lines[0]] += 1
                line_counts[lines[-1]] += 1

        common_lines = {line for line, count in line_counts.items() if count > 1}

        for lines in all_lines:
            cleaned_lines = []
            for line in lines:
                if line in common_lines:
                    continue
                if len(line) < 30:
                    continue
                line = re.sub(r'\s+', ' ', line)
                cleaned_lines.append(line)
            text_pages.append('\n'.join(cleaned_lines))

    return text_pages
