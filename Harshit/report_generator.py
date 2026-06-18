def generate_report(original_count,
                    cleaned_count):

    duplicates_removed = (
        original_count -
        cleaned_count
    )

    print("\n" + "=" * 40)

    print("DATA PROCESSING REPORT")

    print("=" * 40)

    print(
        f"Original Records: {original_count}"
    )

    print(
        f"Final Records: {cleaned_count}"
    )

    print(
        f"Duplicates Removed: {duplicates_removed}"
    )

    print("=" * 40)