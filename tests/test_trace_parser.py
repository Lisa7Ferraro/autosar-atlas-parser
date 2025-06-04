from trace_parser import parse_trace_table


def test_parse_trace_table_mapping():
    text = (
        "[RS_Main_00011] Mechanisms for Reliable Systems\n"
        "RS_Diag_04003 RS_Diag_04005\n"
        "[RS_Main_00012] Another\n"
        "RS_Diag_04006"
    )
    entries = parse_trace_table(text)
    assert entries[0]['tag'] == 'RS_Main_00011'
    assert entries[0]['satisfied_by'] == ['RS_Diag_04003', 'RS_Diag_04005']
    assert entries[1]['tag'] == 'RS_Main_00012'
    assert entries[1]['satisfied_by'] == ['RS_Diag_04006']

