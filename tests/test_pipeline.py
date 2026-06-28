from modules.pipeline_scoring import score_deal


def test_score_deal():

    deal = {
        "segment": "Corporate",
        "value": 150000,
        "age_days": 5,
        "engagement_score": 90,
        "payment_status": "Paid"
    }

    result = score_deal(deal)

    assert result == 100