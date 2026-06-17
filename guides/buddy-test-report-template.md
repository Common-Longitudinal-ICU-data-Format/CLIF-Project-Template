<!--
Buddy test report template. See guides/buddy-testing-guide.md for what each check means.
To use: copy this file to the project root as BUDDY_TEST_REPORT.md, fill it in, and commit it.
In the Result column, bold the outcome that applies (or delete the other), then add a note.
Pass with notes is only for the Overall verdict at the bottom.
-->

# Buddy Test Report

| | |
|---|---|
| **Buddy site / institution** | *site name* |
| **Tester** | *name* |
| **Date** | *YYYY-MM-DD* |

> **How to fill this in:**  See [`buddy-testing-guide.md`](buddy-testing-guide.md) for what each
> check means.

## Checks

| # | Check | Result | Notes |
|:-:|-------|--------|-------|
| 1 | Environment reproduces (`uv sync` / `00_renv_restore.R`, nothing by hand) | Pass / Fail | |
| 2 | Configuration works from `config/README.md` alone; no hardcoding | Pass / Fail | |
| 3 | Required tables/fields match what the code reads (mCIDE-valid) | Pass / Fail | |
| 4 | Runs end to end with no manual edits between steps | Pass / Fail | |
| 5 | Outputs in `output/final_no_phi/` with right naming/type, no raw dumps | Pass / Fail | |
| 6 | **Data security**: no PHI, every stat n ≥ 10, no raw data *(blocking)* | Pass / Fail | |
| 7 | Clinical sanity: aggregates plausible for the cohort | Pass / Fail | |
| 8 | Documentation usable: could run from the README alone | Pass / Fail | |

## Overall verdict

**Verdict:** Pass / Pass with notes / Fail  *(keep one)*

- **Pass** — runs cleanly, output sane and secure, docs followable. Ready to distribute.
- **Pass with notes** — works; address the notes below.
- **Fail** — at least one blocking issue (doesn't run, output wrong/insecure, docs unfollowable). A
  data-security failure (check 6) is always a Fail.

### Blocking issues (must fix before distribution)
1. *…*

### Non-blocking notes / suggestions
1. *…*

