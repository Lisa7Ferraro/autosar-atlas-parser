import re


def detect_sections(pages, *, return_indices: bool = False):
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

    if return_indices:
        return (
            (title_idx, title_idx + 1),
            (toc_start, toc_end),
            (toc_end, trace_end),
            (trace_start, trace_end),
        )

    title_section = pages[title_idx:title_idx + 1]
    toc_section = pages[toc_start:toc_end]
    # Extend RS_Diag a few pages past the trace start to capture cross-page blocks
    doc_section = pages[toc_end:trace_end]
    trace_section = pages[trace_start:trace_end]

    return title_section, toc_section, doc_section, trace_section
