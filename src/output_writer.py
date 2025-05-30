import json
import os

def write_json(data: list, output_path: str):
    """
    パース済みデータ（リスト）を JSON ファイルに保存する。
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
