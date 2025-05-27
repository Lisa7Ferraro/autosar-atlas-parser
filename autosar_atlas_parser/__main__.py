from __future__ import annotations

import argparse
from pathlib import Path

from src.block_extractor import extract_blocks
from src.pdf_parser import load_pdf
from src.rs_parser import parse_requirement_block
from src.section_detector import detect_sections
from src.json_emitter import Requirement, emit_jsonl


def _parse_command(pdf_path: str, output_dir: str) -> None:
    pages_full = load_pdf(pdf_path, remove_header=False)
    ranges = detect_sections(pages_full, pdf_path=pdf_path, return_indices=True)
    pages = load_pdf(pdf_path, remove_header=True)
    doc_range = ranges[2]
    doc_section = pages[doc_range[0] : doc_range[1]]

    blocks = extract_blocks(doc_section, start_page=0)
    requirements: list[Requirement] = []
    for b in blocks:
        parsed = parse_requirement_block(b)
        req = Requirement(
            requirement_id=parsed.get("tag", ""),
            section="Diagnostics",
            title=parsed.get("title", ""),
            description=parsed.get("description", ""),
            rationale=parsed.get("rationale", ""),
            use_case=parsed.get("use_case", ""),
            applies_to=parsed.get("applies_to", []),
            dependencies=parsed.get("dependencies", []),
        )
        requirements.append(req)

    out_path = Path(output_dir) / "RS_Diagnostics_v0.1.jsonl"
    emit_jsonl(requirements, str(out_path))
    print(f"Wrote {len(requirements)} requirements to {out_path}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="autosar_atlas_parser")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_p = subparsers.add_parser("parse", help="Parse AUTOSAR PDF")
    parse_p.add_argument("pdf_path", help="Path to AUTOSAR PDF")
    parse_p.add_argument("-o", "--output-dir", default="out", help="Output directory")

    args = parser.parse_args(argv)

    if args.command == "parse":
        _parse_command(args.pdf_path, args.output_dir)


if __name__ == "__main__":
    main()
