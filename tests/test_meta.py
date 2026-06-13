from modules.meta_normalizer import normalize_meta

def test_normalize_meta():
    data = {
        "reach": 1000,
        "impressions": 1500,
        "engagements": 100,
        "followers_current": 500,
        "followers_previous": 450
    }

    result = normalize_meta(data)

    assert result["engagement_rate"] == 10.0
    assert result["follower_delta"] == 50