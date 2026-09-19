"""Summarise 2022 Hololive YouTube engagement on public holidays.

Writes:
  data/derived/holiday_engagement_2022.csv
  docs/assets/views-boxplot.svg
  docs/assets/median-comparison.svg

Run from the repository root:

    python src/analysis/yt_holiday_summary.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
HOLIDAY_FILES = (
    ROOT / "data" / "Google Calendar" / "JP_holidays.csv",
    ROOT / "data" / "Google Calendar" / "USA_holidays.csv",
    ROOT / "data" / "Google Calendar" / "ID_holidays.csv",
)
YT_FILE = ROOT / "data" / "YouTube" / "Hololive.csv"
START = pd.Timestamp("2022-01-01").date()
END = pd.Timestamp("2022-12-31").date()


def load_holiday_dates() -> set:
    frames = [pd.read_csv(path) for path in HOLIDAY_FILES]
    holidays = pd.concat(frames, ignore_index=True)
    holidays["date"] = pd.to_datetime(holidays["date"]).dt.date
    return set(holidays["date"])


def load_videos() -> pd.DataFrame:
    videos = pd.read_csv(YT_FILE).drop_duplicates()
    videos["date"] = pd.to_datetime(videos["publishedDate"]).dt.date
    return videos.loc[(videos["date"] >= START) & (videos["date"] <= END)].copy()


def tukey_box(series: pd.Series) -> dict[str, float]:
    q1 = float(series.quantile(0.25))
    q3 = float(series.quantile(0.75))
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    whisker_low = float(series[series >= low].min())
    whisker_high = float(series[series <= high].max())
    return {
        "n": float(len(series)),
        "q1": q1,
        "median": float(series.median()),
        "q3": q3,
        "whisker_low": whisker_low,
        "whisker_high": whisker_high,
        "mean": float(series.mean()),
    }


def write_summary(holiday: pd.DataFrame, other: pd.DataFrame) -> Path:
    rows = []
    for name, frame in (("holiday", holiday), ("non_holiday", other)):
        rows.append(
            {
                "group": name,
                "n": len(frame),
                "views_median": int(frame["views"].median()),
                "views_mean": int(frame["views"].mean()),
                "likes_median": int(frame["likes"].median()),
                "comments_median": int(frame["comments"].median()),
            }
        )
    out = ROOT / "data" / "derived" / "holiday_engagement_2022.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    return out


def _yscale(value: float, vmin: float, vmax: float, top: float, bottom: float) -> float:
    import math

    lo, hi = math.log10(vmin), math.log10(vmax)
    return bottom - (math.log10(value) - lo) / (hi - lo) * (bottom - top)


def write_boxplot(holiday: pd.Series, other: pd.Series, dest: Path) -> None:
    boxes = {"Non-holiday": tukey_box(other), "Holiday": tukey_box(holiday)}
    vmin, vmax = 50_000, 2_000_000
    top, bottom = 70, 310
    centres = {"Non-holiday": 230, "Holiday": 470}
    fill = {"Non-holiday": "#94a3b8", "Holiday": "#0f766e"}

    ticks = [50_000, 100_000, 200_000, 500_000, 1_000_000, 2_000_000]
    grid = []
    for tick in ticks:
        y = _yscale(tick, vmin, vmax, top, bottom)
        label = f"{tick // 1000}k" if tick < 1_000_000 else f"{tick // 1_000_000}M"
        grid.append(
            f'<line x1="110" y1="{y:.1f}" x2="620" y2="{y:.1f}" stroke="#e2e8f0"/>'
            f'<text x="100" y="{y + 4:.1f}" text-anchor="end" class="axis">{label}</text>'
        )

    bodies = []
    for name, stats in boxes.items():
        x = centres[name]
        y1 = _yscale(stats["q3"], vmin, vmax, top, bottom)
        y2 = _yscale(stats["q1"], vmin, vmax, top, bottom)
        ymed = _yscale(stats["median"], vmin, vmax, top, bottom)
        yw1 = _yscale(stats["whisker_high"], vmin, vmax, top, bottom)
        yw2 = _yscale(stats["whisker_low"], vmin, vmax, top, bottom)
        bodies.append(
            f'<line x1="{x}" y1="{yw1:.1f}" x2="{x}" y2="{yw2:.1f}" stroke="#14201c" stroke-width="1.6"/>'
            f'<line x1="{x - 18}" y1="{yw1:.1f}" x2="{x + 18}" y2="{yw1:.1f}" stroke="#14201c" stroke-width="1.6"/>'
            f'<line x1="{x - 18}" y1="{yw2:.1f}" x2="{x + 18}" y2="{yw2:.1f}" stroke="#14201c" stroke-width="1.6"/>'
            f'<rect x="{x - 42}" y="{y1:.1f}" width="84" height="{y2 - y1:.1f}" rx="4" fill="{fill[name]}" />'
            f'<line x1="{x - 42}" y1="{ymed:.1f}" x2="{x + 42}" y2="{ymed:.1f}" stroke="#f8fafc" stroke-width="3"/>'
            f'<text x="{x}" y="338" text-anchor="middle" class="label">{name}</text>'
            f'<text x="{x}" y="356" text-anchor="middle" class="muted">n = {int(stats["n"])}</text>'
        )

    dest.write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 380" role="img" aria-labelledby="title desc">
  <title id="title">Views on holiday versus other days</title>
  <desc id="desc">Tukey box plots of Hololive official YouTube views in 2022.</desc>
  <style>
    .bg {{ fill: #f3f6f4; }}
    .title {{ fill: #14201c; font: 700 20px "Segoe UI", "Helvetica Neue", sans-serif; }}
    .sub {{ fill: #5b6b66; font: 400 13px "Segoe UI", "Helvetica Neue", sans-serif; }}
    .axis, .label {{ fill: #14201c; font: 500 13px "Segoe UI", "Helvetica Neue", sans-serif; }}
    .muted {{ fill: #5b6b66; font: 400 12px "Segoe UI", "Helvetica Neue", sans-serif; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #121816; }}
      .title, .axis, .label {{ fill: #e8eeea; }}
      .sub, .muted {{ fill: #9aa8a3; }}
    }}
  </style>
  <rect class="bg" width="700" height="380" rx="20"/>
  <text x="36" y="36" class="title">Hololive official uploads, 2022</text>
  <text x="36" y="56" class="sub">Views · Tukey box (log scale) · holiday = JP ∪ US ∪ ID public calendars</text>
  {''.join(grid)}
  {''.join(bodies)}
</svg>
''',
        encoding="utf-8",
    )


def write_medians(holiday: pd.DataFrame, other: pd.DataFrame, dest: Path) -> None:
    metrics = [
        ("Views", int(other["views"].median()), int(holiday["views"].median())),
        ("Likes", int(other["likes"].median()), int(holiday["likes"].median())),
        ("Comments", int(other["comments"].median()), int(holiday["comments"].median())),
    ]
    bars = []
    y = 92
    for label, non, hol in metrics:
        width_non = 220
        width_hol = 220 * hol / non if non else 0
        bars.append(
            f'<text x="36" y="{y}" class="label">{label} median</text>'
            f'<text x="36" y="{y + 22}" class="muted">Non-holiday {non:,}</text>'
            f'<rect x="200" y="{y + 8}" width="{width_non}" height="14" rx="4" fill="#94a3b8"/>'
            f'<text x="36" y="{y + 54}" class="muted">Holiday {hol:,}</text>'
            f'<rect x="200" y="{y + 40}" width="{width_hol:.1f}" height="14" rx="4" fill="#0f766e"/>'
        )
        y += 88

    dest.write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 380" role="img" aria-labelledby="title desc">
  <title id="title">Median engagement comparison</title>
  <desc id="desc">Median views, likes and comments for holiday and other days.</desc>
  <style>
    .bg {{ fill: #f3f6f4; }}
    .title {{ fill: #14201c; font: 700 20px "Segoe UI", "Helvetica Neue", sans-serif; }}
    .sub {{ fill: #5b6b66; font: 400 13px "Segoe UI", "Helvetica Neue", sans-serif; }}
    .label {{ fill: #14201c; font: 650 14px "Segoe UI", "Helvetica Neue", sans-serif; }}
    .muted {{ fill: #5b6b66; font: 400 12px "Segoe UI", "Helvetica Neue", sans-serif; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #121816; }}
      .title, .label {{ fill: #e8eeea; }}
      .sub, .muted {{ fill: #9aa8a3; }}
    }}
  </style>
  <rect class="bg" width="520" height="380" rx="20"/>
  <text x="36" y="36" class="title">Median engagement</text>
  <text x="36" y="56" class="sub">197 unique 2022 uploads · 51 holiday / 146 other days</text>
  {''.join(bars)}
</svg>
''',
        encoding="utf-8",
    )


def main() -> None:
    dates = load_holiday_dates()
    videos = load_videos()
    videos["is_holiday"] = videos["date"].isin(dates)
    holiday = videos.loc[videos["is_holiday"]]
    other = videos.loc[~videos["is_holiday"]]

    assets = ROOT / "docs" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    summary = write_summary(holiday, other)
    write_boxplot(holiday["views"], other["views"], assets / "views-boxplot.svg")
    write_medians(holiday, other, assets / "median-comparison.svg")
    print(f"videos={len(videos)} holiday={len(holiday)} other={len(other)}")
    print(f"wrote {summary.relative_to(ROOT)}")
    print("wrote docs/assets/views-boxplot.svg")
    print("wrote docs/assets/median-comparison.svg")


if __name__ == "__main__":
    main()
