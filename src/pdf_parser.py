import fitz  # PyMuPDF

def load_pdf(path: str) -> list:
    """
    ページ単位でテキストを読み込む。
    空白や改行の崩れを最小限に抑えて、忠実な文章構造を保持する。
    """
    doc = fitz.open(path)
    pages = [page.get_text("text") for page in doc]
    return pages
