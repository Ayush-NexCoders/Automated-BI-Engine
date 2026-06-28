import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ============================================
# SAMPLE KPI PAYLOAD (like what Ayush will send)
# ============================================
sample_kpi_payload = {
    "week": "June 16-20, 2025",
    "total_deals": 12,
    "total_value": 450000,
    "avg_score": 73.5,
    "top_segments": ["Universities", "Corporates"],
    "deals": [
        {
            "institution": "Delhi University",
            "segment": "University",
            "value": 85000,
            "score": 91,
            "age_days": 5,
            "engagement": "high",
            "payment": "advance"
        },
        {
            "institution": "TechCorp Ltd",
            "segment": "Corporate",
            "value": 120000,
            "score": 85,
            "age_days": 3,
            "engagement": "high",
            "payment": "partial"
        },
        {
            "institution": "Sunshine School",
            "segment": "School",
            "value": 45000,
            "score": 62,
            "age_days": 12,
            "engagement": "medium",
            "payment": "pending"
        }
    ]
}

# ============================================
# MAIN FUNCTION - this is what Day 5 is about
# ============================================
def post_kpi_to_groq(kpi_payload: dict) -> dict:
    """
    Takes KPI data, sends to Groq, returns narrative + recommendations
    """

    # Build the prompt
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

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    print("Sending KPI data to Groq...")
    response = requests.post(GROQ_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return {}

    # Extract the response text
    raw_text = response.json()["choices"][0]["message"]["content"]

    # Parse the JSON response
    try:
        # Clean up in case Groq adds extra text around the JSON
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        clean_json = raw_text[start:end]
        result = json.loads(clean_json)
    except Exception as e:
        print("Could not parse JSON, showing raw response:")
        print(raw_text)
        return {"raw": raw_text}

    return result


# ============================================
# RUN IT
# ============================================
if __name__ == "__main__":
    print("=" * 55)
    print("Groq Integration Function - Day 5")
    print("=" * 55)

    result = post_kpi_to_groq(sample_kpi_payload)

    if result:
        print("\n NARRATIVE:")
        print(result.get("narrative", "No narrative found"))

        print("\n RECOMMENDATIONS:")
        recommendations = result.get("recommendations", [])
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")

    print("\n" + "=" * 55)
    print("Done!")