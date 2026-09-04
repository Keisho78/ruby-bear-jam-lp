# RUBY BEAR — 架空ジャムブランド LP（v2）

参考: [Hungry Tiger style (Refero)](https://styles.refero.design/style/47f15da7-8905-45b3-bcab-06a4277c6168) / https://www.eathungrytiger.com

## 起動

```bash
node .claude/serve.js
```

http://localhost:8765 を開く。

## 構成（v4: 瓶がセクションを渡り歩く）

1. Journey（`main.journey`）— 瓶のレイヤー（`.stage`、sticky）が画面に留まり、その下を 6 つの説明セクション（`.step`）が上から下へ流れる。参考サイト eathungrytiger.com と同じ構造
   - Hero「SWEET RIOT」（中央）→ 01 FRUIT 62%（文字左・瓶右）→ 02 HALF THE SUGAR（文字右・瓶左）→ 03 COPPER POT（左・右）→ 04 NO PECTIN（右・左）→ CRACK IT OPEN（中央、瓶が手前で蓋開き）
   - 各セクションの中央を通過する時点のフレーム番号を `data-f`、瓶の横位置を `data-x`（vw）、大きさを `data-s` で指定。セクション境界で瓶が滑らかに移動
   - 最終セクションの後半で瓶が沈みながらフェードアウトし、次のセクションが下から入ってくる
2. Pick your flavor（透過 PNG/WebP の瓶 3 種）
3. Footer

## ファイル

- `index.html` — 単一ファイル（CSS / JS 同梱）
- `assets/frames/0000.webp … 0314.webp` + `manifest.json` — 透過アルファ付きフレーム列（660×880、24fps、約 10MB）。canvas に描画してスクロールでスクラブ
- `assets/jar-strawberry|apricot|blueberry.webp/.png` — 背景除去済みの瓶
- `assets/icon.webp/.png` (512), `icon-180.png`, `icon-64.png` — ブランドアイコン（いちごを抱えた熊）。ナビ・ローダー・Story・フッター・ファビコンで使用
- `assets/bg-texture.jpg` — 壁の植物ウォーターマーク（ページ唯一の背景）
- `assets/original/` — Higgsfield の元出力（緑バック動画 2 本、PNG）。Web では未使用
- `.claude/build-frames.py` — 緑バック動画 2 本 → クロマキー → 連結 → WebP 列を書き出すスクリプト
- `.claude/serve.js` — ローカル静的サーバー

## 透過の仕組み（境目が出ない理由）

動画は純緑（#00FF00）背景で生成し、ffmpeg の `chromakey` + `despill` でアルファ化 → WebP（アルファ付き）フレーム列に変換。ページ側は `<video>` ではなく `<canvas>` に透過フレームを描くため、映像の矩形やフラット背景が壁テクスチャの上に出ません。静止画の瓶は Higgsfield の Image Background Remover で切り抜き。

## スクロールタイムライン

| セクション | 瓶の位置 | 到達フレーム |
|---|---|---|
| Hero SWEET RIOT | 中央（まだ空） | 0 |
| 01 FRUIT 62% | 右 22vw・0.84 倍 | 78（回転落下中） |
| 02 HALF THE SUGAR | 左 22vw | 150（着地） |
| 03 COPPER POT | 右 22vw | 172（静止） |
| 04 NO PECTIN / NO FLAVORING | 左 22vw | 236（蓋が浮く） |
| CRACK IT OPEN | 中央・等倍 | 314（ジャム流出） |

スマホ（700px 以下）は瓶を中央やや下に固定し、各セクションの英語見出しを左の縦書き巨大 2 カラム、日本語を右端の小さな縦書きで配置。

## 生成ログ（Higgsfield MCP・全て事前にコスト確認）

| 用途 | モデル | クレジット |
|---|---|---|
| v1: 画像 7 枚 + 動画 2 本 | nano_banana_2 / minimax_h3 | 32.5 |
| v2: 緑バック瓶 1 枚 | nano_banana_2 | 2 |
| v2: 背景除去 3 枚 | Image Background Remover | 1 × 3 |
| v2: 落下動画（6s）+ 蓋開き動画（6s） | minimax_h3 | 12 × 2 |
| v3: アイコン 2 案（緑バック生成 → ローカルでキー抜き・2色化） | nano_banana_2 | 1.5 × 2 = 3 |
| v2+v3 小計（残高 643 → 611） | | 32 |
