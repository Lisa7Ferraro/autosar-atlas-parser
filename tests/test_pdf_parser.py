import os
from autosar_atlas_parser.pdf_parser import load_pdf

def test_load_pdf_clips_header(tmp_path):
    src_pdf = os.path.join(os.path.dirname(__file__), 'fixtures', 'header.pdf')
    pages_with_header = load_pdf(src_pdf, remove_header=False)
    assert any('HEADER' in page for page in pages_with_header)

    pages_no_header = load_pdf(src_pdf, remove_header=True, header_margin=50)
    assert 'HEADER' not in pages_no_header[0]

