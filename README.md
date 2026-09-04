# RUBY BEAR — 架空ジャムブランド LP（v2）

参考: [Hungry Tiger style (Refero)](https://styles.refero.design/style/47f15da7-8905-45b3-bcab-06a4277c6168) / https://www.eathungrytiger.com

## 起動

```bash
node .claude/serve.js
```

http://localhost:8765 を開く。

## 構成（シンプル版）

1. Hero（1000vh ピン留め）— 瓶が回転しながら落下 → 着地 → 蓋が回って外れる → ジャムが溢れて流れ落ちる。背景にテロップ 6 枚
2. Our story（一枚看板 + ピル）
3. Pick your flavor（透過 PNG/WebP の瓶 3 種）
4. Footer

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

## スクロールタイムライン（進行度 0→1）

| 進行度 | 映像 | テロップ |
|---|---|---|
| 0.00–0.14 | 空 → 瓶が上から回転落下 | SWEET RIOT |
| 0.12–0.30 | 落下・回転 | FRUIT 62% |
| 0.28–0.46 | 減速・着地 | HALF THE SUGAR |
| 0.44–0.60 | 着地して静止 | COPPER POT |
| 0.58–0.76 | 蓋が回って浮く | NO PECTIN / NO FLAVORING |
| 0.76–1.00 | ジャムが溢れて流れ落ちる | CRACK IT OPEN + CTA |

テロップは `.telop` の `data-in` / `data-out` で調整。デスクトップでは見出し 2 行を瓶の左右に振り分け、日本語 1 行を瓶の下に固定。

## 生成ログ（Higgsfield MCP・全て事前にコスト確認）

| 用途 | モデル | クレジット |
|---|---|---|
| v1: 画像 7 枚 + 動画 2 本 | nano_banana_2 / minimax_h3 | 32.5 |
| v2: 緑バック瓶 1 枚 | nano_banana_2 | 2 |
| v2: 背景除去 3 枚 | Image Background Remover | 1 × 3 |
| v2: 落下動画（6s）+ 蓋開き動画（6s） | minimax_h3 | 12 × 2 |
| v3: アイコン 2 案（緑バック生成 → ローカルでキー抜き・2色化） | nano_banana_2 | 1.5 × 2 = 3 |
| v2+v3 小計（残高 643 → 611） | | 32 |
