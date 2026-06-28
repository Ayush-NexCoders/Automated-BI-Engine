import requests
import os
import json
from dotenv import load_dotenv

# Load secret API key from .env file
# Why? So key never shows in code
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# ================================================
# PART 1 - SYSTEM PROMPT PERSONA
# Why? Tells Groq AI what its job is at Indiefy
# ================================================
system_prompt = """
You are a senior business analyst for Indiefy, 
a B2B startup that sells to schools, universities, 
and corporate clients.

Every week you receive data from:
- Social Media (Instagram and LinkedIn)
- Sales data from Zoho Books
- Inventory data from Zoho Inventory

Your job is to analyze this data and write a 
clear weekly report for the founders.

IMPORTANT: Always reply in JSON format only.
No extra text. Just the JSON.
"""

# ================================================
# PART 2 - DATA CONTEXT
# Why? This is the sample business data
# In real system this comes automatically from
# Meta API, Zoho Books, and Zoho Inventory
# For now we use sample data to test the prompt
# ================================================
weekly_data = {
    "week": "June 16-20, 2025",
    "social_media": {
        "reach": 8000,
        "impressions": 12000,
        "engagements": 720,
        "engagement_rate": 9.0,
        "followers_current": 1500,
        "followers_previous": 1450,
        "follower_delta": 50
    },
    "sales_zoho_books": {
        "total_revenue": 50000,
        "new_invoices": 12,
        "pending_estimates": 5,
        "top_segment": "Universities",
        "new_customers": 3
    },
    "inventory_zoho": {
        "shipments_sent": 45,
        "pending_orders": 8,
        "low_stock_items": 2
    }
}

# ================================================
# PART 3 - OUTPUT SCHEMA
# Why? Tells AI exactly how to format the report
# This format is needed for the HTML email later
# ================================================
output_schema = """
Reply ONLY in this exact JSON format, nothing else:
{
    "wins": "write 2-3 sentences about what went well",
    "dropoffs": "write 2-3 sentences about what went wrong",
    "anomalies": "write 1-2 sentences about anything unusual",
    "recommendations": "write 3 clear action points for founders"
}
"""

# ================================================
# SENDING TO GROQ AI
# Why? To test if our prompt architecture works
# ================================================
print("Sending Indiefy weekly data to Groq AI...")
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
                "content": f"Analyze this weekly business data for Indiefy: {json.dumps(weekly_data, indent=2)}"
            }
        ]
    }
)

# Getting and printing the report
data = response.json()
print("Full Groq Response:", data)
report = data['choices'][0]['message']['content']

import json

print("✅ Groq AI Weekly Report Generated!")
print("=" * 50)

# Parse and print cleanly with gaps
try:
    report_json = json.loads(report)
    
    print("\n🏆 WINS:")
    print(report_json['wins'])
    
    print("\n📉 DROP-OFFS:")
    print(report_json['dropoffs'])
    
    print("\n⚠️ ANOMALIES:")
    print(report_json['anomalies'])
    
    print("\n💡 RECOMMENDATIONS:")
    print(report_json['recommendations'])
    
except:
    print(report)