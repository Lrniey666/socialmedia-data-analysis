# 文件索引

語言：[繁體中文](../README.md) · [English (UK)](README.en-GB.md)

對外入口是根目錄 [`README.md`](../README.md)。這裡放會把主介紹拉太長的東西。

| 檔案 | 內容 |
| --- | --- |
| [README.en-GB.md](README.en-GB.md) | 與根目錄 README 對等的英式英文 |
| [analysis.md](analysis.md) | 問題、資料、方法、發現、限制 |
| [analysis.en-GB.md](analysis.en-GB.md) | 同上，英式英文 |
| [installation.md](installation.md) | Python／R、API 金鑰、重抓步驟 |
| [CONTRIBUTING.en-GB.md](CONTRIBUTING.en-GB.md) | 貢獻指南英文 |
| [assets/](assets/) | Hero 與示範 SVG |
| [../local/README.md](../local/README.md) | 本機材料清單（目錄其餘不進 git） |

## 為什麼根目錄長這樣

2026-09 盤點原 zip：沒有 git、README 一句話、根目錄有 16 MB `chromedriver.exe`、`data/X_Twitter/` 約 2.6 萬列推文全文、Selenium 登入爬蟲、以及未完成的 YouTube × X tags 對齊。

公開展示需要一條**別人 clone 後能重跑、也不踩平台條款**的路徑。因此：

| 留下 | 分離且不進 git |
| --- | --- |
| YouTube Data API 擷取與 CSV | `local/fetching/x_twitter.py` |
| Google 公開假日曆 CSV | `local/data/X_Twitter/*.csv` |
| 假日旗標分析（Python + R） | `local/analysis/x_data_and_holidays.R` |
| 示範圖與摘要表 | `local/analysis/yt_data_and_x_data.R`（半成品） |
| 雙語說明 | `local/tools/chromedriver.exe` |

本機檔沒有刪。`local/` 仍在作者磁碟上，只是 `.gitignore` 擋住。

## 公開資料範圍

| 來源 | 期間 | 列數（去重後） | 取得方式 |
| --- | --- | ---: | --- |
| Hololive 官方頻道 | 2019-02-19 – 2023-11-13 | 599 | YouTube Data API |
| Mori Calliope | 2020-09-12 – 2023-10-23 | 836 | YouTube Data API |
| JP / US / ID / TW / UK 假日 | 2022 | 16–36 | Google Calendar 公開日曆 |
