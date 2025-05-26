"""PDF reading utilities."""

import fitz  # PyMuPDF


def load_pdf(path: str, *, remove_header: bool = False, header_margin: float = 50) -> list:
    """Read a PDF and return page texts.

    Parameters
    ----------
    path : str
        Path to the PDF file.
    remove_header : bool, optional
        When ``True``, exclude the top ``header_margin`` points from each page.
    header_margin : float, optional
        Header height in points to remove when ``remove_header`` is ``True``.

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
