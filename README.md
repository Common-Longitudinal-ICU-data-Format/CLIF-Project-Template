# *CLIF Project Title*

> [!NOTE]
> **Building a project from this template?** Read the
> [Project Creator Guide](guides/creator-guide.md) first, then **delete this note** and customize the
> sections below to describe your project for the consortium sites that will run it.

## CLIF VERSION

[major].[minor]

## Objective

*Describe the project objective*

## Required CLIF tables and fields

Please refer to the [CLIF data dictionary](https://clif-icu.com/data-dictionary), [CLIF Tools](https://clif-icu.com/tools), [ETL Guide](https://clif-icu.com/etl-guide), and [specific table contacts](https://github.com/clif-consortium/CLIF?tab=readme-ov-file#relational-clif) for more information on constructing the required tables and fields.

*List all required tables for the project here, and provide a brief rationale for why they are required.*

Example:
The following tables are required:
1. **patient**: `patient_id`, `race_category`, `ethnicity_category`, `sex_category`
2. **hospitalization**: `patient_id`, `hospitalization_id`, `admission_dttm`, `discharge_dttm`, `age_at_admission`
3. **vitals**: `hospitalization_id`, `recorded_dttm`, `vital_category`, `vital_value`
   - `vital_category` = 'heart_rate', 'resp_rate', 'sbp', 'dbp', 'map', 'resp_rate', 'spo2'
4. **labs**: `hospitalization_id`, `lab_result_dttm`, `lab_category`, `lab_value`
   - `lab_category` = 'lactate'
5. **medication_admin_continuous**: `hospitalization_id`, `admin_dttm`, `med_name`, `med_category`, `med_dose`, `med_dose_unit`
   - `med_category` = "norepinephrine", "epinephrine", "phenylephrine", "vasopressin", "dopamine", "angiotensin", "nicardipine", "nitroprusside", "clevidipine", "cisatracurium"
6. **respiratory_support**: `hospitalization_id`, `recorded_dttm`, `device_category`, `mode_category`, `tracheostomy`, `fio2_set`, `lpm_set`, `resp_rate_set`, `peep_set`, `resp_rate_obs`

For Python users, the [clifpy](https://common-longitudinal-icu-data-format.github.io/clifpy/) package provides essential utilities for working with CLIF data, including:
- Key features: outlier handling, encounter stitching, wide data creation, and more
- Advanced features: SOFA score computation, respiratory support waterfall, medication unit conversion, and more

See the [clifpy user guide](https://common-longitudinal-icu-data-format.github.io/clifpy/user-guide/) for detailed documentation.

## Cohort identification
*Describe study cohort inclusion and exclusion criteria here*

## Expected Results

*Describe the output of the analysis. The final project results should be saved in the [`output/final_no_phi`](output/README.md) directory.*

> [!WARNING]
> **Never upload patient-level data to Box.** Only **aggregate** results may be placed in
> [`output/final_no_phi/`](output/README.md) and shared with the project PI / consortium:
> - No `patient_id` or any row-level / individual patient records.
> - Minimum cell size **n ≥ 10** for every reported statistic (prevents re-identification).
> - No raw `.csv` / `.parquet` data files.
>
> See [`output/README.md`](output/README.md) for the file-naming convention and
> [`guides/primer.md`](guides/primer.md) for the full data-security rules.

## Detailed Instructions for running the project

### 1. Configure `config/config.json`
Follow the instructions in [`config/README.md`](config/README.md) to set your site name, the path to
your CLIF tables, and the file type. You can add any other project specific common config requirements.


### 2. Set up the project environment

Set up the environment for the language(s) this project uses.

**Python (using uv):** install [uv](https://docs.astral.sh/uv/getting-started/installation/), then from
the project root install the project's dependencies:
```
uv sync
```
Run project code inside the managed environment with `uv run python code/<script>.py` (or
`uv run jupyter lab`).

**R (using renv):** run `00_renv_restore.R` in [`code/`](code) to install the project's R packages.

### 3. Run code

Detailed instructions on the code workflow are provided in the [code directory](code/README.md).
Final results are written to [`output/final_no_phi`](output/README.md) — remember the data-security rules
above before sharing anything.

## Example Repositories
* [CLIF Variation in Ventilation](https://github.com/ingra107/clif_vent_variation) for R
* [CLIF Eligibility for mobilization](https://github.com/kaveriC/CLIF-eligibility-for-mobilization) for Python
