# coding: utf-8
from src.pdf_parser import load_pdf
from src.block_extractor import extract_blocks
from src.rs_parser import parse_requirement_block
from src.output_writer import write_json
from src.trace_parser import parse_trace_table
from src.section_detector import detect_sections
import os

INPUT_PDF = os.path.join("samples", "AUTOSAR_RS_Diagnostics.pdf")
OUTPUT_JSON_DIAG = "output/rs_diagnostics.json"
OUTPUT_JSON_TRACE = "output/rs_trace.json"

def extract_metadata(title_page_text):
    """
    タイトルページからメタ情報を抽出する（縦並び構造対応）
    Document Title
    Requirements on Diagnostics
    Document Status
    published
    ... のような構造に対応
    """
    metadata = {
        "document_title": None,
        "document_status": None,
        "part_of_standard": None,
        "release_version": None
    }
    lines = [line.strip() for line in title_page_text.splitlines() if line.strip()]
    for i in range(len(lines) - 1):
        key = lines[i].lower()
        value = lines[i + 1].strip()
        if key == "document title":
            metadata["document_title"] = value
        elif key == "document status":
            metadata["document_status"] = value
        elif key == "part of autosar standard":
            metadata["part_of_standard"] = value
        elif key == "part of standard release":
            metadata["release_version"] = value
    return metadata

if __name__ == "__main__":
    # Load full pages for section detection
    pages_full = load_pdf(INPUT_PDF, remove_header=False)

    # セクションをPDF内容から動的に検出
    # フォントサイズに基づく見出し解析で各セクションを特定する
    ranges = detect_sections(pages_full, pdf_path=INPUT_PDF, return_indices=True)

    # Load header-trimmed pages for actual parsing
    pages = load_pdf(INPUT_PDF, remove_header=True)

    (title_range, toc_range, doc_range, trace_range) = ranges
    title_section = pages[title_range[0]:title_range[1]]
    toc_section = pages[toc_range[0]:toc_range[1]]
    doc_section = pages[doc_range[0]:doc_range[1]]
    trace_section = pages[trace_range[0]:trace_range[1]]

    # RS_Diag 要件抽出
    diag_blocks = extract_blocks(doc_section, start_page=0)
    diag_parsed = [parse_requirement_block(b) for b in diag_blocks]

    # タイトル情報を抽出して結合
    metadata = extract_metadata(title_section[0])
    combined_output = {
        "metadata": metadata if any(metadata.values()) else None,
        "requirements": diag_parsed
    }
    write_json(combined_output, OUTPUT_JSON_DIAG)

    # RS_Main トレース表抽出
    trace_text = "\n".join(trace_section)
    trace_entries = parse_trace_table(trace_text)
    write_json(trace_entries, OUTPUT_JSON_TRACE)
    print(f"RS_Diag 抽出完了: {len(diag_parsed)} 件 → {OUTPUT_JSON_DIAG}")
