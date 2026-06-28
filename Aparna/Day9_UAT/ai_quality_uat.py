import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ============================================
# SAME KPI DATA AS DAY 8
# ============================================
kpi_payload = {
    "week": "June 23-27, 2025",
    "total_deals": 15,
    "total_value": 620000,
    "avg_score": 78.2,
    "top_segments": ["Universities", "Corporates", "Schools"],
    "deals": [
        {
            "deal_id": "ZB001",
            "institution": "IIT Delhi",
            "segment": "University",
            "value": 150000,
            "score": 95,
            "payment_status": "paid",
            "last_contact_days": 2,
            "engagement": "high"
        },
        {
            "deal_id": "ZB002",
            "institution": "Infosys Ltd",
            "segment": "Corporate",
            "value": 200000,
            "score": 88,
            "payment_status": "partial",
            "last_contact_days": 4,
            "engagement": "high"
        },
        {
            "deal_id": "ZB003",
            "institution": "DPS School",
            "segment": "School",
            "value": 55000,
            "score": 65,
            "payment_status": "pending",
            "last_contact_days": 8,
            "engagement": "medium"
        },
        {
            "deal_id": "ZB004",
            "institution": "Delhi University",
            "segment": "University",
            "value": 95000,
            "score": 92,
            "payment_status": "paid",
            "last_contact_days": 1,
            "engagement": "high"
        },
        {
            "deal_id": "ZB005",
            "institution": "TCS Mumbai",
            "segment": "Corporate",
            "value": 175000,
            "score": 85,
            "payment_status": "partial",
            "last_contact_days": 3,
            "engagement": "high"
        }
    ]
}

# ============================================
# VERSION 1 PROMPT - Original (from Day 8)
# ============================================
def prompt_v1(kpi_data):
    return f"""
You are a business intelligence analyst for an Indian B2B company.
Analyze this KPI data and respond ONLY in this exact JSON format:
{{
    "narrative": "3-4 sentence summary of this week performance",
    "recommendations": ["rec 1", "rec 2", "rec 3"],
    "top_3_deals": [
        {{"rank": 1, "institution": "name", "segment": "type", "value": 0, "score": 0, "action": "next step"}},
        {{"rank": 2, "institution": "name", "segment": "type", "value": 0, "score": 0, "action": "next step"}},
        {{"rank": 3, "institution": "name", "segment": "type", "value": 0, "score": 0, "action": "next step"}}
    ],
    "week": "{kpi_data['week']}",
    "total_value": {kpi_data['total_value']},
    "total_deals": {kpi_data['total_deals']}
}}
KPI DATA: {json.dumps(kpi_data, indent=2)}
"""

# ============================================
# VERSION 2 PROMPT - Improved after feedback
# More specific, founder friendly language
# ============================================
def prompt_v2(kpi_data):
    return f"""
You are a sharp B2B sales analyst writing a Monday morning briefing
for busy founders of an Indian EdTech/Corporate training company.

Write in simple, direct language. No jargon. Be specific with numbers.
Focus on: what happened, what needs urgent attention, what to do TODAY.

Respond ONLY in this exact JSON format:
{{
    "narrative": "Write exactly 3 sentences. Sentence 1: total deals and revenue this week. Sentence 2: which segment performed best and why. Sentence 3: one urgent problem that needs attention today.",
    "recommendations": [
        "Action 1: specific thing to do TODAY with a specific deal or segment",
        "Action 2: specific thing to do THIS WEEK to improve pipeline",
        "Action 3: specific thing to watch or fix to prevent revenue loss"
    ],
    "top_3_deals": [
        {{
            "rank": 1,
            "institution": "exact name",
            "segment": "University/Corporate/School",
            "value": exact_number,
            "score": exact_number,
            "action": "One specific action to take with this deal in next 24 hours"
        }},
        {{
            "rank": 2,
            "institution": "exact name",
            "segment": "University/Corporate/School",
            "value": exact_number,
            "score": exact_number,
            "action": "One specific action to take with this deal in next 24 hours"
        }},
        {{
            "rank": 3,
            "institution": "exact name",
            "segment": "University/Corporate/School",
            "value": exact_number,
            "score": exact_number,
            "action": "One specific action to take with this deal in next 24 hours"
        }}
    ],
    "week": "{kpi_data['week']}",
    "total_value": {kpi_data['total_value']},
    "total_deals": {kpi_data['total_deals']}
}}

KPI DATA:
{json.dumps(kpi_data, indent=2)}
"""

# ============================================
# SEND TO GROQ
# ============================================
def send_to_groq(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(GROQ_URL, headers=headers, json=body)
    if response.status_code != 200:
        print("ERROR:", response.status_code)
        return {}
    raw = response.json()["choices"][0]["message"]["content"]
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        return {}

# ============================================
# RATING FUNCTION
# Simulates founder giving feedback/rating
# ============================================
def rate_output(version, result):
    print(f"\n {'='*50}")
    print(f" PROMPT {version} OUTPUT")
    print(f" {'='*50}")
    print(f"\n NARRATIVE:")
    print(f" {result.get('narrative', '')}")
    print(f"\n RECOMMENDATIONS:")
    for i, rec in enumerate(result.get('recommendations', []), 1):
        print(f"  {i}. {rec}")
    print(f"\n TOP DEAL: {result.get('top_3_deals', [{}])[0].get('institution', '')}")
    print(f" ACTION: {result.get('top_3_deals', [{}])[0].get('action', '')}")


# ============================================
# RUN UAT - Compare V1 vs V2
# ============================================
if __name__ == "__main__":
    print("=" * 55)
    print("Day 9 - AI Quality UAT")
    print("Comparing V1 prompt vs V2 improved prompt")
    print("=" * 55)

    # Run V1
    print("\n Running PROMPT V1 (original)...")
    result_v1 = send_to_groq(prompt_v1(kpi_payload))
    rate_output("V1 (Original)", result_v1)

    # Simulated founder feedback
    print("\n" + "="*55)
    print(" FOUNDER FEEDBACK ON V1:")
    print("  - Narrative too vague, not specific enough")
    print("  - Recommendations not actionable")
    print("  - Need to know WHAT TO DO TODAY specifically")
    print(" ITERATING PROMPT → V2")
    print("="*55)

    # Run V2
    print("\n Running PROMPT V2 (improved after feedback)...")
    result_v2 = send_to_groq(prompt_v2(kpi_payload))
    rate_output("V2 (Improved)", result_v2)

    # Save both outputs
    uat_report = {
        "uat_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "v1_output": result_v1,
        "v2_output": result_v2,
        "feedback": "V1 was too vague. V2 improved with specific actions and founder-friendly language.",
        "final_prompt_version": "V2"
    }

    with open("uat_report.json", "w", encoding="utf-8") as f:
        json.dump(uat_report, f, indent=2)

    print("\n" + "="*55)
    print(" UAT COMPLETE!")
    print(" V1 vs V2 comparison saved to uat_report.json")
    print(" V2 prompt selected as final version")
    print("="*55)