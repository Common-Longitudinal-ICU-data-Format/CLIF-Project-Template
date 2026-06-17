"""
01 — Cohort identification (worked example)

This is the one fully worked Python template in this project. It demonstrates the CLIF idiom end to
end; steps 02–04 are skeletons for you to fill in.

Run from the PROJECT ROOT, e.g.:
    uv run python code/01_cohort_identification_template.py

What it does:
  1. Initialize clifpy from config/config.json
  2. Load the tables this project needs
  3. Build a simple cohort  (EDIT the criteria for your project)
  4. Save patient-level working data to output/intermediate_phi/  (NEVER shared, git-ignored)
  5. Save a shareable aggregate to output/final_no_phi/           (no row-level data, every cell n >= 10)
"""

from pathlib import Path

import pandas as pd
from clifpy import ClifOrchestrator

INTERMEDIATE_DIR = Path("output/intermediate_phi")  # patient-level — stays at your site
FINAL_DIR = Path("output/final_no_phi")             # aggregate — safe to share

# 1. Initialize clifpy from the config file (it reads data_directory / filetype / timezone).
#    config.json defaults to the bundled clif_demo/ dataset, so this runs out of the box;
#    point data_directory at your CLIF tables for a real run.
co = ClifOrchestrator(config_path="config/config.json")

# 2. Load the tables this project needs. clifpy raises a clear error if a table is missing.
co.initialize(tables=["patient", "hospitalization", "adt"])
hospitalization = co.hospitalization.df.copy()
adt = co.adt.df.copy()

# 3. Build the cohort — EDIT these criteria for your project.
START_DATE, END_DATE = "2020-01-01", "2021-12-31"
hospitalization["admission_dttm"] = pd.to_datetime(hospitalization["admission_dttm"])

# CLIF category values are lowercase.
inpatient_ids = adt.loc[
    adt["location_category"].isin(["ward", "icu"]), "hospitalization_id"
].unique()

cohort = hospitalization[
    hospitalization["admission_dttm"].between(START_DATE, END_DATE)
    & (hospitalization["age_at_admission"] >= 18)
    & hospitalization["hospitalization_id"].isin(inpatient_ids)
]
print(f"Cohort: {cohort['hospitalization_id'].nunique()} hospitalizations")

# 4. Save patient-level working data (git-ignored, never leaves your site).
INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
cohort.to_parquet(INTERMEDIATE_DIR / "cohort.parquet", index=False)

# 5. Save a shareable aggregate — never report cells with n < 10 (re-identification risk).
FINAL_DIR.mkdir(parents=True, exist_ok=True)
cohort = cohort.assign(
    age_group=pd.cut(
        cohort["age_at_admission"],
        bins=[18, 40, 65, 120],
        right=False,
        labels=["18-39", "40-64", "65+"],
    )
)
summary = (
    cohort.groupby("age_group", observed=True)["hospitalization_id"]
    .nunique()
    .reset_index(name="n_hospitalizations")
)
summary = summary[summary["n_hospitalizations"] >= 10]  # data-security rule
summary.to_csv(FINAL_DIR / "cohort_summary.csv", index=False)
print(f"Wrote {len(summary)} aggregate row(s) to {FINAL_DIR}")
