import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# ================================================
# INPUT DATA — Sample for Testing
# In real system this comes automatically from
# Ayush's kpi_aggregator and pipeline_scoring
# ================================================

# TRENDS — week over week changes
# Will update field names when Ayush finishes
trends_data = {
    "week": "June 16-20, 2025",
    
    "social_media_trends": {
        "reach_change": +500,          # went up by 500
        "impressions_change": +2000,   # went up by 2000
        "engagement_rate_change": -1.2, # went DOWN by 1.2%
        "follower_delta": +50          # gained 50 followers
    },
    
    "sales_trends": {
        "revenue_change": +15000,      # went up by 15000
        "revenue_change_percent": 43,  # 43% increase
        "new_invoices_change": +3,     # 3 more invoices
        "pending_estimates": 5,        # 5 still waiting
        "conversion_rate": 6.6         # only 6.6% converting
    },
    
    "inventory_trends": {
        "pending_orders_change": +3,   # 3 more pending
        "low_stock_items": 2,          # 2 items low
        "shipment_rate": 45            # sent 45 this week
    }
}

# PIPELINE SCORES — from Ayush's pipeline_scoring.py
# Score 0-100: higher = more likely to close/buy soon
# Will update when Ayush finishes pipeline_scoring.py
pipeline_scores = {
    "top_deals": [
        {
            "client": "Delhi University",
            "segment": "University",
            "score": 87,
            "estimated_value": 25000,
            "status": "estimate_sent",
            "days_pending": 3
        },
        {
            "client": "TechCorp India",
            "segment": "Corporate",
            "score": 74,
            "estimated_value": 18000,
            "status": "in_discussion",
            "days_pending": 7
        },
        {
            "client": "St. Mary School",
            "segment": "School",
            "score": 61,
            "estimated_value": 8000,
            "status": "estimate_sent",
            "days_pending": 5
        },
        {
            "client": "Mumbai Institute",
            "segment": "University",
            "score": 45,
            "estimated_value": 32000,
            "status": "first_contact",
            "days_pending": 14
        },
        {
            "client": "Retail Chain Co",
            "segment": "Corporate",
            "score": 28,
            "estimated_value": 12000,
            "status": "cold_lead",
            "days_pending": 21
        }
    ],
    "total_pipeline_value": 95000,
    "high_priority_count": 2
}

# ================================================
# RECOMMENDATIONS PROMPT
# Tells Groq exactly how to prioritize actions
# ================================================
system_prompt = """
You are a strategic business advisor for Indiefy,
a B2B startup selling to schools, universities,
and corporate clients.

You receive two inputs every week:
1. TRENDS — what went up and what went down
2. PIPELINE SCORES — which deals are hottest

Your job is to give founders 3 to 5 specific
actions they must take THIS WEEK ranked from
most important to least important.

RULES:
1. Most urgent action always comes first
2. Be very specific — name actual clients and numbers
3. Focus on actions that make money first
4. Keep each action to 1-2 sentences maximum
5. Always respond in JSON format only
"""

output_schema = """
Reply ONLY in this exact JSON format, nothing else:
{
    "priority_actions": [
        {
            "rank": 1,
            "action": "specific action to take",
            "reason": "why this is most important",
            "expected_outcome": "what will happen if you do this"
        },
        {
            "rank": 2,
            "action": "specific action to take",
            "reason": "why this matters",
            "expected_outcome": "what will happen if you do this"
        },
        {
            "rank": 3,
            "action": "specific action to take",
            "reason": "why this matters",
            "expected_outcome": "what will happen if you do this"
        }
    ],
    "total_opportunity_value": "total value if all actions completed"
}
"""

# ================================================
# SEND TO GROQ AI
# ================================================
print("Generating Indiefy Weekly Recommendations...")
print("=" * 55)

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": system_prompt + output_schema
            },
            {
                "role": "user",
                "content": f"Generate prioritised recommendations based on these trends and pipeline scores: TRENDS: {json.dumps(trends_data, indent=2)} PIPELINE SCORES: {json.dumps(pipeline_scores, indent=2)}"
            }
        ]
    }
)

# ================================================
# CLEAN OUTPUT
# ================================================
data = response.json()
report = data['choices'][0]['message']['content']

try:
    report_json = json.loads(report)

    print("\n🎯 THIS WEEK'S PRIORITY ACTIONS FOR INDIEFY:")
    print("=" * 55)

    for action in report_json['priority_actions']:
        print(f"\n#{action['rank']} — {action['action']}")
        print(f"   Why: {action['reason']}")
        print(f"   Outcome: {action['expected_outcome']}")

    print(f"\n💰 Total Opportunity Value: "
          f"{report_json['total_opportunity_value']}")

except:
    print(report)