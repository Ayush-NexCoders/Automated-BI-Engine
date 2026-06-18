def score_deal(deal: dict) -> int:
    score = 0

    # Segment Score
    segment_scores = {
        "Corporate": 20,
        "University": 15,
        "School": 10
    }

    score += segment_scores.get(
        deal.get("segment"),
        0
    )

    # Value Score
    value = deal.get("value", 0)

    if value >= 100000:
        score += 25
    elif value >= 50000:
        score += 15
    else:
        score += 5

    # Age Score
    age_days = deal.get("age_days", 0)

    if age_days <= 7:
        score += 15
    elif age_days <= 30:
        score += 10
    else:
        score += 5

    # Engagement Score
    engagement = deal.get(
        "engagement_score",
        0
    )

    if engagement >= 80:
        score += 20
    elif engagement >= 50:
        score += 10
    else:
        score += 5

    # Payment Score
    payment_status = deal.get(
        "payment_status"
    )

    if payment_status == "Paid":
        score += 20
    elif payment_status == "Partial":
        score += 10

    return score

def rank_deals(deals: list) -> list:

    scored = []

    for deal in deals:

        deal["score"] = score_deal(deal)

        scored.append(deal)

    scored.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored