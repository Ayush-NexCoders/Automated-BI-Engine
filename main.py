from modules.meta_normalizer import normalize_meta

from modules.zoho_normalizer import (
    normalize_invoice,
    calculate_revenue_by_segment
)

sample_meta = {
    "reach": 8000,
    "impressions": 12000,
    "engagements": 720,
    "followers_current": 1500,
    "followers_previous": 1450
}

result = normalize_meta(sample_meta)

print(result)


sample_invoices = [
    {
        "invoice_id": "INV001",
        "organization_name": "ABC University",
        "segment": "University",
        "amount": 50000,
        "date": "2026-06-18"
    },
    {
        "invoice_id": "INV002",
        "organization_name": "XYZ School",
        "segment": "School",
        "amount": 25000,
        "date": "2026-06-18"
    },
    {
        "invoice_id": "INV003",
        "organization_name": "Tech Corp",
        "segment": "Corporate",
        "amount": 75000,
        "date": "2026-06-18"
    }
]

print("Normalized Invoice:")
print(normalize_invoice(sample_invoices[0]))

print("\nRevenue By Segment:")
print(calculate_revenue_by_segment(sample_invoices))