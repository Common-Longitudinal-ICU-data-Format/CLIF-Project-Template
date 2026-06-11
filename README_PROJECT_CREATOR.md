# Project Creator Guide

This guide is for the **project creator** — the person turning this template into a CLIF project that
will be distributed to and run by other consortium sites. When you are done, the people who clone your
finished repository will read **[`README_PROJECT.md`](README_PROJECT.md)** (which you customize in
Step 4), not this file.

> [!IMPORTANT]
> **This repository ships TWO code templates** — **R** ([`code/templates/R/`](code/templates/R)) and
> **Python** ([`code/templates/Python/`](code/templates/Python)). A project can be built in **R,
> Python, or both**. Set up the environment(s) for whichever language(s) your project uses.

## Step 1 — Configure `config/config.json`

Rename `config_template.json` to `config.json` and fill in your site-specific settings. Follow
[`config/README.md`](config/README.md) for details. The `.gitignore` in that directory keeps your
config out of the remote repository.

**Note:** if your project uses the `01_run_cohort_id_app.R` file, this step is not necessary — the app
creates the config file for the user.

## Step 2 — Set up the project environment

### Python (using uv) — preferred

First, install uv if you don't already have it (see the
[uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)):
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Then, from inside this cloned template directory, initialize uv and add your dependencies:
```
uv init               # initialize uv in the existing project directory
uv add clifpy pandas  # add the packages your project needs
```
uv automatically creates and manages a virtual environment. Run project code inside it with:
```
uv run python code/<script>.py
# or launch a notebook
uv run jupyter lab
```

> [!IMPORTANT]
> **Commit both `pyproject.toml` and `uv.lock`** to your repository. This is what lets the sites who
> clone your finished project reproduce the exact same environment with a single `uv sync`.

Use `uv init project-name` *only* if you want uv to scaffold a brand-new project in its own
subdirectory instead of using this template. For more details, see the
[CLIF uv guide by Zewei Whiskey Liao](https://github.com/Common-Longitudinal-ICU-data-Format/CLIF-data-huddles/blob/main/notes/uv-and-conv-commits.md).

### R (using renv)

Run `00_renv_restore.R` in [`code/templates/R`](code/templates/R) to set up the project environment.
Before distributing the project across the consortium, run `renv::snapshot()` so the most up-to-date
packages are captured in the lockfile. See [`code/templates/R/README.md`](code/templates/R/README.md)
for the full renv initialization steps.

### Alternative method using python3

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 3 — Data security (read before producing any output)

> [!WARNING]
> **Never upload patient-level data to Box.** Only **aggregate** results may be placed in
> [`output/final/`](output/README.md) and shared with the project PI / consortium:
> - No `patient_id` or any row-level / individual patient records.
> - Minimum cell size **n ≥ 10** for every reported statistic (prevents re-identification).
> - No raw `.csv` / `.parquet` data files — share results only (e.g. PDFs named `RESULT_SITE_TIME.pdf`).
>
> See [`output/README.md`](output/README.md) for the file-naming convention and
> [`docs/primer.md`](docs/primer.md) for the full data-security rules.

## Step 4 — Customize the project README for the sites that will run your project

Edit **[`README_PROJECT.md`](README_PROJECT.md)** to describe your project for the consortium sites who
will run it: the title, CLIF version, objective, required CLIF tables and fields, cohort
identification criteria, and expected results. That file is the run-it-yourself guide your cloners
will follow (they reproduce your environment with `uv sync` / `00_renv_restore.R`).

## Where to go deeper

- **[`docs/primer.md`](docs/primer.md)** — practical guide to building CLIF projects (cohort workflow,
  optimization tips, data security, common errors).
- **[`code/README.md`](code/README.md)** — the script workflow (cohort identification → quality
  checks → outlier handling → analysis).
- **[`config/README.md`](config/README.md)** — configuration details.

## Example Repositories
* [CLIF Adult Sepsis Events](https://github.com/08wparker/CLIF_sepsis) for R
* [CLIF Eligibility for mobilization](https://github.com/kaveriC/CLIF-eligibility-for-mobilization) for Python
* [CLIF Variation in Ventilation](https://github.com/ingra107/clif_vent_variation)
