from modules.schema_validator import validate_invoice


def test_valid_invoice():

    invoice = {
        "invoice_id": "INV001",
        "organization_name": "ABC University",
        "segment": "University",
        "amount": 10000,
        "date": "2026-06-20"
    }

    valid, error = validate_invoice(invoice)

    assert valid is True
    assert error is None


def test_missing_field():

    invoice = {
        "invoice_id": "INV001",
        "amount": 10000
    }

    valid, error = validate_invoice(invoice)

    assert valid is False
    assert "Missing field" in error