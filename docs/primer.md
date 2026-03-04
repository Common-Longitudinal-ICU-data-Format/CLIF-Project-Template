# CLIF Project Primer

**Author:** Kaveri Chhikara

A practical guide to building CLIF projects — from cohort identification to optimized analysis.

---

## Code Workflow

### Step 1: Load Core Tables to Identify the Cohort

Output: A list of `hospitalization_id`s

1. **Start with `hospitalization`** — filter by age, dates, or other static criteria
2. **Join with `adt`** — sanity check that hospitalizations have location data
3. **Join with `patient`** — get demographics and other static info
4. **Extract the list of `hospitalization_id`s** — this is your starting cohort
5. **Optional: Stitch encounters** — use `stitching_encounters` logic or the `hospitalization_joined_id` column to identify linked hospitalizations (available in clifpy)

### Step 2: Refine the Cohort

Output: A filtered list of `hospitalization_id`s meeting your inclusion/exclusion criteria

**Example cohort definitions:**

| Criteria | Approach |
|:---------|:---------|
| ICU stay ≥24 hours | Load `adt` for Step 1 cohort → calculate ICU duration → filter |
| On IMV at least once | Load `respiratory_support` → filter `device_category == "IMV"` → get unique IDs |
| Exclude trach patients | Load `respiratory_support` → identify `tracheostomy == True` → exclude from cohort |

### Step 3: Load Required Tables for Final Cohort

Once the cohort is finalized:

- Use clifpy's `load_data()` function to filter CLIF tables to your cohort
- Specify only the required fields and mCIDE categories
- This keeps memory usage manageable

### Step 4: Build Patient Trajectories

For time-series data like respiratory support or CRRT:

- Use `waterfall()` for respiratory support or CRRT tables
- Apply appropriate filling logic to create complete event-based patient trajectories

### Step 5: Optimization Tips

| Tip | Why |
|:----|:----|
| Use vectorized operations | Loops are slow; Polars/pandas vectorized ops are fast |
| Use efficient dtypes | `Int8` for flags/dummies instead of `Int64` saves memory |
| Load `*_category` as lowercase | Consistent casing prevents matching bugs |
| Never use `*_name` fields | Always use `*_category` — these are harmonized and standardized in the CLIF schema |
| Use try/except blocks | Handle errors gracefully across sites with different data quirks |

---

## Data Security

### Never Commit Patient Data

```bash
# Your .gitignore should ALWAYS include:
data/
*.csv
*.parquet
```

### Only Share Aggregates

```python
# ❌ Bad - sharing patient-level data
results = df.select("patient_id", "outcome")

# ✅ Good - sharing only aggregates
results = df.group_by("site").agg([
    pl.count().alias("n"),
    pl.col("outcome").mean().alias("mortality_rate")
])
```

### Minimum Cell Sizes

For any summary statistics, ensure minimum cell sizes (typically n ≥ 10) to prevent re-identification.

---

## Common Errors

| Error | Cause | Fix |
|:------|:------|:----|
| "Column not found" | Wrong column name | Check the [CLIF data dictionary](https://clif-icu.com/data-dictionary) |
| DateTime parsing errors | Column not parsed as datetime | Use `pl.col("dttm").str.to_datetime()` |
| Memory errors | Loading too much data | Use lazy evaluation: `pl.scan_parquet()` then `.collect()` |
| Validation failures | Categories don't match mCIDE | Check `df["category"].unique()` against mCIDE |

---

## Getting Help

- **#clif-code-ecosystem** — Slack channel for coding questions
- **#clifpy** — Slack channel for clifpy-specific issues
- **GitHub Issues** — For bugs in clifpy, project repos
- **Weekly CLIF Calls** — Thursdays 2-3 PM CT

---

*Have improvements? PR to [CLIF-Project-Template](https://github.com/Common-Longitudinal-ICU-data-Format/CLIF-Project-Template) or let us know in #clif-code-ecosystem!*
