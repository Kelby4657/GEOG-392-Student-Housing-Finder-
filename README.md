# GEOG 392 Student Housing Finder

This repository stores datasets and scripts for the GEOG 392 Student Housing Finder project. The goal is to collect, clean, and analyze housing data for students.

Repository structure

- Raw Data/       : Original unmodified data files (CSV, GeoJSON, shapefiles, etc.)
- Processed Data/ : Cleaned, standardized datasets ready for analysis
- Web App Code/   : Frontend and backend code for the web application
- docs/           : Documentation, notes, data dictionaries

How to add data

1. Put original files into Raw Data/. Include a README in the same folder if the dataset needs explanation.
2. When cleaning or transforming data, commit outputs to Processed Data/ and include a brief note in docs/ or as a comment in the script used.
3. Do not commit large binary files (>10 MB). Use external hosting or Git LFS for large files; add a small placeholder and a link in docs/ or Raw Data/.

Naming conventions

- Use lowercase and hyphens: source-name_YYYYMMDD.ext (e.g., housing-survey_20251128.csv)
- For processed files: source-name_YYYYMMDD_processed.ext

Contributing

- Create a branch for any substantive change using the pattern `feature/<short-description>` or `fix/<short-description>`.
- Open a pull request and request at least one review from a teammate before merging to main.

Contact

If you have questions, contact the repo owner or open an issue.
