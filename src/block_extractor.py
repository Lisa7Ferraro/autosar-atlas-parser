import re

def parse_requirement_block(block: dict) -> dict:
    content = block["content"]
    tag = block["tag"]
    page_range = block["page_range"]

    # タイトル抽出
    title_match = re.match(r"\[RS_Diag_\d{5}\]\s*(.*)", content)
    title = title_match.group(1).strip() if title_match else ""

    # 各フィールド抽出用正規表現
    fields = ["Description", "Rationale", "Use Case", "AppliesTo", "Dependencies", "Supporting Material"]
    # フィールド毎に次のフィールド名または文字列終端までを取得する正規表現
    pattern = rf"{{f}}:\s*(.*?)\s*(?=(?:{'|'.join(fields)}|$))"
    field_regex = {f: re.compile(pattern.format(f=f), re.DOTALL) for f in fields}

    def extract_field(name):
        match = field_regex[name].search(content)
        text = match.group(1).strip() if match else ""
        if text in ["–", ""]:
            return None if name in ["Supporting Material"] else ""
        if name in ["AppliesTo", "Dependencies"]:
            return [x.strip() for x in text.split(",") if x.strip()] if text else []
        return text

    # Cross references
    cross_refs = re.findall(r"RS_Main_\d{5}", content)

    return {
        "tag": tag,
        "title": title,
        "description": extract_field("Description"),
        "rationale": extract_field("Rationale"),
        "use_case": extract_field("Use Case"),
        "applies_to": extract_field("AppliesTo"),
        "dependencies": extract_field("Dependencies"),
        "supporting_material": extract_field("Supporting Material"),
        "cross_references": cross_refs,
        "page_range": page_range  # optionalで出力するかは後段で判断
    }


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
