# Project Creator Guide
**Author:** Kaveri Chhikara


This guide is for the **project creator** — the person turning this template into a CLIF project that
will be distributed to and run by other consortium sites. When you are done, the people who clone your
finished repository will read the project **[`README.md`](../README.md)** (which you customize in
Step 4), not this file.

> [!IMPORTANT]
> **This repository ships TWO code templates** — **R** ([`code/templates/R/`](../code/templates/R)) and
> **Python** ([`code/templates/Python/`](../code/templates/Python)). A project can be built in **R,
> Python, or both**. Set up the environment(s) for whichever language(s) your project uses.

## Step 1 — Configure `config/config.json`

Rename `config_template.json` to `config.json` and fill in your site-specific settings. Follow
[`config/README.md`](../config/README.md) for details. The `.gitignore` in that directory keeps your
config out of the remote repository.

## Step 2 — Set up the project environment

This template ships starter scripts for both languages in
[`code/templates/`](../code/templates). Build your project in **R**, **Python**, or **both** — set up
only the language(s) you'll use. The scripts are **suggested examples, not a fixed ruleset** — a
shared convention to start from; adapt, restructure, or replace them as your project needs.

### Python (using uv)

1. Copy the Python templates into your working `code/` directory:
   ```
   cp code/templates/Python/*.py code/
   ```
2. Install uv if you don't already have it (see the
   [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)):
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. From the project root, create the project file and add your dependencies:
   ```
   uv init               # creates pyproject.toml at the project root
   uv add clifpy pandas  # add the packages your project needs
   uv sync               # installs them into a managed environment
   ```
   Run project code inside that environment with `uv run python code/<script>.py`.

> [!IMPORTANT]
> **Commit `pyproject.toml`** so sites get the project's declared dependencies with a single
> `uv sync`. Also commit `uv.lock` if you want every site pinned to the exact same versions
> (recommended for reproducible results — uv generates it for you).

Use `uv init project-name` *only* if you want uv to scaffold a brand-new project in its own
subdirectory instead of using this template. For more details, see the
[CLIF uv guide by Zewei Whiskey Liao](https://github.com/Common-Longitudinal-ICU-data-Format/CLIF-data-huddles/blob/main/notes/uv-and-conv-commits.md).

### R (using renv)

1. Copy the R templates into your working `code/` directory:
   ```
   cp code/templates/R/*.R code/
   ```
2. Initialize renv, install the packages your project needs, then capture them
   (see [`code/templates/R/README.md`](../code/templates/R/README.md) for the full steps):
   ```
   # run initialize_renv_template.R, install your packages, then:
   renv::snapshot()      # writes renv.lock
   ```

> [!IMPORTANT]
> **Commit `renv.lock`** — it is what lets sites reproduce your R environment with
> `00_renv_restore.R`. Re-run `renv::snapshot()` before distributing so the lockfile is current.

### Then finalize the language setup

- **Delete the template folder for any language you are NOT using** (e.g. remove
  [`code/templates/R/`](../code/templates/R) for a Python-only project).
- **Trim the "Set up the project environment" section in [`README.md`](../README.md)** so it lists
  only the language(s) you kept.

## Step 3 — Data security (read before producing any output)

> [!WARNING]
> **Never upload patient-level data to Box.** Only **aggregate** results may be placed in
> [`output/final_no_phi/`](../output/README.md) and shared with the project PI / consortium:
> - No `patient_id` or any row-level / individual patient records.
> - Minimum cell size **n ≥ 10** for every reported statistic (prevents re-identification).
> - No raw `.csv` / `.parquet` data files.
>
> See [`output/README.md`](../output/README.md) for the file-naming convention and
> [`primer.md`](primer.md) for the full data-security rules.

## Step 4 — Customize the project README for the sites that will run your project

Edit the project **[`README.md`](../README.md)** to describe your project for the consortium sites who
will run it: the title, CLIF version, objective, required CLIF tables and fields, cohort
identification criteria, and expected results. It is the run-it-yourself guide your cloners will
follow (they reproduce your environment with `uv sync` / `00_renv_restore.R`). **Delete the
"Building a project from this template?" note at the top** once you have customized it.

## Step 5 — Buddy test before distributing

Before releasing the project to the whole consortium, have **one other site** run it end to end on
their own data as a validation gate. Recruit a buddy (ideally at a different institution / EHR), point
them at the **[Buddy Testing Guide](buddy-testing-guide.md)**, and have them return a filled
[`buddy-test-report-template.md`](buddy-test-report-template.md) as `BUDDY_TEST_REPORT.md`.

Fix any blocking issues they find. Once the report is a **Pass**, add a validation stamp near the top
of [`README.md`](../README.md) (just below the title) so cloning sites can see it was validated:

```markdown
> ✅ Buddy-tested by **[Site]** on **[YYYY-MM-DD]** — see [`BUDDY_TEST_REPORT.md`](BUDDY_TEST_REPORT.md).
```

## Where to go deeper

- **[`buddy-testing-guide.md`](buddy-testing-guide.md)** — pre-distribution validation: what a buddy
  site checks when running your project.
- **[`primer.md`](primer.md)** — practical guide to building CLIF projects (cohort workflow,
  optimization tips, data security, common errors).
- **[`code/README.md`](../code/README.md)** — the script workflow (cohort identification → quality
  checks → outlier handling → analysis).
- **[`config/README.md`](../config/README.md)** — configuration details.

See the [project README](../README.md#example-repositories) for example CLIF project repositories.
