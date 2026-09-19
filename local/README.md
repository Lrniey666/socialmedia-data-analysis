# Local-only materials / 本機材料

This folder stays on the author’s machine. Git ignores everything here except this file.

這個目錄留在作者本機。除了本檔以外，全部被 `.gitignore` 排除，**不會**進公開 GitHub 樹。

| Path | Why it is local |
| --- | --- |
| `fetching/x_twitter.py` | Login-based X/Twitter collector. Publishing it as the “how to run this repo” path would push readers toward a terms-of-service violation. |
| `data/X_Twitter/*.csv` | Full tweet text and engagement columns. Redistributing the dump is a copyright / platform-policy risk. |
| `analysis/x_data_and_holidays.R` | Exploratory holiday comparison that **depends on the tweet dump**. |
| `analysis/yt_data_and_x_data.R` | Unfinished YouTube × X tag join (fuzzy match left half-written). |
| `tools/chromedriver.exe` | 16 MB Windows binary used only by the local collector. |

The public tree answers a narrower question with official APIs: **did public holidays change Hololive YouTube engagement in 2022?**

public tree 只保留官方 API 能重做的部分：假日是否改變 2022 年 Hololive YouTube 互動量。

Do not add this folder to a public branch, gist, or release archive.
