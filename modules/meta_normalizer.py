def calculate_engagement_rate(engagements: int, reach: int) -> float:
    """
    Calculate engagement rate percentage.
    """
    if reach == 0:
        return 0.0

    return round((engagements / reach) * 100, 2)


def normalize_meta(meta_data: dict) -> dict:
    """
    Normalize Meta API metrics into a standard structure.
    """

    reach = meta_data.get("reach", 0)
    impressions = meta_data.get("impressions", 0)
    engagements = meta_data.get("engagements", 0)
    followers_current = meta_data.get("followers_current", 0)
    followers_previous = meta_data.get("followers_previous", 0)

    follower_delta = followers_current - followers_previous

    return {
        "reach": reach,
        "impressions": impressions,
        "engagements": engagements,
        "engagement_rate": calculate_engagement_rate(
            engagements,
            reach
        ),
        "followers_current": followers_current,
        "followers_previous": followers_previous,
        "follower_delta": follower_delta
    }