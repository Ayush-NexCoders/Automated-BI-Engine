"""
APARNA - DAY 10: FINAL PROMPT LIBRARY
======================================
This file is the single source of truth for all
Groq prompts used in the Automated BI Engine.

If anyone wants to change how the AI writes the
report, they only need to edit THIS file.
"""

# ============================================
# GROQ CONFIGURATION
# ============================================
GROQ_CONFIG = {
    "api_url": "https://api.groq.com/openai/v1/chat/completions",
    "model": "llama-3.3-70b-versatile",
    "max_tokens": 1000,
    "temperature": 0.7,
    "api_key_env_variable": "GROQ_API_KEY"
}

# ============================================
# PROMPT VERSION HISTORY
# ============================================
PROMPT_VERSION = "v2"
PROMPT_LAST_UPDATED = "2025-06-27"
PROMPT_UPDATED_BY = "Aparna"

# ============================================
# PROMPT 1: MAIN KPI ANALYSIS PROMPT (FINAL)
# Used in: Day 5, Day 6, Day 8
# Version: V2 (selected after UAT on Day 9)
# ============================================
def get_kpi_analysis_prompt(kpi_data):
    """
    Main prompt that analyzes weekly KPI data.
    Takes kpi_data (dict) and returns a prompt string.
    Groq will return: narrative + recommendations + top 3 deals
    """
    import json
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
    "week": "{kpi_data.get('week', '')}",
    "total_value": {kpi_data.get('total_value', 0)},
    "total_deals": {kpi_data.get('total_deals', 0)}
}}

KPI DATA:
{json.dumps(kpi_data, indent=2)}
"""


# ============================================
# PROMPT 2: SCORING PROMPT (FINAL)
# Used in: Day 7
# Version: V1 (validated against Zoho records)
# ============================================
def get_scoring_prompt(deals):
    """
    Prompt that scores deals and picks Top 3.
    Takes deals (list) and returns a prompt string.
    Groq will return: top 3 ranked deals with scores
    """
    import json
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
{json.dumps(deals, indent=2)}

Respond ONLY in this exact JSON format:
{{
    "top_3_deals": [
        {{
            "rank": 1,
            "deal_id": "ID here",
            "institution": "name here",
            "total_score": 0,
            "reason": "one sentence why this deal is top priority"
        }},
        {{
            "rank": 2,
            "deal_id": "ID here",
            "institution": "name here",
            "total_score": 0,
            "reason": "one sentence why"
        }},
        {{
            "rank": 3,
            "deal_id": "ID here",
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
# PROMPT 3: NARRATIVE PROMPT (FINAL)
# Used in: Day 3
# Version: V1
# ============================================
def get_narrative_prompt(data):
    """
    Prompt that generates executive narrative only.
    Used when only the story paragraph is needed.
    """
    import json
    return f"""
You are writing a short executive summary for a founder.
Write 3-4 sentences summarizing this week's business performance.
Be specific with numbers. Use simple language.

DATA:
{json.dumps(data, indent=2)}

Respond ONLY in this JSON format:
{{
    "narrative": "your 3-4 sentence summary here"
}}
"""


# ============================================
# PRINT SUMMARY WHEN FILE IS RUN
# ============================================
if __name__ == "__main__":
    print("=" * 55)
    print("APARNA - FINAL PROMPT LIBRARY")
    print("=" * 55)
    print(f"\n Prompt Version  : {PROMPT_VERSION}")
    print(f" Last Updated    : {PROMPT_LAST_UPDATED}")
    print(f" Updated By      : {PROMPT_UPDATED_BY}")
    print(f"\n Groq Model      : {GROQ_CONFIG['model']}")
    print(f" API URL         : {GROQ_CONFIG['api_url']}")
    print(f" Temperature     : {GROQ_CONFIG['temperature']}")
    print(f"\n Prompts Available:")
    print("   1. get_kpi_analysis_prompt()  → narrative + recs + top 3")
    print("   2. get_scoring_prompt()       → top 3 deals with scores")
    print("   3. get_narrative_prompt()     → executive summary only")
    print("\n To use in any file:")
    print("   from Aparna.Day10_Prompt_Library.prompt_library import get_kpi_analysis_prompt")
    print("\n" + "=" * 55)
    print(" Prompt library locked and ready for production!")
    print("=" * 55)