import re


def detect_sections(pages):
    """Detect document sections based on page contents.

    Returns tuple of (title_section, toc_section, doc_section, trace_section).
    The function attempts to locate the Table of Contents and Requirements
    Tracing sections dynamically. If not found, it falls back to default
    page ranges. The RS_Diag section may extend a few pages beyond the
    trace section start to capture requirements spanning multiple pages.
    """
    title_idx = 0
    toc_start, toc_end = None, None
    trace_start, trace_end = None, None

    for i, text in enumerate(pages):
        if toc_start is None and "Table of Contents" in text:
            toc_start = i
        elif toc_start is not None and toc_end is None and "1 Introduction" in text:
            toc_end = i
        if "Requirements Tracing" in text and toc_end is not None and i > toc_end:
            trace_start = i
            trace_end = min(i + 3, len(pages))  # trace section up to 3 pages long
            break

    toc_start = toc_start or 5
    toc_end = toc_end or 11
    trace_start = trace_start or 69
    trace_end = trace_end or 72

    title_section = pages[title_idx:title_idx + 1]
    toc_section = pages[toc_start:toc_end]
    # Extend RS_Diag a few pages past the trace start to capture cross-page blocks
    doc_section = pages[toc_end:trace_end]
    trace_section = pages[trace_start:trace_end]

    return title_section, toc_section, doc_section, trace_section
