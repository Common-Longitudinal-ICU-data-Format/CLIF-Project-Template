# Load required libraries
import sys
import os
import pandas as pd
import time
import pyarrow.parquet as pq
from utils import config 
from clifpy.tables import Vitals, Labs, MedicationAdminContinuous
from clifpy import ClifOrchestrator
from clifpy.utils.outlier_handler import apply_outlier_handling, get_outlier_summary

# Setup and Load Data

# ==============================================================================
# OPTION A: Using `clifpy` (Recommended)
# ==============================================================================

# Provide the path to your CLIF config file
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "config", "config_template.json")
co = ClifOrchestrator(config_path=os.path.abspath(config_path))
print("Loading required tables...")
co.initialize(tables=['vitals', 'labs', 'medication_admin_continuous'])
co.get_loaded_tables()

# Access the table objects
vitals = co.vitals
labs = co.labs
meds = co.medication_admin_continuous

# ==============================================================================
# END OPTION A
# ==============================================================================


# ==============================================================================
# OPTION B: Manual setup and data loading
# ==============================================================================
# Add the parent directory of the current script to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Use the imported config
# Access configuration parameters
site_name = config['site_name']
tables_path = config['tables_path']
file_type = config['file_type']

# Print the configuration parameters
print(f"Site Name: {site_name}")
print(f"Tables Path: {tables_path}")
print(f"File Type: {file_type}")

## Confirm that these are the correct paths
adt_filepath = f"{tables_path}/clif_adt.{file_type}"
hospitalization_filepath = f"{tables_path}/clif_hospitalization.{file_type}"
vitals_filepath = f"{tables_path}/clif_vitals.{file_type}"
labs_filepath = f"{tables_path}/clif_labs.{file_type}"
meds_filepath = f"{tables_path}/clif_medication_admin_continuous.{file_type}"
resp_support_filepath = f"{tables_path}/clif_respiratory_support.{file_type}"


def read_data(filepath, filetype):
    """
    Read data from file based on file type.
    Parameters:
        filepath (str): Path to the file.
        filetype (str): Type of the file ('csv' or 'parquet').
    Returns:
        DataFrame: DataFrame containing the data.
    """
    start_time = time.time()  # Record the start time
    file_name = os.path.basename(filepath) 
    if filetype == 'csv':
        df = pd.read_csv(filepath)
    elif filetype == 'parquet':
        table = pq.read_table(filepath)
        df = table.to_pandas()
    else:
        raise ValueError("Unsupported file type. Please provide either 'csv' or 'parquet'.")
    
    end_time = time.time()  # Record the end time
    load_time = end_time - start_time  # Calculate the loading time
    
    # Calculate the size of the loaded dataset in MB
    dataset_size_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f"File name: {file_name}")
    print(f"Time taken to load the dataset: {load_time:.2f} seconds")
    print(f"Size of the loaded dataset: {dataset_size_mb:.2f} MB\n")
    
    return df


vitals = read_data(vitals_filepath, file_type)
labs = read_data(labs_filepath, file_type)
meds = read_data(meds_filepath, file_type)


# ==============================================================================
# END OPTION B
# ==============================================================================

# ==============================================================================
# Step 1: Preview outliers before applying changes
# ==============================================================================
# Use get_outlier_summary() to see the impact before modifying data

print("Vitals Outlier Summary")
vitals_summary = get_outlier_summary(vitals)
print(f"Total rows: {vitals_summary['total_rows']}")
print(f"Config source: {vitals_summary['config_source']}")

print("Labs Outlier Summary")
labs_summary = get_outlier_summary(labs)
print(f"Total rows: {labs_summary['total_rows']}")

print("Medications Outlier Summary")
meds_summary = get_outlier_summary(meds)
print(f"Total rows: {meds_summary['total_rows']}")



# ==============================================================================
# Step 2: Apply outlier handling
# ==============================================================================
# After reviewing the summary, apply outlier handling to convert out-of-range
# values to NaN. This modifies the table data in-place.

# Using CLIF standard ranges (default)
apply_outlier_handling(vitals)
apply_outlier_handling(labs)
apply_outlier_handling(meds)

print("Outlier handling applied to all tables.")


# ==============================================================================
# Optional: Using custom configuration
# ==============================================================================
# You can provide a custom YAML configuration file.
#
# Custom YAML structure:
# ```yaml
# tables:
#   vitals:
#     vital_value:
#       heart_rate:
#         min: 0
#         max: 300
#       temperature:
#         min: 32
#         max: 44
# ```
#
# Example usage:
# custom_config_path = "/path/to/custom_outlier_config.yaml"
# apply_outlier_handling(vitals, outlier_config_path=custom_config_path)


# ==============================================================================
# Step 3: Access the cleaned data
# ==============================================================================
# The cleaned DataFrames are available via the .df attribute

vitals_df = vitals.df
labs_df = labs.df
meds_df = meds.df

print(f"Cleaned vitals shape: {vitals_df.shape}")
print(f"Cleaned labs shape: {labs_df.shape}")
print(f"Cleaned meds shape: {meds_df.shape}")


