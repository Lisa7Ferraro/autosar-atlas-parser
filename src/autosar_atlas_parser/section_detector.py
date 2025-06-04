import fitz
import re


def _get_page_heading(page) -> str:
    """Return heading text for a page based on largest font size."""
    text_dict = page.get_text("dict")
    heading = ""
    max_size = 0.0
    for block in text_dict.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            line_text = "".join(span.get("text", "") for span in line.get("spans", []))
            if not line_text.strip():
                continue
            line_size = max(span.get("size", 0) for span in line.get("spans", []))
            if line_size > max_size:
                max_size = line_size
                heading = line_text.strip()
    return heading


def detect_sections(pages, *, pdf_path: str | None = None, return_indices: bool = False):
    """Detect document sections based on page contents.

    Parameters
    ----------
    pages : list[str]
        Page texts in order.
    return_indices : bool, optional
        When ``True``, return index ranges instead of text slices.

    Returns
    -------
    tuple
        When ``return_indices`` is ``False`` (default), returns a tuple of
        (title_section, toc_section, doc_section, trace_section) each as a
        list of strings. When ``True``, returns their index ranges as
        ``(start, end)`` pairs.
    """
    title_idx = 0
    toc_start, doc_start = None, None
    trace_start, trace_end = None, None

    headings = []
    if pdf_path:
        doc = fitz.open(pdf_path)
        headings = [_get_page_heading(page) for page in doc]
        doc.close()
    else:
        headings = ["" for _ in pages]

    for i, heading in enumerate(headings):
        if toc_start is None and re.search(r"Table of Contents", heading, re.I):
            toc_start = i
        elif doc_start is None and re.search(r"Requirements Specification", heading, re.I):
            doc_start = i
        elif trace_start is None and re.search(r"Requirements tracing", heading, re.I):
            trace_start = i
            trace_end = min(i + 3, len(pages))
            break

    if toc_start is not None and doc_start is None:
        # Fallback end of TOC if Requirements Specification heading missing
        doc_start = toc_start + 1
    if doc_start is not None and trace_start is None:
        trace_start = len(pages)
        trace_end = len(pages)
    

    if return_indices:
        return (
            (title_idx, title_idx + 1),
            (toc_start, doc_start),
            (doc_start, trace_start),
            (trace_start, trace_end),
        )

    title_section = pages[title_idx:title_idx + 1]
    toc_section = pages[toc_start:doc_start]
    # Extend RS_Diag a few pages past the trace start to capture cross-page blocks
    doc_section = pages[doc_start:trace_start]
    trace_section = pages[trace_start:trace_end]

    return title_section, toc_section, doc_section, trace_section
