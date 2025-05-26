"""PDF reading utilities."""

import fitz  # PyMuPDF
import pdfplumber

def _load_with_plumber(path: str, header_margin: float) -> list:
    """Load PDF text with ``pdfplumber`` while removing header regions.

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
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            bbox = (0, header_margin, page.width, page.height)
            cropped = page.within_bbox(bbox)
            text = cropped.extract_text() or ""
            pages.append(text)
    return pages

def load_pdf(path: str, *, remove_header: bool = True, header_margin: float = 50) -> list:
    """Read a PDF and return page texts.

    Parameters
    ----------
    path : str
        Path to the PDF file.
    remove_header : bool, optional
        When ``True`` (default), attempt to exclude header areas from each page.
    header_margin : float, optional
        Header height in points to remove when ``remove_header`` is ``True``.

    Returns
    -------
    list[str]
        Text content of each page.
    """
    if remove_header:
        try:
            return _load_with_plumber(path, header_margin)
        except Exception:
            # Fallback to basic text extraction
            pass

    doc = fitz.open(path)
    pages = [page.get_text("text") for page in doc]
    return pages
