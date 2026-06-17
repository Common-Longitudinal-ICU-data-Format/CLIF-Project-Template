## Output directory

Results are split into two folders by **data-sharing safety** — the names encode whether the contents
may leave your site:

* **[`final_no_phi/`](final_no_phi)** — **aggregate, shareable** results only. Everything delivered to
  the project PI / consortium goes here: no `patient_id` or row-level records, every reported statistic
  at cell size **n ≥ 10**, no raw `.csv` / `.parquet` data. Keeping all shareable results in one folder
  makes exporting them convenient.

* **[`intermediate_phi/`](intermediate_phi)** — **patient-level working data (NEVER share).** Filtered
  cohorts and any per-patient tables live here. Its contents are **git-ignored** so they can't be
  committed, and they must never be uploaded to Box or sent to the PI. See
  [`intermediate_phi/README.md`](intermediate_phi/README.md).

See [`../guides/primer.md`](../guides/primer.md) for the full data-security rules.
