# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-09-19

### Added

- Public showcase layout: bilingual README (zh-Hant / en), docs index, method notes, installation, contributing guide.
- `requirements.txt`, `r-packages.txt`, `src/analysis/packages.R`.
- Repeatable holiday summary: `src/analysis/yt_holiday_summary.py` and a batch-safe `yt_data_and_holidays.R`.
- Demo figures and `data/derived/holiday_engagement_2022.csv`.
- Hollow credential files in `config.example/`.
- `local/README.md` listing materials that stay off git.

### Changed

- Holiday flag is a JP ∪ US ∪ ID date set so overlapping calendars do not explode the join.
- Fetchers resolve paths from the repository root and write Calendar output under `data/Google Calendar/`.

### Fixed

- `get_hoilday` renamed to `get_holiday` in the Calendar collector.

---

[Unreleased]: https://github.com/naritaroad/SocialMediaDataAnalysis/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/naritaroad/SocialMediaDataAnalysis/releases/tag/v0.1.0
