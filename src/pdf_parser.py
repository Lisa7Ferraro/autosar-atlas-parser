import fitz  # PyMuPDF

def load_pdf(path: str) -> list:
    """Read a PDF and return a list of page texts.

    Each element in the returned list contains the text of one page.
    """
    doc = fitz.open(path)
    pages = [page.get_text("text") for page in doc]
    return pages
