def validate_schema(df, required_columns):

    missing_columns = []

    for column in required_columns:

        if column not in df.columns:

            missing_columns.append(column)

    if len(missing_columns) == 0:

        print("[SUCCESS] Schema Valid")

        return True

    print("[ERROR] Missing Columns:")

    for col in missing_columns:

        print(f" - {col}")

    return False