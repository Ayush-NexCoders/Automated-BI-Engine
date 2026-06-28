REQUIRED_FIELDS = [
    "invoice_id",
    "organization_name",
    "segment",
    "amount",
    "date"
]


def validate_invoice(invoice: dict) -> tuple:
    """
    Validate invoice schema.

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """

    for field in REQUIRED_FIELDS:

        if field not in invoice:
            return (
                False,
                f"Missing field: {field}"
            )

        if invoice[field] is None:
            return (
                False,
                f"Null value found in: {field}"
            )

    return (
        True,
        None
    )