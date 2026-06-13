from modules.meta_normalizer import normalize_meta

sample_meta = {
    "reach": 8000,
    "impressions": 12000,
    "engagements": 720,
    "followers_current": 1500,
    "followers_previous": 1450
}

result = normalize_meta(sample_meta)

print(result)