from modules.zoho_normalizer import calculate_revenue_by_segment


def test_revenue_by_segment():

    invoices = [
        {
            "segment": "Corporate",
            "amount": 1000
        },
        {
            "segment": "Corporate",
            "amount": 2000
        },
        {
            "segment": "School",
            "amount": 500
        }
    ]

    result = calculate_revenue_by_segment(invoices)

    assert result["Corporate"] == 3000
    assert result["School"] == 500