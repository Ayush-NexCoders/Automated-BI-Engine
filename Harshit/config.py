DATA_FILES = {
    "meta": "data/meta_data.csv",
    "linkedin": "data/linkedin_data.csv",
    "zoho": "data/zoho_data.csv"
}

REQUIRED_SCHEMAS = {
    "meta": [
        "platform",
        "impressions",
        "reach",
        "engagement"
    ],

    "linkedin": [
        "company",
        "followers",
        "post_engagement"
    ],

    "zoho": [
        "customer",
        "segment",
        "value"
    ]
}