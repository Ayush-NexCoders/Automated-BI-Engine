import pandas as pd

def clean_data(df):

    print("\n[INFO] Starting Data Cleaning")

    original_rows = len(df)

    # Remove duplicates
    df = df.drop_duplicates()

    removed = original_rows - len(df)

    print(f"[INFO] Removed {removed} duplicate records")

    # Fill missing text values
    for column in df.columns:

        if df[column].dtype == "object":

            df[column] = df[column].fillna("Unclassified")

    # Fill missing numeric values
    for column in df.columns:

        if str(df[column].dtype).startswith(("int", "float")):

            df[column] = df[column].fillna(0)

    print("[SUCCESS] Missing values handled")

    return df