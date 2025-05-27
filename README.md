# AUTOSAR Atlas Parser

AUTOSAR仕様書（PDF）から要件・トレーサビリティ情報を自動抽出し、JSON形式で出力するOSSツールです。
[AUTOSAR仕様書](https://www.autosar.org/)は著作物のため，ツール実行者が適切にダウンロードしてください

## 開発環境（Dev Container 推奨）
本リポジトリは [Dev Container](https://containers.dev/) 対応です。VS Codeで「Remote - Containers」拡張を使い、`Reopen in Container` で開発環境を自動構築できます。
- Pythonや依存パッケージのセットアップ不要ですぐに解析・開発が可能
- コマンド例：
  1. VS Codeで本リポジトリを開く
  2. コマンドパレットで「Dev Containers: Reopen in Container」を選択

## 特徴
- **セクションごとに異なるパースロジック**：要件セクションとトレースセクションで異なる解析を実施
- **ページまたぎ対応**：1要件が複数ページにまたがる場合も正しく抽出
- **柔軟なJSON出力**：空セルや“–”は`null`や空文字列として許容
- **箇条書き・改行保持**：Description等の改行やリストも維持

## インストール
Python 3.8以降が必要です。

```sh
pip install -r requirements.txt
pip install markitdown  # markitdownがインストールされていない場合
```

## 使い方
1. `samples/`ディレクトリにAUTOSAR PDF（例: `AUTOSAR_RS_Diagnostics.pdf`）を配置する
   - リポジトリには空ディレクトリを保持するため`.gitkeep`が含まれています
   - スクリプトはこの`samples/`フォルダからPDFを読み込みます
2. 以下のコマンドで実行

```sh
python3 main.py
```

ヘッダとフッタを除去した上で [`markitdown`](https://github.com/yuukiw/markitdown)
 を利用してJSON化する場合は次を実行します。

```sh
python3 markitdown_convert.py
```

- `output/rs_markitdown.json`：markitdown で変換した結果
- `output/rs_diagnostics.json`：RS_Diag要件の抽出結果
- `output/rs_trace.json`：RS_Mainトレース表の抽出結果

## JSON出力例
### RS_Diag 要件
```json
{
  "tag": "RS_Diag_04200",
  "title": "Support event combination",
  "description": "The diagnostic in AUTOSAR shall allow combining several individual events...",
  "rationale": "Advanced fault analysis",
  "use_case": "Improved clustering and judging of events...",
  "applies_to": ["CP", "AP"],
  "dependencies": [],
  "supporting_material": null,
  "cross_references": ["RS_Main_00260"]
}
```

### RS_Main 要件（トレーサビリティ表）
```json
{
  "tag": "RS_Main_00011",
  "description": "Mechanisms for Reliable Systems",
  "satisfied_by": ["RS_Diag_04003", "RS_Diag_04005", ...]
}
```


- `src/pdf_parser.py`: PDF読み取り。PyMuPDFで取得し、必要に応じヘッダ領域を除外

- `src/block_extractor.py`: タグ単位のテキストブロック抽出
- `src/rs_parser.py`: 要件ブロックのパース
- `src/output_writer.py`: JSONファイル書き出し
- `src/trace_parser.py`: トレース表パース
- `src/section_detector.py`: フォントサイズから見出しを抽出し各セクションを決定
- `main.py`: セクション単位で処理を組み合わせて実行

## ライセンス
MIT License

## 貢献方法
バグ報告・プルリクエスト歓迎します。詳細は`CONTRIBUTING.md`をご参照ください。
