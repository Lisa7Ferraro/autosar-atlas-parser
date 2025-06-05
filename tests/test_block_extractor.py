from autosar_atlas_parser.block_extractor import extract_blocks


def test_extract_blocks_multi_page():
    pages = [
        "[RS_Diag_00001] Req1 Title\nDescription line 1",
        "Continued line 2",
        "[RS_Diag_00002] Req2 Title\nDescription"
    ]
    blocks = extract_blocks(pages, start_page=0)
    assert blocks[0]['tag'] == 'RS_Diag_00001'
    assert blocks[0]['page_range'] == (1, 2)
    assert blocks[1]['tag'] == 'RS_Diag_00002'
    assert blocks[1]['page_range'] == (3, 3)

