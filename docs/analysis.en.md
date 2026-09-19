# Method and findings

Language: [繁體中文](analysis.md) · [English](analysis.en.md)

This page is what the public tree actually does. The main README only keeps the table and figures.

## Question

Between **2022-01-01 and 2022-12-31**, did Hololive official YouTube uploads posted on a Japan, United States or Indonesia public holiday show different median views, likes or comments?

This is a descriptive contrast, not a causal design that “holidays raise views”. Scheduling, campaign calendars and the recommender can all move at once.

## Data

| Table | Columns | Treatment |
| --- | --- | --- |
| `data/YouTube/Hololive.csv` | title, publishedDate, tags, views, likes, comments | De-duplicate, then keep 2022 |
| `data/Google Calendar/JP_holidays.csv` and siblings | date, holiday name | Build a three-country date set |
| `data/YouTube/CalliopeMori.csv` | no tags column | Contrast only; not in the headline |

The raw official CSV repeats rows (the same video written three times). Skipping de-duplication inflates *n*.

Holiday flag:

```text
is_holiday = publishedDate ∈ (JP dates ∪ US dates ∪ ID dates)
```

The original R draft `rbind`-ed the three calendars and `left_join`-ed. Overlapping days such as 1 January counted the same video more than once. The public draft does not explode rows. TW and UK tables remain for extensions and are not merged by default.

## Findings (official channel, 2022)

197 unique uploads: 51 holiday, 146 other days. The union calendar has 62 holiday dates.

| Measure | Holiday | Other days |
| --- | ---: | ---: |
| Median views | 288,606 | 286,457 |
| Mean views | 635,514 | 522,421 |
| Median likes | 17,415 | 15,787 |
| Median comments | 319 | 353 |

Means are pulled by a few hits. **Medians barely move.** After a Tukey 1.5 IQR trim, median views stay close (279,940 vs 271,144).

Replay:

```bash
python src/analysis/yt_holiday_summary.py
```

Outputs: `data/derived/holiday_engagement_2022.csv`, `docs/assets/views-boxplot.svg`, `docs/assets/median-comparison.svg`.

## Contrast: Mori Calliope, 2022

Same flag, 221 uploads (33 holiday, 188 other). Median views 249,536 on holidays versus 180,345 on other days. A single talent channel can show a holiday gap that the official omnibus channel does not. That is not the headline; it warns against generalising.

## Limits

- View counts are cumulative at scrape time, not first-day traffic.
- “Holiday” spans three time zones and cultures; viewers do not share one calendar.
- No hypothesis test, and no split by format (3D live versus short animation).
- The X contrast is not reproduced here. That line needs the local tweet library; see [`../local/README.md`](../local/README.md).

## Draft (local only)

`local/analysis/yt_data_and_x_data.R` tried a fuzzy tag join between YouTube and X. Two `stringdist` attempts never settled. The showcase does not treat that file as a finished analysis.
