
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
    field_regex = {f: re.compile(rf"{f}:(.*?)\s*(?=(?:{'|'.join(fields)}|c\())", re.DOTALL) for f in fields}

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
        "page_range": page_range
    }