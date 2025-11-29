# GEOG-392-Student-Housing-Finder-

A simple Streamlit web application for browsing student housing listings near campus.

## Features

- **Housing Listings**: View and filter housing data by rent and number of bedrooms
- **Interactive Map**: See housing locations on an interactive map
- **Commute Data**: Browse commute information and filter by transportation mode
- **Custom Data**: Upload your own CSV files or use the included sample data

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kelby4657/GEOG-392-Student-Housing-Finder-.git
   cd GEOG-392-Student-Housing-Finder-
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Start the Streamlit application:
```bash
streamlit run app.py
```

The app will open in your default web browser. You can:
- Use the sample data provided in the `data/` folder
- Upload your own CSV files through the sidebar

## Project Structure

```
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/
│   ├── housing_sample.csv      # Sample housing data
│   └── commute_sample.csv      # Sample commute data
└── src/
    ├── __init__.py
    └── data_loader.py          # Data loading and validation functions
```

## Data Format

### Housing CSV

Required columns:
- `id`: Unique listing identifier
- `address`: Property address
- `rent`: Monthly rent ($)
- `beds`: Number of bedrooms
- `baths`: Number of bathrooms
- `sqft`: Square footage
- `lat`: Latitude coordinate
- `lon`: Longitude coordinate
- `distance_to_campus_miles`: Distance to campus
- `link`: URL to listing

### Commute CSV

Required columns:
- `id`: Unique record identifier
- `origin_lat`: Origin latitude
- `origin_lon`: Origin longitude
- `destination`: Destination name
- `commute_mode`: Mode of transportation (e.g., walking, biking, driving)
- `duration_minutes`: Commute duration in minutes
- `distance_miles`: Commute distance in miles

## Using the Data Loader Module

You can also use the data loader module directly in Python:

```python
from src.data_loader import load_housing, load_commute

# Load housing data
housing_df = load_housing("data/housing_sample.csv")
print(housing_df)

# Load commute data
commute_df = load_commute("data/commute_sample.csv")
print(commute_df)
```

Or run it as a script:
```bash
python -m src.data_loader
```

## License

This project is for educational purposes.
