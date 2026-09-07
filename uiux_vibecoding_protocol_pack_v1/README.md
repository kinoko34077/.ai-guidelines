# UI/UX Vibe Coding Protocol Pack v1

## 使い方
1. このフォルダごとコーディングAIへ渡す。
2. まず `prompts/COPY_ME_FIRST.txt` の文面を貼る。
3. AIに `00_START_HERE.md` を最初に読むよう指定する。
4. 新規UIならモック案、既存UIならレビュー、思想策定なら質問票へ進める。
5. 実装前は必要に応じて `07_USABILITY_BASELINE.md` を参照し、実装後は `06_ACCESSIBILITY_CHECKLIST.md` と `08_REVIEW_CHECKLIST.md` で自己検収させる。

## フォルダ構成
- `00_START_HERE.md`: 最初に読む入口。
- `01_AGENT_PROTOCOL.md`: AIの実行手順。
- `02_DEFAULT_UI_POLICY.md`: 既定UI思想。
- `03_DECISION_QUESTION_BANK.md`: 発火条件つき質問集。
- `07_USABILITY_BASELINE.md`: 操作効率、慣習、状態継承、直接操作、回復性、暗黙期待の標準規約。
- `04_COMPONENT_RULES.md`: ボタン、フォーム、テーブル等の規約。
- `05_LAYOUT_RULES.md`: レイアウト規約。
- `06_ACCESSIBILITY_CHECKLIST.md`: アクセシビリティ検収。
- `08_REVIEW_CHECKLIST.md`: UIレビュー検収。
- `09_HANDOFF_PROMPT.md`: AIへ最初に渡す文面。
- `templates/`: モック、レビュー、質問要約などのテンプレート。
- `schemas/`: ui_policy / ui_config のJSON Schema。
- `project/`: プロジェクトごとの回答・設定サンプル。
- `reference/`: 調査ダイジェスト。最上位命令ではない。
