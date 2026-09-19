# 貢獻指南

語言：[繁體中文](CONTRIBUTING.md) · [English](docs/CONTRIBUTING.en.md)

這是 2023 課程資料管線的封存 Showcase Repository。歡迎修文件、補重跑註記、在**公開**分析上加檢定。請先當歷史作業看，再動手。

## 動工前

1. 讀根目錄 [`README.md`](README.md) 與 [`docs/analysis.md`](docs/analysis.md)。
2. 改數字或圖時，重跑 `python src/analysis/yt_holiday_summary.py`，並核對 README 表格。
3. 衝突時：**可重跑的公開結果 > 舊 R 互動稿的記憶**。原稿在 `local/`，不要為了「看起來完整」把半成品搬回 `src/`。

## 慣例

| 項目 | 約定 |
| --- | --- |
| 對外說明 | 繁中在 `README.md`；英文在 `docs/README.en.md`，兩邊一起改 |
| 日期 | `YYYY-MM-DD`，台北時間 |
| 變更紀錄 | `CHANGELOG.md` 的 `## [Unreleased]`（Keep a Changelog 2.0.0） |
| 換行 | LF（`.gitattributes`） |
| 英文 | English（licence, analysed, behaviour） |

## 請不要

- 提交 `local/`（除了已被追蹤的 `local/README.md`）、`secrets/`、token、推文全文
- 提交 `chromedriver.exe` 或其他瀏覽器驅動
- 把登入爬蟲寫成安裝主路徑或「建議做法」
- 在程式裡硬寫本機絕對路徑或真實 API key
- 主張本 Repository 與 COVER / hololive 有官方關係

不可逆的動作（force push、把本機推文庫打進歷史）請先問。

## 改完必做

1. Notable 變更寫進 `CHANGELOG.md` → `## [Unreleased]`
2. 動到 Hero／安裝／結構／數字 → 繁中與英文 README 一起改
3. 若改了假日定義，同步 [`docs/analysis.md`](docs/analysis.md) 與 [`docs/analysis.en.md`](docs/analysis.en.md)
