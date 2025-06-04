# coding: utf-8
from autosar_atlas_parser.pdf_parser import load_pdf
from autosar_atlas_parser.block_extractor import extract_blocks
from autosar_atlas_parser.rs_parser import parse_requirement_block
from autosar_atlas_parser.output_writer import write_json
from autosar_atlas_parser.trace_parser import parse_trace_table
from autosar_atlas_parser.section_detector import detect_sections
import argparse
import os

INPUT_PDF = os.path.join("samples", "AUTOSAR_RS_Diagnostics.pdf")
OUTPUT_JSON_DIAG = "output/rs_diagnostics.json"
OUTPUT_JSON_TRACE = "output/rs_trace.json"

DEFAULT_INPUT_PDF = INPUT_PDF
DEFAULT_OUTPUT_DIR = os.path.dirname(OUTPUT_JSON_DIAG)

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

def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Parse AUTOSAR specification PDF")
    parser.add_argument(
        "pdf",
        nargs="?",
        default=DEFAULT_INPUT_PDF,
        help="Input AUTOSAR PDF file",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to write output JSON files",
    )
    opts = parser.parse_args(args)

    input_pdf = opts.pdf
    output_dir = opts.output_dir
    os.makedirs(output_dir, exist_ok=True)

    out_diag = os.path.join(output_dir, os.path.basename(OUTPUT_JSON_DIAG))
    out_trace = os.path.join(output_dir, os.path.basename(OUTPUT_JSON_TRACE))

    # Load full pages for section detection
    pages_full = load_pdf(input_pdf, remove_header=False)

    # セクションをPDF内容から動的に検出
    # フォントサイズに基づく見出し解析で各セクションを特定する
    ranges = detect_sections(pages_full, pdf_path=input_pdf, return_indices=True)

    # Load header-trimmed pages for actual parsing
    pages = load_pdf(input_pdf, remove_header=True)

    (title_range, toc_range, doc_range, trace_range) = ranges
    title_section = pages[title_range[0]:title_range[1]]
    doc_section = pages[doc_range[0]:doc_range[1]]
    trace_section = pages[trace_range[0]:trace_range[1]]

    # RS_Diag 要件抽出
    diag_blocks = extract_blocks(doc_section, start_page=0)
    diag_parsed = [parse_requirement_block(b) for b in diag_blocks]

    # タイトル情報を抽出して結合
    metadata = extract_metadata(title_section[0])
    combined_output = {
        "metadata": metadata if any(metadata.values()) else None,
        "requirements": diag_parsed,
    }
    write_json(combined_output, out_diag)

    # RS_Main トレース表抽出
    trace_text = "\n".join(trace_section)
    trace_entries = parse_trace_table(trace_text)
    write_json(trace_entries, out_trace)
    print(f"RS_Diag 抽出完了: {len(diag_parsed)} 件 → {out_diag}")


if __name__ == "__main__":
    main()
