# Install and load the public analysis stack.
# Run from the repository root:
#   Rscript src/analysis/packages.R

pkgs <- c("pacman", "dplyr", "ggplot2", "this.path", "readr", "scales")

installed <- rownames(installed.packages())
missing <- setdiff(pkgs, installed)
if (length(missing) > 0) {
  install.packages(missing, repos = "https://cloud.r-project.org")
}

invisible(lapply(pkgs, library, character.only = TRUE))
message("R packages ready: ", paste(pkgs, collapse = ", "))
