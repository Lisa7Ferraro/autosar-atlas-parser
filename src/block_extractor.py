import re


def extract_blocks(pages, start_page=13):
    """
    ページテキストのリストを受け取り、RS_Diagブロック単位で抽出する。
    出力は tag, content, page_range (1-based, inclusive) を含む辞書のリスト。
    """
    blocks = []
    current_block = None
    current_text = []
    current_start_page = None

    for i, page_text in enumerate(pages):
        page_num = i + 1
        if page_num <= start_page:
            continue

        lines = page_text.splitlines()
        for line in lines:
            tag_match = re.match(r"\[(RS_Diag_\d{5})\]\s*(.*)", line)
            if tag_match:
                if current_block:
                    blocks.append({
                        "tag": current_block,
                        "content": "\n".join(current_text).strip(),
                        "page_range": (current_start_page, page_num - 1 if current_start_page != page_num else page_num)
                    })
                current_block = tag_match.group(1)
                current_text = [line]
                current_start_page = page_num
            elif current_block:
                current_text.append(line)

    if current_block:
        blocks.append({
            "tag": current_block,
            "content": "\n".join(current_text).strip(),
            "page_range": (current_start_page, page_num)
        })

    return blocks
