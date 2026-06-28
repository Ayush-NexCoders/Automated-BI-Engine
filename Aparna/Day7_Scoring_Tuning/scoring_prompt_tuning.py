import os
import json
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ============================================
# ZOHO BOOKS SAMPLE RECORDS
# These simulate real Zoho Books live data
# In real integration, zoho_normalizer.py
# will provide these automatically
# ============================================
zoho_sample_records = [
    {
        "deal_id": "ZB001",
        "institution": "IIT Delhi",
        "segment": "University",
        "invoice_value": 150000,
        "payment_status": "paid",
        "last_contact_days": 2,
        "engagement_score": 95,
        "follow_up_due": False
    },
    {
        "deal_id": "ZB002",
        "institution": "Infosys Ltd",
        "segment": "Corporate",
        "invoice_value": 200000,
        "payment_status": "partial",
        "last_contact_days": 4,
        "engagement_score": 88,
        "follow_up_due": True
    },
    {
        "deal_id": "ZB003",
        "institution": "DPS School",
        "segment": "School",
        "invoice_value": 55000,
        "payment_status": "pending",
        "last_contact_days": 8,
        "engagement_score": 65,
        "follow_up_due": True
    },
    {
        "deal_id": "ZB004",
        "institution": "Delhi University",
        "segment": "University",
        "invoice_value": 95000,
        "payment_status": "paid",
        "last_contact_days": 1,
        "engagement_score": 92,
        "follow_up_due": False
    },
    {
        "deal_id": "ZB005",
        "institution": "TCS Mumbai",
        "segment": "Corporate",
        "invoice_value": 175000,
        "payment_status": "partial",
        "last_contact_days": 3,
        "engagement_score": 85,
        "follow_up_due": True
    }
]


# ============================================
# TUNED SCORING PROMPT
# This is the prompt we are tuning today
# It tells Groq exactly how to pick Top 3
# ============================================
def build_scoring_prompt(records):
    return f"""
You are a B2B sales pipeline analyst. 

Your job is to pick the TOP 3 most important deals to focus on this week.

Use these scoring rules:
- Payment status: "paid" = 40 points, "partial" = 25 points, "pending" = 10 points
- Engagement score: use directly (out of 100)
- Last contact: less than 3 days = 20 points, 3-7 days = 10 points, more than 7 days = 0 points
- Follow up due: if True = add 15 points bonus

Calculate total score for each deal and pick TOP 3.

DEALS DATA:
{json.dumps(records, indent=2)}

Respond ONLY in this exact JSON format, nothing else:
{{
    "top_3_deals": [
        {{
            "rank": 1,
            "deal_id": "ZB00X",
            "institution": "name here",
            "total_score": 0,
            "reason": "one sentence why this deal is top priority"
        }},
        {{
            "rank": 2,
            "deal_id": "ZB00X",
            "institution": "name here",
            "total_score": 0,
            "reason": "one sentence why"
        }},
        {{
            "rank": 3,
            "deal_id": "ZB00X",
            "institution": "name here",
            "total_score": 0,
            "reason": "one sentence why"
        }}
    ],
    "prompt_version": "v1",
    "validation_notes": "one sentence about overall pipeline health"
}}
"""


# ============================================
# SEND TO GROQ AND GET RESULT
# ============================================
def get_top3_deals(records):
    prompt = build_scoring_prompt(records)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(GROQ_URL, headers=headers, json=body)

    if response.status_code != 200:
        print("ERROR:", response.status_code)
        return {}

    raw = response.json()["choices"][0]["message"]["content"]

    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        result = json.loads(raw[start:end])
    except:
        print("Raw response:", raw)
        return {}

    return result


# ============================================
# VALIDATE: check AI picks match Zoho records
# ============================================
def validate_against_zoho(top3, zoho_records):
    zoho_ids = [r["deal_id"] for r in zoho_records]
    print("\n VALIDATION - Checking AI picks exist in Zoho records:")
    all_valid = True
    for deal in top3:
        deal_id = deal["deal_id"]
        if deal_id in zoho_ids:
            print(f"  ✅ {deal_id} - {deal['institution']} → Found in Zoho records")
        else:
            print(f"  ❌ {deal_id} - {deal['institution']} → NOT found in Zoho records!")
            all_valid = False

    if all_valid:
        print("\n All Top-3 deals validated against Zoho records!")
    else:
        print("\n Some deals not found — prompt needs more tuning")

    return all_valid


# ============================================
# RUN EVERYTHING
# ============================================
if __name__ == "__main__":
    print("=" * 55)
    print("Day 7 - Scoring Prompt Tuning")
    print("Validating Top-3 deals vs Zoho sample records")
    print("=" * 55)

    print("\n Sending deals to Groq for scoring...")
    result = get_top3_deals(zoho_sample_records)

    if not result:
        print("No result received. Check API key.")
        sys.exit(1)

    top3 = result.get("top_3_deals", [])

    print("\n TOP 3 DEALS SELECTED BY AI:")
    for deal in top3:
        print(f"\n  Rank {deal['rank']}: {deal['institution']}")
        print(f"  Deal ID : {deal['deal_id']}")
        print(f"  Score   : {deal['total_score']}")
        print(f"  Reason  : {deal['reason']}")

    print(f"\n Validation Notes: {result.get('validation_notes', '')}")

    # Validate AI picks against Zoho records
    validate_against_zoho(top3, zoho_sample_records)

    # Save output
    with open("top3_deals_output.json", "w") as f:
        json.dump(result, f, indent=2)

    print("\n Output saved to top3_deals_output.json")
    print("=" * 55)