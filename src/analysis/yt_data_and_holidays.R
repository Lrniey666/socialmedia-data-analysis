# Holiday vs non-holiday engagement — Hololive official YouTube, 2022.
# Run from the repository root:
#   Rscript src/analysis/packages.R
#   Rscript src/analysis/yt_data_and_holidays.R
#
# A date is a holiday if it appears on the JP, US, or ID public calendar
# (the three markets used in the original coursework). Videos are
# de-duplicated first so a multi-country holiday does not explode the join.

library(pacman)
p_load("dplyr", "ggplot2", "this.path", "readr")

root <- file.path(dirname(this.path()), "..", "..")
setwd(root)

yt_data <- read.csv("./data/YouTube/Hololive.csv") |>
  unique()

holidays <- bind_rows(
  read.csv("./data/Google Calendar/JP_holidays.csv"),
  read.csv("./data/Google Calendar/USA_holidays.csv"),
  read.csv("./data/Google Calendar/ID_holidays.csv")
)
holidays$date <- as.Date(holidays$date)
holiday_dates <- unique(holidays$date)

names(yt_data)[names(yt_data) == "publishedDate"] <- "date"
yt_data$date <- as.Date(yt_data$date)

start_date <- as.Date("2022-01-01")
end_date <- as.Date("2022-12-31")

new_yt_data <- yt_data |>
  filter(date >= start_date, date <= end_date) |>
  mutate(is_holiday = date %in% holiday_dates)

non_holiday_yt_data <- filter(new_yt_data, !is_holiday)
holiday_yt_data <- filter(new_yt_data, is_holiday)

RemoveOutliers <- function(data, column, multiplier = 1.5) {
  values <- data[[column]]
  iqr_val <- IQR(values)
  lower <- quantile(values, 0.25) - multiplier * iqr_val
  upper <- quantile(values, 0.75) + multiplier * iqr_val
  filter(data, .data[[column]] >= lower, .data[[column]] <= upper)
}

non_holiday_trim <- RemoveOutliers(non_holiday_yt_data, "views")
holiday_trim <- RemoveOutliers(holiday_yt_data, "views")

dir.create("./data/derived", showWarnings = FALSE, recursive = TRUE)
dir.create("./docs/assets", showWarnings = FALSE, recursive = TRUE)

summary_tbl <- bind_rows(
  holiday_yt_data |>
    summarise(
      group = "holiday",
      n = n(),
      views_median = median(views),
      views_mean = mean(views),
      likes_median = median(likes),
      comments_median = median(comments)
    ),
  non_holiday_yt_data |>
    summarise(
      group = "non_holiday",
      n = n(),
      views_median = median(views),
      views_mean = mean(views),
      likes_median = median(likes),
      comments_median = median(comments)
    )
)
write_csv(summary_tbl, "./data/derived/holiday_engagement_2022.csv")

plot_data <- bind_rows(
  mutate(non_holiday_yt_data, period = "Non-holiday"),
  mutate(holiday_yt_data, period = "Holiday")
)
plot_data$period <- factor(plot_data$period, levels = c("Non-holiday", "Holiday"))

p <- ggplot(plot_data, aes(x = period, y = views, fill = period)) +
  geom_boxplot(outlier.alpha = 0.25, width = 0.55) +
  scale_y_log10(labels = scales::label_number(scale_cut = scales::cut_short_scale())) +
  scale_fill_manual(values = c("Non-holiday" = "#94a3b8", "Holiday" = "#0f766e")) +
  labs(
    title = "Hololive official uploads, 2022",
    subtitle = "Views on public holidays (JP ∪ US ∪ ID) versus other days",
    x = NULL,
    y = "Views (log10)"
  ) +
  theme_minimal(base_size = 13) +
  theme(legend.position = "none")

ggsave("./docs/assets/views-boxplot.png", p, width = 8, height = 5, dpi = 140)

message("Wrote data/derived/holiday_engagement_2022.csv")
message("Wrote docs/assets/views-boxplot.png")
print(summary_tbl)
print("trimmed (Tukey 1.5 IQR) view medians:")
print(c(
  holiday = median(holiday_trim$views),
  non_holiday = median(non_holiday_trim$views)
))
