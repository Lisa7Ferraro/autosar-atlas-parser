"""PDF reading utilities."""

import fitz  # PyMuPDF
import pdfplumber

def _load_with_plumber(path: str, header_margin: float) -> list:

    """Load PDF text while excluding header regions.


    Parameters
    ----------
    path : str
        Path to the PDF file.
    header_margin : float
        Height in PDF points to exclude from the top of each page.

    Returns
    -------
    list[str]
        Text content of each page with headers removed.
    """
    pages = []

    with pdfplumber.open(path) as plumber_pdf:
        doc = fitz.open(path)
        for fpage, ppage in zip(doc, plumber_pdf.pages):
            width, height = ppage.width, ppage.height
            rect = fitz.Rect(0, header_margin, width, height)
            text = fpage.get_text("text", clip=rect)

            pages.append(text)
    return pages


def load_pdf(path: str, *, remove_header: bool = False, header_margin: float = 50) -> list:

    if remove_header:
        try:
            return _load_with_plumber(path, header_margin)
        except Exception:
            # Fallback to basic text extraction
            pass

    doc = fitz.open(path)
    pages = []
    for page in doc:
        if remove_header:
            clip = fitz.Rect(0, header_margin, page.rect.width, page.rect.height)
            text = page.get_text("text", clip=clip)
        else:
            text = page.get_text("text")
        pages.append(text)
    return pages
