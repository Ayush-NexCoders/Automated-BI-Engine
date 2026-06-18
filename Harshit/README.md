# Automated BI Engine - Week 1

## Objective

Develop the foundational data processing pipeline for the Automated BI Engine.

## Features Implemented

* Multi-source CSV data loading
* Schema validation
* Data cleaning
* Duplicate record removal
* Missing value handling
* Automated report generation
* Export of cleaned datasets

## Project Structure

data/

* meta_data.csv
* linkedin_data.csv
* zoho_data.csv

output/

* cleaned_meta.csv
* cleaned_linkedin.csv
* cleaned_zoho.csv

Core Modules:

* config.py
* data_loader.py
* schema_validator.py
* data_cleaner.py
* report_generator.py
* main.py

## Technologies Used

* Python 3
* Pandas
* NumPy

## How to Run

```bash
python main.py
```

## Output

The pipeline validates, cleans, and exports processed datasets into the output directory.

## Week 1 Deliverables Completed

* Environment Setup
* Repository Setup
* Data Loading
* Schema Validation
* Data Cleaning
* Duplicate Removal
* Missing Value Handling
* Report Generation
* Export Pipeline
