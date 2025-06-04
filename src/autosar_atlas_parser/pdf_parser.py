"""PDF reading utilities."""

import fitz  # PyMuPDF


def load_pdf(path: str, *, remove_header: bool = False, header_margin: float = 50) -> list:
    """Load PDF pages as text.

    When ``remove_header`` is ``True``, the top ``header_margin`` points of each
    page are excluded using PyMuPDF's clipping functionality.  Previously
    pdfplumber was used in conjunction with PyMuPDF, but this combination caused
    page offsets to become inconsistent.  The implementation now relies solely on
    PyMuPDF to keep page indices stable.

    Parameters
    ----------
    path : str
        Path to the PDF file.
    remove_header : bool, optional
        If ``True``, remove the header area from each page.
    header_margin : float, optional
        Height in PDF points to exclude from the top of each page.

    Returns
    -------
    list[str]
        Text content of each page.
    """

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


