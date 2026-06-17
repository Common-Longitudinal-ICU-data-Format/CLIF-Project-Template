"""
03 — Outlier handling (skeleton — fill this in)

Purpose: set physiologically implausible values to NaN before analysis.
Input:   output/intermediate_phi/   (cleaned cohort from 02)
Output:  output/intermediate_phi/   (outlier-handled data)

Use clifpy's built-in outlier handling — it applies CLIF-wide thresholds, so there are no
threshold CSVs to manage:

    from clifpy.utils import apply_outlier_handling, get_outlier_summary

    get_outlier_summary(co.vitals)   # preview the impact before modifying anything
    apply_outlier_handling(co.vitals)  # sets out-of-range values to NaN, in place

TODO: apply outlier handling to the tables your project uses.
"""
