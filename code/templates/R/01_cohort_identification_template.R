# 01 — Cohort identification (worked example)
#
# This is the one fully worked R template in this project. It demonstrates the CLIF idiom end to
# end; steps 02–04 are skeletons for you to fill in.
#
# Run from the PROJECT ROOT, e.g.:
#     Rscript code/01_cohort_identification_template.R
#
# What it does:
#   1. Load config + the tables this project needs (errors clearly if one is missing)
#   2. Build a simple cohort  (EDIT the criteria for your project)
#   3. Save patient-level working data to output/intermediate_phi/  (NEVER shared, git-ignored)
#   4. Save a shareable aggregate to output/final_no_phi/           (no row-level data, every cell n >= 10)

library(here)
library(tidyverse)
library(arrow)

# 1. Configuration — reads config/config.json (see config/README.md).
#    config.json defaults to the bundled clif_demo/ dataset, so this runs out of the box;
#    point data_directory at your CLIF tables for a real run.
source("utils/config.R")
data_directory <- config$data_directory
filetype       <- config$filetype

# Helper: read a CLIF table by name, with a clear error if the file is missing.
read_clif_table <- function(name) {
  path <- file.path(data_directory, paste0("clif_", name, ".", filetype))
  if (!file.exists(path)) stop("Missing required CLIF table: ", path)
  if (filetype == "parquet") {
    collect(open_dataset(path))
  } else if (filetype == "csv") {
    read_csv(path, show_col_types = FALSE)
  } else {
    stop("Unsupported filetype: ", filetype, " (use 'csv' or 'parquet')")
  }
}

hospitalization <- read_clif_table("hospitalization")
adt             <- read_clif_table("adt")

# 2. Build the cohort — EDIT these criteria for your project.
start_date <- as.Date("2020-01-01")
end_date   <- as.Date("2021-12-31")

inpatient_ids <- adt %>%
  filter(location_category %in% c("Ward", "ICU")) %>%
  distinct(hospitalization_id) %>%
  pull(hospitalization_id)

cohort <- hospitalization %>%
  filter(as.Date(admission_dttm) >= start_date,
         as.Date(admission_dttm) <= end_date,
         age_at_admission >= 18,
         hospitalization_id %in% inpatient_ids)

message("Cohort: ", n_distinct(cohort$hospitalization_id), " hospitalizations")

# 3. Save patient-level working data (git-ignored, never leaves your site).
dir.create(here("output", "intermediate_phi"), showWarnings = FALSE, recursive = TRUE)
write_parquet(cohort, here("output", "intermediate_phi", "cohort.parquet"))

# 4. Save a shareable aggregate — never report cells with n < 10 (re-identification risk).
dir.create(here("output", "final_no_phi"), showWarnings = FALSE, recursive = TRUE)
cohort_summary <- cohort %>%
  mutate(age_group = cut(age_at_admission, breaks = c(18, 40, 65, Inf),
                         right = FALSE, labels = c("18-39", "40-64", "65+"))) %>%
  group_by(age_group) %>%
  summarise(n_hospitalizations = n_distinct(hospitalization_id), .groups = "drop") %>%
  filter(n_hospitalizations >= 10)   # data-security rule
write_csv(cohort_summary, here("output", "final_no_phi", "cohort_summary.csv"))
message("Wrote ", nrow(cohort_summary), " aggregate row(s) to output/final_no_phi/")
