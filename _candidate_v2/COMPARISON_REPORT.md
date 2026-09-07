# Candidate v2 比較・検証レポート

## 対象と目的

この候補版は、既存の専門知識・安全境界・アクセシビリティ基準を維持したまま、作業種別に無関係な手順の強制、過剰な資料読み込み、実行フローの矛盾を減らすための差し替え案である。

|現行ファイル|候補ファイル|変更の要点|
|---|---|---|
|`uiux_vibecoding_protocol_pack_v1/00_START_HERE.md`|`uiux_vibecoding_protocol_pack_v1/00_START_HERE.md`|作業種別ごとの分岐を明記。新規UIだけが条件付きでワイヤーフレームへ進み、UIレビュー・方針策定・設定作成は実装を強制しない。|
|`uiux_vibecoding_protocol_pack_v1/01_AGENT_PROTOCOL.md`|`uiux_vibecoding_protocol_pack_v1/01_AGENT_PROTOCOL.md`|実装前ゲート、質問、ワイヤーフレーム、検収を変更規模・未確定事項に応じて適用する。|
|`uiux_vibecoding_protocol_pack_v1/08_HANDOFF_PROMPT.md`|`uiux_vibecoding_protocol_pack_v1/08_HANDOFF_PROMPT.md`|依頼側が範囲・完了条件を渡せる起動文に整理し、UIレビューへ実装を要求しない。|
|`uiux_vibecoding_protocol_pack_v1/prompts/COPY_ME_FIRST.txt`|`uiux_vibecoding_protocol_pack_v1/prompts/COPY_ME_FIRST.txt`|入口・条件付き質問・条件付き検収だけを短く案内する。|
|`guidelines_mcp.py`|`guidelines_mcp.py`|既知の作業はタスク別取得を優先し、未確定のときだけ軽量bootstrapを使う。|
|`guidelines/UI_UX_POLICY.md`|`guidelines/UI_UX_POLICY.md`|直接操作、CRUD回避、Undo/Redo、即時反映、インライン編集、自動補正を一律強制せず、目的・影響・安全性・実装可能性で選ぶ。|

## 維持したこと

- UI作業では入口から作業種別を判定し、必要資料だけを参照する。
- PC優先の業務・管理・編集UIで、情報密度、操作階層、アクセシビリティを重視する。
- 危険操作は影響と回復可否に応じて分離し、confirm又はundoを用意する。
- UIの実装・変更では、変更範囲に応じてアクセシビリティとUIの検収を行う。
- 実行できない検収は推測で合格にせず、未確認理由を報告する。
- ユーザーの明示指示、既存仕様、安全境界を優先する。

## 検証結果

- 6ファイルの候補差分に空白エラーなし。
- 候補版のMCPを、現行の規約ルートを読み取り専用で参照する形で実行確認した。
- `get_bootstrap()` は入口文書1件と利用可能な作業種別を返した。
- `get_guidelines_for_task('coding')` はコーディング・仕様規約だけを返した。
- `get_guidelines_for_task('ui_review')` はUIレビューに必要な資料だけを返した。
- 現行の追跡済みファイルには変更がない。候補ファイルはこの `_candidate_v2/` にのみ存在する。

## 置換前の確認事項

- 他モデルも同じ規約を使う場合、条件化した表現で期待する最低限の誘導が保たれるか。
- 実プロジェクトでMCPを接続し、候補版を規約ルートにした状態のUIタスクを1件試行するか。
- 実際の本番接続・テストデータ・外部操作の境界は、各リポジトリ側の指示で明示するか。

現時点では、現行ファイルの置換は行わない。
