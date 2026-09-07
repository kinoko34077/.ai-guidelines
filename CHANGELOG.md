# Changelog

## 2026-09-07 — Usability独立化後の監査指摘を反映

- 新規UIの実装後に `get_review_checklists('all')` を呼ぶ導線を、入口ルーターとMCPのタスク取得結果へ追加した。
- `UI_UX_POLICY.md` はUsabilityの正本を `USABILITY_POLICY.md` へ委譲し、画面構造・視覚表現との接続に責務を絞った。
- Accessibility検収へFocus Not Obscured、D&D代替、Redundant Entry、色以外の状態伝達、keyboard trap、zoom/text scaling、hover/focus content、IMEを追加した。
- ファイルパスの補正は対象プラットフォームと入力元が明確な場合だけ行い、異なるOSの構文や正当な文字を無条件変換しないようにした。

## 2026-09-07 — Usability責務の独立化

- 恒久的な上位原則を `guidelines/USABILITY_POLICY.md` に分離した。
- 操作経路、状態・文脈継承、回復性、効率、慣習、フォーム、検索、一覧、Dialog、永続化、IME等の具体規約を `07_USABILITY_BASELINE.md` に整理した。
- UI実装前のUsability inferenceと、実装後のExpected interaction / Continuity / Recovery / Efficiency / Conventionによる検収を `01_AGENT_PROTOCOL.md` から呼び出すようにした。
- 既存のレビューを `08_REVIEW_CHECKLIST.md`、Handoffを `09_HANDOFF_PROMPT.md` へ移動し、MCPのタスク別取得対象と入口ルーターを更新した。

## 2026-09-07 — ユーザビリティ評価軸と操作完全性の組込み

- 「GUI操作性の分析考察」をもとに、ユーザビリティを機能の有無ではなく、目的達成の有効性・効率・予測可能性・回復可能性・アクセシビリティで評価する規約を追加した。
- OS・一般GUI・同種アプリで定着した「当然期待される操作」を、対象タスクに適用可能か確認する要求源として明文化した。
- `03A_INTERACTION_BASELINE.md` と `07_REVIEW_CHECKLIST.md` に、実装した機能だけでなく欠落操作、状態・文脈の喪失、失敗からの回復を検収する項目を追加した。
- 指示最適化の方針に合わせ、操作経路や検証を無条件の必須事項にせず、対象タスク・変更範囲・安全境界に応じて参照・適用する構成を維持した。承認範囲と完了条件も分離した。

## 2026-09-07 — UI/UXガイドラインの監査・候補版作成・置換

### 1. 先行チャット資料と現行資料の監査

- 指定された「KiNoTch.2 - 妥当性考察と要約」チャットを参照した。
- このディレクトリ内のガイドライン、UI/UXプロトコルパック、MCPサーバーを確認した。
- 先行資料の中核である次の方針を採用した。
  - 必要な資料へのルーティングを残し、無関係な資料の一律読み込みを避ける。
  - プロジェクト固有知識、安全境界、専門知識、必要な検証は削除しない。
  - テスト量・承認・作業手順は、タスク範囲と環境条件に応じて定義する。
  - 完了条件と承認範囲を分ける。
  - Astra専用と決めつけず、別モデル利用の可能性を残す。

### 2. 置換前の計画

- 現行ファイルを直接編集せず、差し替え候補を別ディレクトリで作成する方針を決定した。
- 変更は候補版との比較、構文・動作検証、人間確認を経てから正式位置へ置換することにした。

### 3. 候補版 v2 の作成

`_candidate_v2/` に、次の候補を作成した。

- `uiux_vibecoding_protocol_pack_v1/00_START_HERE.md`
- `uiux_vibecoding_protocol_pack_v1/01_AGENT_PROTOCOL.md`
- `uiux_vibecoding_protocol_pack_v1/08_HANDOFF_PROMPT.md`
- `uiux_vibecoding_protocol_pack_v1/prompts/COPY_ME_FIRST.txt`
- `guidelines_mcp.py`
- `guidelines/UI_UX_POLICY.md`

主な変更内容:

- 新規UI、既存UI改善、UIレビュー、方針策定、設定作成のフローを分岐した。
- ワイヤーフレームを、画面骨格が未確定な新規UIに限定した。
- UIレビューや設定作成に実装を要求しないようにした。
- 質問・検収・ワイヤーフレームを変更範囲に応じて適用する形にした。
- MCPは、作業種別が既知ならタスク別資料を取得し、未確定時だけ軽量bootstrapを使うようにした。
- 直接操作、CRUD回避、Undo/Redo、即時反映、インライン編集、自動補正を無条件の命令から条件付きの設計判断へ変更した。
- 安全境界、アクセシビリティ、標準操作経路、未確認事項の報告は維持した。

### 4. 候補版の検証とプッシュ

- 差分の空白エラーがないことを確認した。
- MCPの `get_bootstrap`、`get_guidelines_for_task('coding')`、`get_guidelines_for_task('ui_review')` を実行確認した。
- 候補版をコミットし、`origin/main` へプッシュした。
- コミット: `a6327c4 Add candidate v2 guideline revisions`

### 5. 最終照合と正式置換

- 先行チャットの結論と候補版を再照合した。
- 先行資料が求める「資料の存在と読む条件の分離」「安全境界の維持」「タスク依存の検証」「承認範囲と完了条件の分離」に反していないことを確認した。
- 置換前の現行6ファイルをバックアップした。
- バックアップ先: `C:\Users\kinok\AppData\Local\Temp\ai-guidelines-before-v2-20260907`
- 候補版6ファイルを正式位置へ置換した。
- 置換後に候補版と正式ファイルのSHA-256が一致することを確認した。

### 6. 置換後の検証

- `guidelines_mcp.py` のPython AST解析: 成功
- JSONファイルの構文解析: 成功
- MCPセットアップ状態: ready
- `get_bootstrap`: 入口文書1件を取得
- `coding`資料取得: 2件を取得
- `ui_review`資料取得: 7件を取得
- Git差分の空白チェック: 成功

候補版 `_candidate_v2/` は、置換内容の比較・追跡用として残している。今回の置換では、プロジェクト固有の専門知識や安全制約を削除していない。実際の各リポジトリ環境での本番接続、実機UI、別モデルごとの挙動、改善効果の実測は未確認である。
