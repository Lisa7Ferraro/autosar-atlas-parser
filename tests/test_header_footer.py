import re
from pathlib import Path

import fitz
import pytest

pdfplumber = pytest.importorskip("pdfplumber")

from src.header_footer import create_header_footer_stripper


def _create_pdf(path: Path, *, pages: int = 3, landscape: bool = False) -> None:
    doc = fitz.open()
    for i in range(pages):
        if landscape:
            page = doc.new_page(width=842, height=595)
        else:
            page = doc.new_page(width=595, height=842)
        page.insert_text((50, 30), "HEADER TEXT", fontsize=10)
        page.insert_text((50, 100), f"Body {i+1}", fontsize=12)
        page.insert_text((50, page.rect.height - 30), str(i + 1), fontsize=10)
    doc.save(path)
    doc.close()


def test_strip_header_footer_portrait(tmp_path: Path) -> None:
    pdf_path = tmp_path / "portrait.pdf"
    _create_pdf(pdf_path, pages=3, landscape=False)

    with pdfplumber.open(pdf_path) as pdf:
        stripper = create_header_footer_stripper(pdf.pages)
        texts = [stripper(p) for p in pdf.pages]

    for idx, text in enumerate(texts, start=1):
        assert "HEADER TEXT" not in text
        assert not re.search(rf"^\s*{idx}\s*$", text.splitlines()[-1])
        assert f"Body {idx}" in text


def test_strip_header_footer_landscape(tmp_path: Path) -> None:
    pdf_path = tmp_path / "landscape.pdf"
    _create_pdf(pdf_path, pages=2, landscape=True)

    with pdfplumber.open(pdf_path) as pdf:
        stripper = create_header_footer_stripper(pdf.pages)
        texts = [stripper(p) for p in pdf.pages]

    for idx, text in enumerate(texts, start=1):
        assert "HEADER TEXT" not in text
        assert not re.search(rf"^\s*{idx}\s*$", text.splitlines()[-1])
        assert f"Body {idx}" in text
