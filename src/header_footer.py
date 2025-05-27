"""Header and footer removal utilities using pdfplumber."""

from __future__ import annotations

from collections import defaultdict
from statistics import median
from typing import Callable, List, Tuple

import pdfplumber


def _collect_lines(page: pdfplumber.page.Page, *, x_tol: float = 1.5, y_tol: float = 3) -> List[Tuple[float, str]]:
    """Extract text lines with their top positions."""
    words = page.extract_words(x_tolerance=x_tol, y_tolerance=y_tol, keep_blank_chars=False)
    lines: defaultdict[float, List[Tuple[float, str]]] = defaultdict(list)
    for w in words:
        top = round(w["top"], 1)
        lines[top].append((w["x0"], w["text"]))
    results = []
    for top, wds in lines.items():
        line_text = " ".join(text for _, text in sorted(wds))
        if line_text.strip():
            results.append((top, line_text.strip()))
    return results


def create_header_footer_stripper(
    pages: List[pdfplumber.page.Page], *, threshold: float = 0.8
) -> Callable[[pdfplumber.page.Page], str]:
    """Detect repeating header/footer lines and return a stripping function."""
    line_positions: defaultdict[str, List[float]] = defaultdict(list)
    page_count = len(pages)

    for page in pages:
        for top, text in _collect_lines(page):
            norm_y = top / float(page.height)
            line_positions[text].append(norm_y)

    repeating: List[Tuple[str, float]] = []
    for text, ys in line_positions.items():
        if len(ys) >= threshold * page_count:
            med = median(ys)
            if max(abs(y - med) for y in ys) <= 0.02:
                repeating.append((text, med))

    def strip_header_footer(page: pdfplumber.page.Page) -> str:
        lines = _collect_lines(page)
        cleaned = []
        for top, text in lines:
            norm_y = top / float(page.height)
            if any(text == rep_text and abs(norm_y - rep_y) <= 0.02 for rep_text, rep_y in repeating):
                continue
            cleaned.append(text)
        return "\n".join(cleaned)

    return strip_header_footer

