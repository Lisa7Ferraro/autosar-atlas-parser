# coding: utf-8
from src.pdf_parser import load_pdf
from src.block_extractor import extract_blocks
from src.rs_parser import parse_requirement_block
from src.output_writer import write_json
from src.trace_parser import parse_trace_table

INPUT_PDF = "AUTOSAR_RS_Diagnostics.pdf"
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
    pages = load_pdf(INPUT_PDF)

    # セクション分割（ページは0-based index）
    title_section = pages[0:1]       # ページ1
    toc_section = pages[5:11]        # ページ6〜11
    doc_section = pages[11:69]       # ページ12〜69（RS_Diag）
    trace_section = pages[69:72]     # ページ70〜72（RS_Main）

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