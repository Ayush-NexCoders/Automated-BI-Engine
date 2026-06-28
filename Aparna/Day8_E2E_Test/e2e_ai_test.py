import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ============================================
# STEP 1: REAL KPI PAYLOAD
# This simulates what comes from Zoho/pipeline
# ============================================
try:
    import pandas as pd
    import sys
    sys.path.append("C:\\Users\\ASUS\\Automated-BI-Engine")

    zoho_df = pd.read_csv(
        "C:\\Users\\ASUS\\Automated-BI-Engine\\Harshit\\data\\zoho_data.csv"
    )
    meta_df = pd.read_csv(
        "C:\\Users\\ASUS\\Automated-BI-Engine\\Harshit\\data\\meta_data.csv"
    )

    real_kpi_payload = {
        "week": "June 23-27, 2025",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_deals": len(zoho_df),
        "total_value": int(zoho_df['value'].sum()),
        "avg_score": round(zoho_df['value'].mean(), 1),
        "top_segments": list(zoho_df['segment'].dropna().unique()),
        "total_impressions": int(meta_df['impressions'].sum()),
        "total_reach": int(meta_df['reach'].sum()),
        "total_engagement": int(meta_df['engagement'].sum()),
        "deals": zoho_df.rename(columns={
            "customer": "institution"
        }).to_dict(orient='records')
    }
    print(f"Real data loaded! Deals: {len(zoho_df)}, Value: {real_kpi_payload['total_value']}")

except Exception as e:
    print(f"Could not load real data: {e}")
    real_kpi_payload = {
        "week": "June 23-27, 2025",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_deals": 15,
        "total_value": 620000,
        "avg_score": 78.2,
        "top_segments": ["Universities", "Corporates", "Schools"],
        "deals": []
    }

# ============================================
# STEP 2: SEND TO GROQ
# ============================================
def send_to_groq(kpi_data):
    prompt = f"""
You are a business intelligence analyst for an Indian B2B company.

Analyze this KPI data and respond ONLY in this exact JSON format:
{{
    "narrative": "3-4 sentence summary of this week performance",
    "recommendations": [
        "recommendation 1",
        "recommendation 2",
        "recommendation 3"
    ],
    "top_3_deals": [
        {{
            "rank": 1,
            "institution": "name",
            "segment": "type",
            "value": 0,
            "score": 0,
            "action": "what to do next"
        }},
        {{
            "rank": 2,
            "institution": "name",
            "segment": "type",
            "value": 0,
            "score": 0,
            "action": "what to do next"
        }},
        {{
            "rank": 3,
            "institution": "name",
            "segment": "type",
            "value": 0,
            "score": 0,
            "action": "what to do next"
        }}
    ],
    "week": "{kpi_data['week']}",
    "total_value": {kpi_data['total_value']},
    "total_deals": {kpi_data['total_deals']}
}}

KPI DATA:
{json.dumps(kpi_data, indent=2)}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }

    print("  Sending to Groq AI...")
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
        print("Parse error, raw response:", raw)
        return {}


# ============================================
# STEP 3: BUILD HTML REPORT
# This is the HTML template part
# ============================================
def build_html_report(ai_output):
    top3_html = ""
    for deal in ai_output.get("top_3_deals", []):
        top3_html += f"""
        <div class="deal-card">
            <div class="rank">#{deal['rank']}</div>
            <div class="deal-info">
                <h3>{deal['institution']}</h3>
                <p><strong>Segment:</strong> {deal['segment']}</p>
                <p><strong>Value:</strong> ₹{deal['value']:,}</p>
                <p><strong>Score:</strong> {deal['score']}/100</p>
                <p><strong>Action:</strong> {deal['action']}</p>
            </div>
        </div>
"""

    recommendations_html = ""
    for i, rec in enumerate(ai_output.get("recommendations", []), 1):
        recommendations_html += f"<li>{rec}</li>"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Weekly BI Report - {ai_output.get('week', '')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: #1a3c5e;
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .header p {{ margin: 5px 0 0 0; opacity: 0.8; }}
        .stats-row {{
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-box {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            flex: 1;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .stat-box h2 {{
            color: #1a3c5e;
            font-size: 32px;
            margin: 0;
        }}
        .stat-box p {{
            color: #666;
            margin: 5px 0 0 0;
        }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #1a3c5e;
            border-bottom: 2px solid #1a3c5e;
            padding-bottom: 10px;
        }}
        .deal-card {{
            display: flex;
            align-items: flex-start;
            gap: 15px;
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-bottom: 10px;
        }}
        .rank {{
            background: #1a3c5e;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }}
        .deal-info h3 {{ margin: 0 0 8px 0; color: #1a3c5e; }}
        .deal-info p {{ margin: 3px 0; font-size: 14px; }}
        ul li {{ margin-bottom: 8px; line-height: 1.5; }}
        .footer {{
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Weekly Business Intelligence Report</h1>
        <p>Week: {ai_output.get('week', '')} | Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    </div>

    <div class="stats-row">
        <div class="stat-box">
            <h2>{ai_output.get('total_deals', 0)}</h2>
            <p>Total Deals</p>
        </div>
        <div class="stat-box">
            <h2>₹{ai_output.get('total_value', 0):,}</h2>
            <p>Total Value</p>
        </div>
        <div class="stat-box">
            <h2>3</h2>
            <p>Priority Deals</p>
        </div>
    </div>

    <div class="section">
        <h2>Executive Narrative</h2>
        <p>{ai_output.get('narrative', '')}</p>
    </div>

    <div class="section">
        <h2>Top 3 Priority Deals</h2>
        {top3_html}
    </div>

    <div class="section">
        <h2>Strategic Recommendations</h2>
        <ul>
            {recommendations_html}
        </ul>
    </div>

    <div class="footer">
        Automated BI Engine | Aparna - Day 8 End-to-End Test
    </div>
</body>
</html>"""

    return html


# ============================================
# RUN THE FULL END TO END TEST
# ============================================
if __name__ == "__main__":
    print("=" * 55)
    print("Day 8 - End-to-End AI Test")
    print("real KPI → Groq → JSON → HTML Report")
    print("=" * 55)

    # STEP 1
    print("\n STEP 1: KPI data ready")
    print(f"  Deals: {real_kpi_payload['total_deals']}")
    print(f"  Total Value: ₹{real_kpi_payload['total_value']:,}")

    # STEP 2
    print("\n STEP 2: Sending to Groq AI...")
    ai_output = send_to_groq(real_kpi_payload)

    if not ai_output:
        print("Failed! Check API key.")
        exit(1)

    print("  Groq responded successfully!")

    # Save JSON output
    with open("e2e_output.json", "w") as f:
        json.dump(ai_output, f, indent=2)
    print("  JSON saved to e2e_output.json")

    # STEP 3
    print("\n STEP 3: Building HTML report...")
    html = build_html_report(ai_output)

    with open("weekly_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("  HTML report saved to weekly_report.html")

    # FINAL SUMMARY
    print("\n" + "=" * 55)
    print("END-TO-END TEST COMPLETE!")
    print("=" * 55)
    print(f"\n Narrative: {ai_output.get('narrative', '')[:100]}...")
    print(f"\n Top Deal: {ai_output.get('top_3_deals', [{}])[0].get('institution', '')}")
    print("\n Files created:")
    print("   e2e_output.json    ← structured JSON output")
    print("   weekly_report.html ← HTML report (open in browser!)")
    print("=" * 55)