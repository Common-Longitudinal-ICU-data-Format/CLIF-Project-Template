## Code directory

This is where your project's scripts live. The repository ships starter scripts under
[`templates/`](templates) for both **R** and **Python** — as the project creator you **copy the
language(s) you use into `code/`** (see the [Creator Guide](../guides/creator-guide.md)), then adapt
them.

> [!NOTE]
> **These templates are suggestions, not requirements.** They exist to make it easy to follow a
> shared convention across the consortium — the numbered steps, file layout, and naming are just a
> starting point. Rename, restructure, combine, or replace anything to fit your project.

Only **step 01 (cohort identification)** is a fully worked example
([Python](templates/Python/01_cohort_identification_template.py) ·
[R](templates/R/01_cohort_identification_template.R)) — it shows the CLIF idiom end to end:
load `config/config.json`, read the tables you need, build a cohort, and split outputs into
patient-level working data ([`output/intermediate_phi/`](../output/intermediate_phi)) vs. shareable
aggregates ([`output/final_no_phi/`](../output/final_no_phi)).

**Steps 02–04 are skeletons** (purpose + expected inputs/outputs, no code) for you to fill in.

**Try it on demo data:** the config defaults to the bundled [`clif_demo/`](../clif_demo) dataset, so
once you create your config you can run `01` immediately — no real data needed:
```
cp config/config_template.json config/config.json   # default data_directory = clif_demo
uv run python code/templates/Python/01_cohort_identification_template.py
# or: Rscript code/templates/R/01_cohort_identification_template.R
```
Point `data_directory` at your CLIF tables when you're ready to run on real data.

### General workflow

1. **Cohort identification** (`01`, worked example)
   - Apply inclusion/exclusion criteria, select required fields, filter the tables.
   - Output: the cohort + a `cohort_summary` aggregate.

2. **Quality checks** (`02`, skeleton)
   - Project-specific QC on the cohort: required fields present, categories valid (mCIDE),
     plausible ranges.
   - Input: cohort from `01` → Output: cleaned cohort.

3. **Outlier handling** (`03`, skeleton)
   - Set physiologically implausible values to NaN/NA. **Python:** use clifpy's
     `apply_outlier_handling` (CLIF-wide thresholds, no CSVs to manage). **R:** apply your
     project's agreed plausible ranges.
   - Input: cleaned cohort → Output: outlier-handled data.

4. **Analysis** (`04`, skeleton)
   - The main analysis. Write **aggregate** results to
     [`output/final_no_phi/`](../output/README.md) — no row-level data, every reported statistic
     n ≥ 10 (see the data-security rules in [`output/README.md`](../output/README.md) and
     [`../guides/primer.md`](../guides/primer.md)).
