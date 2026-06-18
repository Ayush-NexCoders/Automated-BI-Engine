from config import (
    DATA_FILES,
    REQUIRED_SCHEMAS
)

from data_loader import (
    load_dataset
)

from schema_validator import (
    validate_schema
)

from data_cleaner import (
    clean_data
)

from report_generator import (
    generate_report
)

print("\nAUTOMATED BI ENGINE")
print("\nStarting Pipeline...")

for source_name, file_path in DATA_FILES.items():

    print(
        f"\nProcessing: {source_name.upper()}"
    )

    df = load_dataset(file_path)

    if df is None:
        continue

    schema_ok = validate_schema(
        df,
        REQUIRED_SCHEMAS[source_name]
    )

    if not schema_ok:
        continue

    original_count = len(df)

    # Clean Data
    cleaned_df = clean_data(df)

    # Export Cleaned Dataset
    cleaned_df.to_csv(
        f"output/cleaned_{source_name}.csv",
        index=False
    )

    print(
        f"[SUCCESS] Exported cleaned_{source_name}.csv"
    )

    cleaned_count = len(cleaned_df)

    # Generate Report
    generate_report(
        original_count,
        cleaned_count
    )

print("\nPipeline Execution Completed.")