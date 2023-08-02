import io
import binascii
from typing import List, Dict

import pypdf
from pypdf import PdfReader


# TODO: LangChain can be used instead once
# https://github.com/hwchase17/langchain/pull/3915 is merged.
def convert_to_text(pdf: Dict[str, any]) -> List[Dict[str, str]]:
    pdf_bytes_io = io.BytesIO(pdf["bytes"])

    try:
        pdf_doc = PdfReader(pdf_bytes_io)
    except pypdf.errors.PdfStreamError:
        # Skip pdfs that are not readable.
        # We still have over 30,000 pages after skipping these.
        return []

    pages = []
    for page in pdf_doc.pages:
        try:
            pages.append({"text": page.extract_text()})
        except binascii.Error:
            # Skip all pages that are not parsable due to malformed character.
            print("parsing failed")
    return pages
