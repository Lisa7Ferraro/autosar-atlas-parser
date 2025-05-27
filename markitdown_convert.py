"""Convert PDF to JSON using markitdown after removing headers and footers."""

from src.pdf_parser import load_pdf
from src.markitdown_wrapper import run_markitdown
from src.output_writer import write_json
import os

INPUT_PDF = os.path.join("samples", "AUTOSAR_RS_Diagnostics.pdf")
OUTPUT_JSON = "output/rs_markitdown.json"

if __name__ == "__main__":
    # Remove header and footer then join pages
    pages = load_pdf(INPUT_PDF, remove_header=True, remove_footer=True)
    text = "\n".join(pages)

    # Convert using markitdown
    json_data = run_markitdown(text)

    write_json(json_data, OUTPUT_JSON)
    print(f"Conversion completed -> {OUTPUT_JSON}")
