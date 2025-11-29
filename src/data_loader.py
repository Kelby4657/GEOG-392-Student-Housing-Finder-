"""
Data Loader Module for Student Housing Finder

This module provides functions to load and validate housing and commute data
from CSV files into pandas DataFrames.
"""

import pandas as pd
import os


# Required columns for each data type
HOUSING_COLUMNS = [
    "id", "address", "rent", "beds", "baths", "sqft",
    "lat", "lon", "distance_to_campus_miles", "link"
]

COMMUTE_COLUMNS = [
    "id", "origin_lat", "origin_lon", "destination",
    "commute_mode", "duration_minutes", "distance_miles"
]

# Numeric columns that need type coercion
HOUSING_NUMERIC_COLUMNS = [
    "id", "rent", "beds", "baths", "sqft", "lat", "lon", "distance_to_campus_miles"
]

COMMUTE_NUMERIC_COLUMNS = [
    "id", "origin_lat", "origin_lon", "duration_minutes", "distance_miles"
]


def load_housing(path: str) -> pd.DataFrame:
    """
    Load housing data from a CSV file.

    Parameters
    ----------
    path : str
        Path to the housing CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing housing listings with validated columns.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If required columns are missing from the CSV.
    """
    # Check if file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Housing data file not found: {path}")

    # Load the CSV
    df = pd.read_csv(path)

    # Validate required columns
    missing_cols = set(HOUSING_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Missing required columns in housing data: {missing_cols}"
        )

    # Coerce numeric fields to appropriate types
    for col in HOUSING_NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def load_commute(path: str) -> pd.DataFrame:
    """
    Load commute data from a CSV file.

    Parameters
    ----------
    path : str
        Path to the commute CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing commute data with validated columns.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If required columns are missing from the CSV.
    """
    # Check if file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Commute data file not found: {path}")

    # Load the CSV
    df = pd.read_csv(path)

    # Validate required columns
    missing_cols = set(COMMUTE_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Missing required columns in commute data: {missing_cols}"
        )

    # Coerce numeric fields to appropriate types
    for col in COMMUTE_NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


if __name__ == "__main__":
    # Demonstration of loading the sample CSVs
    import sys

    # Determine the base path (relative to this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")

    housing_path = os.path.join(data_dir, "housing_sample.csv")
    commute_path = os.path.join(data_dir, "commute_sample.csv")

    print("Loading sample housing data...")
    try:
        housing_df = load_housing(housing_path)
        print(housing_df)
        print()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading housing data: {e}")
        sys.exit(1)

    print("Loading sample commute data...")
    try:
        commute_df = load_commute(commute_path)
        print(commute_df)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading commute data: {e}")
        sys.exit(1)

    print("\nData loaded successfully!")
