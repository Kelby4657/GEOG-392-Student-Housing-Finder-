"""
Student Housing Finder - Streamlit Application

A simple web application to browse student housing listings and commute data.
Students can filter listings by rent and number of bedrooms, view locations
on an interactive map, and explore commute options.
"""

import streamlit as st
import pandas as pd
import os

# Import data loader functions
from src.data_loader import (
    load_housing, load_commute,
    HOUSING_COLUMNS, COMMUTE_COLUMNS,
    HOUSING_NUMERIC_COLUMNS, COMMUTE_NUMERIC_COLUMNS
)


# Default paths to sample data files
DEFAULT_HOUSING_PATH = os.path.join("data", "housing_sample.csv")
DEFAULT_COMMUTE_PATH = os.path.join("data", "commute_sample.csv")


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Student Housing Finder",
        page_icon="🏠",
        layout="wide"
    )

    st.title("🏠 Student Housing Finder")
    st.markdown(
        "Browse student housing listings near campus. "
        "Filter by rent and bedrooms, view locations on a map, and explore commute data."
    )

    # Sidebar for file uploads and filters
    st.sidebar.header("📁 Data Source")

    # Option to upload custom housing CSV
    housing_file = st.sidebar.file_uploader(
        "Upload Housing CSV (optional)",
        type=["csv"],
        help="Upload a custom housing CSV file or use the default sample data."
    )

    # Option to upload custom commute CSV
    commute_file = st.sidebar.file_uploader(
        "Upload Commute CSV (optional)",
        type=["csv"],
        help="Upload a custom commute CSV file or use the default sample data."
    )

    # Load housing data
    housing_df = load_data(housing_file, DEFAULT_HOUSING_PATH, "housing")

    # Load commute data
    commute_df = load_data(commute_file, DEFAULT_COMMUTE_PATH, "commute")

    # Display housing section
    st.header("🏘️ Housing Listings")

    if housing_df is not None:
        # Sidebar filters for housing
        st.sidebar.header("🔍 Housing Filters")

        # Handle potential NaN values in rent and beds columns
        max_rent_value = housing_df["rent"].dropna().max() if not housing_df["rent"].dropna().empty else 2000
        max_beds_value = housing_df["beds"].dropna().max() if not housing_df["beds"].dropna().empty else 4

        max_rent = st.sidebar.slider(
            "Max Rent ($)",
            min_value=0,
            max_value=int(max_rent_value) + 500,
            value=int(max_rent_value),
            step=50
        )

        min_beds = st.sidebar.slider(
            "Min Bedrooms",
            min_value=0,
            max_value=int(max_beds_value),
            value=0,
            step=1
        )

        # Apply filters
        filtered_housing = housing_df[
            (housing_df["rent"] <= max_rent) &
            (housing_df["beds"] >= min_beds)
        ]

        # Display results
        st.subheader(f"Found {len(filtered_housing)} listing(s)")

        if not filtered_housing.empty:
            # Display the filtered listings table
            st.dataframe(
                filtered_housing[["address", "rent", "beds", "baths", "sqft", "distance_to_campus_miles", "link"]],
                use_container_width=True
            )

            # Display map of housing locations
            st.subheader("📍 Housing Locations Map")
            # st.map expects columns named 'lat' and 'lon' or 'latitude' and 'longitude'
            map_data = filtered_housing[["lat", "lon"]].rename(
                columns={"lat": "latitude", "lon": "longitude"}
            )
            st.map(map_data)
        else:
            st.info("No listings match your filters. Try adjusting the criteria.")
    else:
        st.warning("No housing data available. Please upload a valid CSV file.")

    # Display commute section
    st.header("🚗 Commute Data")

    if commute_df is not None:
        # Sidebar filter for commute mode
        st.sidebar.header("🚶 Commute Filters")

        commute_modes = ["All"] + list(commute_df["commute_mode"].unique())
        selected_mode = st.sidebar.selectbox(
            "Commute Mode",
            options=commute_modes
        )

        # Apply filter
        if selected_mode == "All":
            filtered_commute = commute_df
        else:
            filtered_commute = commute_df[commute_df["commute_mode"] == selected_mode]

        # Display results
        st.subheader(f"Found {len(filtered_commute)} commute record(s)")

        if not filtered_commute.empty:
            st.dataframe(
                filtered_commute[["destination", "commute_mode", "duration_minutes", "distance_miles"]],
                use_container_width=True
            )
        else:
            st.info("No commute records match your filter.")
    else:
        st.warning("No commute data available. Please upload a valid CSV file.")

    # Footer
    st.markdown("---")
    st.markdown(
        "Built with [Streamlit](https://streamlit.io) | "
        "Data provided for educational purposes"
    )


def load_data(uploaded_file, default_path: str, data_type: str) -> pd.DataFrame:
    """
    Load data from an uploaded file or default path.

    Parameters
    ----------
    uploaded_file : UploadedFile or None
        Streamlit uploaded file object.
    default_path : str
        Path to the default sample data file.
    data_type : str
        Type of data ("housing" or "commute").

    Returns
    -------
    pd.DataFrame or None
        Loaded DataFrame or None if loading fails.
    """
    try:
        if uploaded_file is not None:
            # Load from uploaded file
            df = pd.read_csv(uploaded_file)

            # Validate columns based on data type
            if data_type == "housing":
                missing = set(HOUSING_COLUMNS) - set(df.columns)
                if missing:
                    st.error(f"Missing columns in housing CSV: {missing}")
                    return None
                # Coerce numeric columns
                for col in HOUSING_NUMERIC_COLUMNS:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            else:
                missing = set(COMMUTE_COLUMNS) - set(df.columns)
                if missing:
                    st.error(f"Missing columns in commute CSV: {missing}")
                    return None
                # Coerce numeric columns
                for col in COMMUTE_NUMERIC_COLUMNS:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

            return df
        else:
            # Load from default path
            if data_type == "housing":
                return load_housing(default_path)
            else:
                return load_commute(default_path)

    except FileNotFoundError:
        st.warning(f"Default {data_type} data file not found at: {default_path}")
        return None
    except ValueError as e:
        st.error(f"Error loading {data_type} data: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error loading {data_type} data: {e}")
        return None


if __name__ == "__main__":
    main()
