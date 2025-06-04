import re

def parse_trace_table(text):
    """
    トレースセクションの縦並びテキストを解析して RS_Main → RS_Diag マッピングを抽出。
    """
    entries = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    current_entry = None
    description_lines = []
    for line in lines:
        if re.match(r"\[RS_Main_\d{5}\]", line):
            # 直前のエントリを保存
            if current_entry:
                current_entry["description"] = " ".join(description_lines).strip()
                entries.append(current_entry)
            # 新しいエントリ開始
            tag = re.search(r"RS_Main_\d{5}", line).group()
            current_entry = {"tag": tag, "description": "", "satisfied_by": []}
            description_lines = []
        elif re.findall(r"RS_Diag_\d{5}", line):
            if current_entry:
                current_entry["satisfied_by"].extend(re.findall(r"RS_Diag_\d{5}", line))
        elif current_entry:
            description_lines.append(line)
    # 最後のエントリ追加
    if current_entry:
        current_entry["description"] = " ".join(description_lines).strip()
        entries.append(current_entry)
    return entries
