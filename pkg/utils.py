import io
import binascii
from typing import List, Dict

import pypdf
from pypdf import PdfReader


def convert_pdf_to_text(pdf: Dict[str, any]) -> List[Dict[str, str]]:
    pdf_bytes_io = io.BytesIO(pdf["bytes"])

    try:
        pdf_doc = PdfReader(pdf_bytes_io)
    except pypdf.errors.PdfStreamError:
        # Skip pdfs that are not readable.
        return []

    pages = []
    for page in pdf_doc.pages:
        try:
            pages.append({"text": page.extract_text()})
        except binascii.Error:
            # Skip all pages that are not parsable due to malformed character.
            print("parsing failed")
    return pages


def convert_md_to_text(md: Dict[str, any]) -> List[Dict[str, str]]:
    return [{"text": str(md["bytes"], encoding="utf-8")}]
