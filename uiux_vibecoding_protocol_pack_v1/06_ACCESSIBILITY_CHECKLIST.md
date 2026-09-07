# 06_ACCESSIBILITY_CHECKLIST: アクセシビリティ検収

## 1. 基準
本チェックリストはWCAG 2.2 AA相当を目標とする。完全な法的適合証明ではなく、AI実装時に最低限の崩壊を防ぐための検収用である。

## 2. 必須チェック
|項目|確認内容|NG例|
|---|---|---|
|Keyboard|Tabで主要操作へ到達できるか|クリック必須の隠し操作|
|Focus visible|フォーカス位置が見えるか|outline: noneのみ|
|Focus not obscured|フォーカスがsticky header、dialog、toast等に隠れないか|フォーカス先が画面外や固定領域の下|
|Label|inputにvisible labelがあるか|placeholderだけ|
|Name/Role/Value|button, input, dialog等が機械可読か|div onclickだけ|
|Icon button|tooltipとaria-labelがあるか|ゴミ箱アイコンだけ|
|Contrast|本文4.5:1、非テキスト3:1目安|薄灰色文字、薄い境界|
|Target size|最低24px、タッチ主体なら44px目安|小さすぎるクリック領域|
|Error|エラー箇所と理由が分かるか|赤枠だけ|
|Status|保存中/完了/失敗が伝わるか|視覚だけ、読み上げ不可|
|Reflow|狭幅や拡大時に破綻しないか|横スクロール必須のフォーム|
|色以外の情報|色だけに状態・エラー・必須を依存していないか|赤色だけでエラー表示|
|Dragging alternative|D&Dに依存する操作へキーボード又はボタン等の代替があるか|ドラッグだけで並べ替え|
|Redundant entry|同一セッションで既知の情報を再入力させないか|同じ住所を再入力|
|Keyboard trap|dialogやwidgetからキーボードで脱出できるか|Tabが閉じた領域に閉じ込められる|
|Zoom/Text scaling|拡大・文字サイズ変更で内容や操作が欠落しないか|拡大でボタンが隠れる|
|Hover/Focus content|hover/focusで出る内容がキーボードでも確認・閉じられるか|hoverでしか読めないtooltip|
|IME/Input method|IME変換中の入力、確定、エラー表示を壊さないか|変換途中で送信・消去|

## 3. 実装ルール
- `<button>` を使える場所で `<div role="button">` に逃げない。
- icon-only buttonには `aria-label` を付ける。
- decorative iconには `aria-hidden="true"` を付ける。
- dialogはfocus trap、escape close、初期focus、aria-modalを考慮する。
- focus trapを使う場合は、Escape又は明示的な閉じる操作でdialog外へ戻れるようにする。
- error messageは対象inputと関連付ける。
- loadingやsave statusは `role="status"` またはaria-liveを検討する。
- D&D、hover、色、音、pointer gestureだけが唯一の操作・状態伝達にならないよう代替を用意する。
- focus順、focus位置、ズーム、文字サイズ変更、IME変換中の状態を実行環境で確認し、未確認なら理由を記録する。

## 4. 完了報告
検収結果は「OK/修正/未確認」で出す。未確認が残る場合は、なぜ未確認かを明記する。
