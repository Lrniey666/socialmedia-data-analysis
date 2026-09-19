# 安裝與重抓

語言：[繁體中文](installation.md) · 步驟與根目錄 README 相同；此頁補 API 細節。  
English (UK) notes are in the second half.

## 重跑公開分析（不必金鑰）

倉裡已有 2022 中介 CSV。

```bash
python -m pip install -r requirements.txt
python src/analysis/yt_holiday_summary.py
```

可選 R：

```bash
Rscript src/analysis/packages.R
Rscript src/analysis/yt_data_and_holidays.R
```

`r-packages.txt` 列出套件名。`packages.R` 會向 `https://cloud.r-project.org` 補齊缺件。

## 重抓 YouTube

1. 在 Google Cloud 開專案，啟用 **YouTube Data API v3**，建立 API key。
2. 複製 `config.example/youtube.json` 成 `secrets/youtube.json`，填入 `API_KEY`。
3. 在專案根目錄執行：

```bash
python src/fetching/youtube.py
```

預設頻道是 Hololive 官方（`UCJFZiqLMntJufDCHc6bQixg`）。輸出寫到 `data/YouTube/video_details.csv`（此檔已被 gitignore，避免蓋掉展示用的歷史快照）。要更新展示用的 `Hololive.csv`，請先比對列數再手動覆寫。

配額：uploads playlist 分頁 + `videos.list` 每 50 支一批。整頻道歷史會吃掉每日額度，請分次或提高配額。

## 重抓假日曆

1. 建立 OAuth **Desktop** 用戶端，下載 JSON。
2. 複製成 `secrets/google_calendar_credentials.json`（格式見 `config.example/`）。
3. 執行 `python src/fetching/google_calendar.py`。第一次會開瀏覽器；token 寫入 `secrets/google_calendar_token.json`。

腳本預設抓英國 2022 年日曆並寫回 `data/Google Calendar/UK_holidays.csv`。改 `main()` 裡的 calendar id 可抓 JP／US／ID／TW。日曆 id 是 Google 公開假日曆，不是私人行事曆。

## 請不要

- 提交 `secrets/` 或任何 token
- 把 `local/` 推進公開分支
- 把登入式 X 蒐集器寫進安裝主路徑

---

## Installation notes (UK English)

Replaying the public analysis needs no keys: install `requirements.txt` and run `yt_holiday_summary.py`. R is optional (`src/analysis/packages.R`).

YouTube: enable Data API v3, copy `config.example/youtube.json` to `secrets/youtube.json`, run `src/fetching/youtube.py`. The default channel is the Hololive official uploads playlist. Fresh output lands on the gitignored `video_details.csv` so the 2022 showcase snapshot stays put until you overwrite it on purpose.

Holidays: an OAuth desktop client, then `src/fetching/google_calendar.py`. The first run opens a browser. Calendar identifiers are Google’s public holiday calendars. The default write-back is the 2022 UK table.

Do not commit `secrets/`, `local/`, or a login-based X collector as the documented happy path.
