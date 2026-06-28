def normalize_invoice(invoice: dict) -> dict:
    """
    Normalize a Zoho invoice record.
    """

    return {
        "invoice_id": invoice.get("invoice_id"),
        "organization_name": invoice.get("organization_name"),
        "segment": invoice.get("segment"),
        "revenue": invoice.get("amount", 0),
        "timestamp": invoice.get("date")
    }


def calculate_revenue_by_segment(invoices: list) -> dict:
    """
    Calculate total revenue grouped by segment.
    """

    revenue = {
        "Corporate": 0,
        "University": 0,
        "School": 0
    }

    for invoice in invoices:
        segment = invoice.get("segment")
        amount = invoice.get("amount", 0)

        if segment in revenue:
            revenue[segment] += amount

    return revenue