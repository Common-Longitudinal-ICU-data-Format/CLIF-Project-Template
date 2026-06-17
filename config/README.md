## Configuration

1. Rename `config_template.json` to `config.json`.
2. Fill in your site-specific settings:
   - `site_name` — your site's identifier (used in output file names).
   - `data_directory` — path to the directory holding your CLIF table files
     (`clif_vitals.parquet`, `clif_labs.parquet`, …). **Defaults to the bundled `clif_demo/`
     dataset so the templates run out of the box; change it to your site's CLIF tables directory
     for a real run.**
   - `filetype` — `"csv"` or `"parquet"`.
   - `timezone` — your data's timezone, e.g. `"US/Eastern"` (required by clifpy).
   - `output_directory` — where clifpy writes logs and validation results (e.g. `"./output"`).

This file uses the **clifpy config schema**, so the Python templates can read it directly with
`ClifOrchestrator(config_path="config/config.json")`, and the R templates read the same fields via
`utils/config.R`. You can add or remove attributes based on project requirements.

Note: the `.gitignore` in this directory keeps `config.json` out of the remote repository.
