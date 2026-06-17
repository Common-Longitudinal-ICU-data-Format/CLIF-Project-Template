# Buddy Testing Guide

**Buddy testing** is a pre-distribution validation gate: before a CLIF project is released to the
whole consortium, **one other site** ("the buddy") clones the finished repository, runs it end to end
on **their own data**, and confirms it works cleanly somewhere other than where it was built. The
buddy produces a short report ([`buddy-test-report-template.md`](buddy-test-report-template.md)) with
a pass/fail verdict and a list of any blocking issues for the creator to fix.

> **Who and when.** The project creator recruits a buddy after finishing the project
> ([Creator Guide → Step 5](creator-guide.md)) and before consortium-wide distribution. Ideally the
> buddy is at a **different institution / EHR** than the creator, so site-specific assumptions get
> caught.

## What you are — and aren't — checking

You run on your **own** data, so you **cannot** reproduce the creator's exact result values, and that
is not the goal. You are confirming the project **runs cleanly, produces sane and security-compliant
output, and is documented well enough for any site to follow** — plus a light clinical plausibility
pass on the aggregate results.

You are **not** doing a full methodology or code-correctness audit. If the cohort logic or analysis
looks wrong, flag it as a note — but proving statistical correctness is the creator's and PI's job,
not the buddy's.

## What to check

Work top to bottom; record a result and notes for each in the report.

### 1. Environment reproduces
Clone the repository **fresh** (don't reuse the creator's working copy) and rebuild the environment
exactly as the [project README](../README.md) instructs:
- **Python:** `uv sync` succeeds from the committed `pyproject.toml` (and `uv.lock` if present) — no
  manual `pip install` needed.
- **R:** `00_renv_restore.R` restores from the committed `renv.lock` without hand-installing packages.
- Note the language version and anything you had to install or work around.

### 2. Configuration works as documented
- You can create `config/config.json` from the template by following
  [`config/README.md`](../config/README.md) alone — site name, data path, and file type.
- The code reads **everything site-specific from the config** — no hardcoded paths, site names, or
  date ranges buried in the scripts.

### 3. Required tables and fields match reality
- The CLIF tables and fields the README lists as required are **actually** the ones the code reads —
  nothing undocumented, nothing listed-but-unused.
- Category values match mCIDE (e.g. `vital_category`, `med_category`).
- If a required table or field is missing in your data, the code fails with a **clear message**, not a
  cryptic stack trace.

### 4. End-to-end execution
- Scripts run in order (cohort identification → quality checks → outlier handling → analysis; see
  [`code/README.md`](../code/README.md)) **without manual edits** between steps.
- Note total runtime and any memory pressure.

### 5. Outputs land correctly
- Final results are written to [`output/final_no_phi/`](../output/README.md).
- File naming follows the project's convention (e.g. `RESULT_SITE_TIME`).
- Output files are the expected type (aggregate tables / figures), not raw data dumps.

### 6. Data-security compliance *(blocking — never wave this through)*
Inspect **every** file the project would have you share:
- **No** `patient_id` or any row-level / individual patient records.
- **Every** reported statistic has cell size **n ≥ 10**.
- **No** raw `.csv` / `.parquet` patient data among the shareable outputs.
- Nothing in `output/final_no_phi/` would be unsafe to upload to Box / send to the PI.

Any failure here is an automatic **Fail** regardless of how well everything else ran. See
[`primer.md`](primer.md) for the full data-security rules.

### 7. Light clinical sanity
Eyeball the aggregate results against what you'd expect for an ICU cohort — cohort size, mortality,
age distribution, vital/lab ranges. You're not validating the science, just flagging the obviously
implausible (e.g. a 0% or 100% mortality rate, negative ages, a cohort of 3 patients). Note anything
that looks off.

### 8. Documentation usability
The honest test: **could you run this project from the README alone**, without asking the creator
anything? Note every spot where you got stuck, guessed, or had to reach out — those are the gaps real
sites will hit.

## Reporting and sign-off

1. Copy [`buddy-test-report-template.md`](buddy-test-report-template.md) to the project root as
   `BUDDY_TEST_REPORT.md`.
2. Mark each check **Pass** or **Fail** and add a note.
3. Record an **overall verdict** (this is where "Pass with notes" lives):
   - **Pass** — runs cleanly, output is sane and secure, docs are followable. Ready to distribute.
   - **Pass with notes** — works, but has non-blocking rough edges the creator should address.
   - **Fail** — at least one **blocking** issue: it doesn't run, output is wrong/insecure, or the docs
     are unfollowable. List every blocker explicitly.
4. Commit `BUDDY_TEST_REPORT.md` and share it with the creator. On a Pass, the creator adds a
   validation stamp to the README (see [Creator Guide → Step 5](creator-guide.md)).

**A data-security failure (check 6) is always blocking.** Everything else is a judgment call between
"pass with notes" and "fail" — when unsure, write it down and let the creator decide.
