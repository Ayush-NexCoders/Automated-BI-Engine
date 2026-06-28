import os
import json
import requests
import sys
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def post_kpi_to_groq(kpi_payload: dict) -> dict:
    """
    This is your Day 5 function — now wrapped as an n8n node.
    n8n will call this function and pass real KPI data into it.
    """

    prompt = f"""
You are a business intelligence analyst. Analyze this weekly KPI data and provide:
1. A short narrative (3-4 sentences) explaining overall performance
2. Top 3 actionable recommendations

KPI DATA:
{json.dumps(kpi_payload, indent=2)}

Respond in this exact JSON format:
{{
    "narrative": "your narrative here",
    "recommendations": [
        "recommendation 1",
        "recommendation 2",
        "recommendation 3"
    ]
}}
"""

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

    print("Sending KPI payload to Groq API...")
    response = requests.post(GROQ_URL, headers=headers, json=body)

    if response.status_code != 200:
        print("ERROR:", response.status_code, response.text)
        return {"error": response.text}

    raw_text = response.json()["choices"][0]["message"]["content"]

    # Parse JSON from response
    try:
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        result = json.loads(raw_text[start:end])
    except:
        return {"raw": raw_text}

    return result


# ============================================
# n8n SIMULATION
# n8n sends data as JSON through stdin or file
# This simulates that flow
# ============================================

# This is what n8n will send as real KPI payload
# Replace this later with actual output from Ayush's schema validator
real_kpi_payload = {
    "week": "June 23, 2025",
    "total_deals": 15,
    "total_value": 620000,
    "avg_score": 78.2,
    "top_segments": ["Universities", "Corporates", "Schools"],
    "deals": [
        {
            "institution": "IIT Delhi",
            "segment": "University",
            "value": 150000,
            "score": 95,
            "age_days": 2,
            "engagement": "high",
            "payment": "advance"
        },
        {
            "institution": "Infosys Ltd",
            "segment": "Corporate",
            "value": 200000,
            "score": 88,
            "age_days": 4,
            "engagement": "high",
            "payment": "partial"
        },
        {
            "institution": "DPS School",
            "segment": "School",
            "value": 55000,
            "score": 65,
            "age_days": 8,
            "engagement": "medium",
            "payment": "pending"
        }
    ]
}


if __name__ == "__main__":
    print("=" * 55)
    print("Day 6 - Groq n8n Integration Node")
    print("Verifying data-in → AI-out flow")
    print("=" * 55)

    # Step 1: Show what data is coming IN
    print("\n DATA COMING IN (KPI Payload):")
    print(json.dumps(real_kpi_payload, indent=2))

    # Step 2: Send to Groq and get result
    print("\n Sending to Groq AI...")
    result = post_kpi_to_groq(real_kpi_payload)

    # Step 3: Show what is coming OUT
    print("\n AI OUTPUT (Narrative + Recommendations):")
    print("\n NARRATIVE:")
    print(result.get("narrative", "None"))

    print("\n RECOMMENDATIONS:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"  {i}. {rec}")

    # Step 4: Save output to JSON file
    # This is what n8n would pass to the next node (Harshit's Jinja2)
    output_path = "groq_output.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n Output saved to {output_path}")
    print("n8n data-in → AI-out flow verified!")
    print("=" * 55)