# `intermediate_phi/` — patient-level working data (NEVER share)

This folder holds intermediate, **patient-level** working data (filtered cohorts, per-patient tables,
anything with `patient_id` or row-level records). Treat everything here as containing PHI.

- **Never** upload the contents of this folder to Box, share with the PI, or send across the
  consortium.
- Its contents are **git-ignored** so they cannot be committed — only this `README.md` is tracked.
- Share results **only** from [`../final_no_phi/`](../final_no_phi) (aggregate, n ≥ 10, no row-level
  records). See [`../README.md`](../README.md) and [`../../guides/primer.md`](../../guides/primer.md)
  for the full data-security rules.
