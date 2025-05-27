"""Convert PDF to JSON using markitdown after removing headers and footers."""

import os
import sys
from src.pdf_parser import load_pdf
from src.markitdown_wrapper import run_markitdown
from src.output_writer import write_json

INPUT_PDF = os.path.join("samples", "AUTOSAR_RS_Diagnostics.pdf")
OUTPUT_JSON = "output/rs_markitdown.json"

if __name__ == "__main__":
    pdf_path = INPUT_PDF
    out_path = OUTPUT_JSON

    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    if len(sys.argv) > 2:
        out_path = sys.argv[2]

    if not os.path.exists(pdf_path):
        sys.exit(f"Input PDF not found: {pdf_path}")

    pages = load_pdf(pdf_path, remove_header=True, remove_footer=True)
    text = "\n".join(pages)

    json_data = run_markitdown(text)

    write_json(json_data, out_path)
    print(f"Conversion completed -> {out_path}")
