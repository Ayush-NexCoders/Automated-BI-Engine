import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# ================================================
# KPI JSON — Sample Data for Testing
# WHY: Right now data is written here manually
# In real system Day 5 — this data arrives 
# automatically from Akshat and Ayush's code
# Nobody writes data in code in real system!
# ================================================
kpi_data = {
    "week": "June 16-20, 2025",

    # Matches Ayush's meta_normalizer.py exactly
    "social_media": {
        "reach": 8000,
        "impressions": 12000,
        "engagements": 720,
        "engagement_rate": 9.0,
        "followers_current": 1500,
        "followers_previous": 1450,
        "follower_delta": 50
    },

    # Will update when Ayush finishes zoho_normalizer
    "sales": {
        "total_revenue": 50000,
        "revenue_last_week": 35000,
        "new_invoices": 12,
        "pending_estimates": 5,
        "top_segment": "Universities",
        "new_customers": 3
    },

    # Will update when Ayush finishes zoho_normalizer
    "inventory": {
        "shipments_sent": 45,
        "pending_orders": 8,
        "low_stock_items": 2
    }
}

# ================================================
# SYSTEM PROMPT
# This tells Groq AI exactly what its job is
# This never changes — it is the brain of system
# ================================================
system_prompt = """
You are a senior business analyst for Indiefy,
a B2B startup selling to schools, universities,
and corporate clients.

Every week you receive KPI data from:
- Social Media (Meta/Instagram and LinkedIn)
- Sales data (Zoho Books)
- Inventory data (Zoho Inventory)

You must analyze the numbers and write a 
performance narrative report for the founders.

RULES:
1. Compare this week vs last week where possible
2. Be specific — mention actual numbers
3. Keep language simple for non-analyst founders
4. Always respond in JSON format only

DEFINITIONS:
- WINS = metrics that improved or performed well
- DROP-OFFS = metrics that declined or failed
- ANOMALIES = anything unexpected or unusual
- RECOMMENDATIONS = specific actions to take
"""

# ================================================
# OUTPUT SCHEMA
# Tells Groq exactly how to format the answer
# Harshit uses this format for the HTML email
# ================================================
output_schema = """
Reply ONLY in this exact JSON format, nothing else:
{
    "wins": "2-3 sentences about what went well with specific numbers",
    "dropoffs": "2-3 sentences about what declined with specific numbers",
    "anomalies": "1-2 sentences about anything unexpected or unusual",
    "recommendations": [
        "Action 1 — specific thing to do this week",
        "Action 2 — specific thing to do this week",
        "Action 3 — specific thing to do this week"
    ]
}
"""

# ================================================
# SEND TO GROQ AI
# In real system this whole block becomes a 
# function that gets called automatically
# ================================================
print("Building Indiefy Performance Narrative...")
print("=" * 50)

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
                "content": f"Analyze this week's KPI data for Indiefy: {json.dumps(kpi_data, indent=2)}"
            }
        ]
    }
)

# ================================================
# CLEAN OUTPUT
# In real system this output goes to Harshit's
# HTML template — not printed on screen
# ================================================
data = response.json()
report = data['choices'][0]['message']['content']

try:
    report_json = json.loads(report)

    print("\n🏆 WINS:")
    print(report_json['wins'])

    print("\n📉 DROP-OFFS:")
    print(report_json['dropoffs'])

    print("\n⚠️  ANOMALIES:")
    print(report_json['anomalies'])

    print("\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(report_json['recommendations'], 1):
        print(f"  {i}. {rec}")

except:
    print(report)