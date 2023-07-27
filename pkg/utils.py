import io
import binascii

import pypdf
from pypdf import PdfReader


# TODO: LangChain can be used instead once
# https://github.com/hwchase17/langchain/pull/3915 is merged.
def convert_to_text(pdf_bytes: bytes):
    pdf_bytes_io = io.BytesIO(pdf_bytes)

    try:
        pdf_doc = PdfReader(pdf_bytes_io)
    except pypdf.errors.PdfStreamError:
        # Skip pdfs that are not readable.
        # We still have over 30,000 pages after skipping these.
        return []

    text = []
    for page in pdf_doc.pages:
        try:
            text.append(page.extract_text())
        except binascii.Error:
            # Skip all pages that are not parsable due to malformed character.
            print("parsing failed")
    return text
