# Contributing

Language: [繁體中文](../CONTRIBUTING.md) · [English (UK)](CONTRIBUTING.en-GB.md)

This is an archived 2023 coursework pipeline. Fixes to the docs, replay notes, or a statistical test on the **public** analysis are welcome. Treat it as historical coursework first.

## Before you edit

1. Read [`../README.md`](../README.md) and [`analysis.en-GB.md`](analysis.en-GB.md).
2. If you change a figure or a number, rerun `python src/analysis/yt_holiday_summary.py` and check the README table.
3. On conflict: **repeatable public results beat memories of the old interactive R draft**. The draft lives in `local/`. Do not move unfinished work back into `src/` to look complete.

## Conventions

| Item | Rule |
| --- | --- |
| Public docs | Traditional Chinese in `README.md`; British English in `docs/README.en-GB.md`. Edit both. |
| Dates | `YYYY-MM-DD`, Taipei time |
| Changelog | `CHANGELOG.md` → `## [Unreleased]` (Keep a Changelog 2.0.0) |
| Line endings | LF (`.gitattributes`) |
| English | British English (licence, analysed, behaviour) |

## Please do not

- Commit `local/` (except the tracked `local/README.md`), `secrets/`, tokens, or tweet text
- Commit `chromedriver.exe` or other browser drivers
- Document a login scraper as the happy path
- Hard-code absolute machine paths or live API keys
- Claim an official relationship with COVER / hololive

Ask first before irreversible git (force-push, or stuffing the tweet dump into history).

## After you change something

1. Notable work goes in `CHANGELOG.md` → `## [Unreleased]`
2. Hero / install / structure / numbers → update both READMEs
3. Holiday definition changes → update [`analysis.md`](analysis.md) and [`analysis.en-GB.md`](analysis.en-GB.md)
