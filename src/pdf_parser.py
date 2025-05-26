import pdfplumber
import re

def load_pdf(path: str) -> list:
    """
    ページ単位でテキストを読み込み、ハイフネーションや改行を補正して返す。
    タグ行（[RS_Diag_XXXXX]）の検出を妨げないように改行は制限的に処理する。
    """
    with pdfplumber.open(path) as pdf:
        pages = []
        for page in pdf.pages:
            text = page.extract_text() or ""
            # ハイフン＋改行は1単語にする
            text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
            # 改行はスペースに変換（ただしタグ行の直後やその周囲は除く）
            lines = text.splitlines()
            new_lines = []
            for line in lines:
                # タグ行はそのまま
                if re.match(r"\[RS_Diag_\d{5}\]", line.strip()):
                    new_lines.append(line)
                else:
                    # 単語の途中改行の補正
                    line = re.sub(r'(\w)\n(\w)', r'\1 \2', line)
                    new_lines.append(line.replace('\n', ' '))
            cleaned = "\n".join(new_lines)
            pages.append(cleaned)
        return pages

import fitz  # PyMuPDF

def load_pdf(path: str) -> list:
    """
    ページ単位でテキストを読み込む。
    空白や改行の崩れを最小限に抑えて、忠実な文章構造を保持する。
    """
    doc = fitz.open(path)
    pages = [page.get_text("text") for page in doc]
    return pages