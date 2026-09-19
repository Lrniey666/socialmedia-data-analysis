# 分析方法與發現

語言：[繁體中文](analysis.md) · [English](analysis.en.md)

這頁寫公開樹實際做了什麼。主 README 只放結論表與圖。

## 問題

在 **2022-01-01 到 2022-12-31**，Hololive 官方 YouTube 頻道的上傳，若發佈日落在日本、美國或印尼的公開假日，觀看、喜歡、留言的中位數是否不同？

這是描述性對照，不是「假日導致觀看上升」的因果設計。發片節奏、企劃檔期、推薦演算法都可能同時變動。

## 資料

| 表 | 欄位 | 處理 |
| --- | --- | --- |
| `data/YouTube/Hololive.csv` | title, publishedDate, tags, views, likes, comments | 先 `drop_duplicates`，再切 2022 |
| `data/Google Calendar/JP_holidays.csv` 等 | date, holiday name | 三國日期做成集合 |
| `data/YouTube/CalliopeMori.csv` | 無 tags 欄 | 只作對照，不進主結論 |

原 CSV 有重複列（同一支影片寫了三次）。不去重會灌水 n。

假日旗標：

```text
is_holiday = publishedDate ∈ (JP dates ∪ US dates ∪ ID dates)
```

原 R 稿把三國表 `rbind` 後 `left_join`。1 月 1 日這類重疊日會讓同一支影片在假日組出現多次。公開稿不再爆列。TW、UK 表保留供延伸，預設不合併。

## 發現（官方頻道，2022）

去重後 197 支上傳：假日 51、非假日 146。聯集假日日數 62 天。

| 指標 | 假日 | 非假日 |
| --- | ---: | ---: |
| 觀看中位數 | 288,606 | 286,457 |
| 觀看平均 | 635,514 | 522,421 |
| 喜歡中位數 | 17,415 | 15,787 |
| 留言中位數 | 319 | 353 |

平均被少數爆款拉高；**中位數幾乎沒有假日差**。Tukey 1.5 IQR 修剪後觀看中位數仍接近（279,940 vs 271,144）。

可重跑：

```bash
python src/analysis/yt_holiday_summary.py
```

輸出：`data/derived/holiday_engagement_2022.csv`、`docs/assets/views-boxplot.svg`、`docs/assets/median-comparison.svg`。

## 對照：Mori Calliope，2022

同一套假日旗標、221 支上傳（假日 33、非假日 188）。觀看中位數假日 249,536、非假日 180,345。人才頻道的假日差比官方綜合頻道明顯。這不是主結論，只說明「官方頻道沒差」不能外推到每個 talent。

## 限制

- 觀看數是擷取當下的累積值，不是上線 24 小時的流量。
- 「假日」跨三個時區與文化；觀眾不在同一套日曆上放假。
- 沒有做檢定、也沒有依內容類型分層（3D 直播 vs 短動畫）。
- 本 Repository 不重現 X 對照。那條線依賴本機推文庫，見 [`../local/README.md`](../local/README.md)。

## 半成品（本機）

`local/analysis/yt_data_and_x_data.R` 曾嘗試用 tags 做 YouTube × X 模糊比對，`stringdist` 寫了兩套未收斂的 join。Showcase Repository 不把它當成完成分析。
