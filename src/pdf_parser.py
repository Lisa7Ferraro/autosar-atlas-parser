"""PDF reading utilities."""

import fitz  # PyMuPDF


def load_pdf(
    path: str,
    *,
    remove_header: bool = False,
    remove_footer: bool = False,
    header_margin: float = 50,
    footer_margin: float = 50,
) -> list:
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
    remove_footer : bool, optional
        If ``True``, remove the footer area from each page.
    header_margin : float, optional
        Height in PDF points to exclude from the top of each page.
    footer_margin : float, optional
        Height in PDF points to exclude from the bottom of each page.

    Returns
    -------
    list[str]
        Text content of each page.
    """

    doc = fitz.open(path)
    pages = []
    for page in doc:
        top = header_margin if remove_header else 0
        bottom = page.rect.height - footer_margin if remove_footer else page.rect.height
        clip = fitz.Rect(0, top, page.rect.width, bottom)
        text = page.get_text("text", clip=clip)
        pages.append(text)
    return pages


