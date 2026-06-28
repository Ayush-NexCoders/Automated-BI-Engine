# Prompt Update Guide
## For Startup Team — How to Update AI Prompts

---

### What is this file?
This is the instruction manual for updating the AI prompts
used in the Weekly BI Report system.

All prompts live in one file:
Aparna/Day10_Prompt_Library/prompt_library.py

---

### Groq Configuration
- Model: llama-3.3-70b-versatile
- API URL: https://api.groq.com/openai/v1/chat/completions
- API Key: stored in .env file as GROQ_API_KEY (never share this)
- Temperature: 0.7 (higher = more creative, lower = more factual)

---

### When should you update a prompt?

Update a prompt when:
- The narrative sounds wrong or unclear
- Recommendations are not useful
- Wrong deals are being prioritized
- Founders give feedback that the report is not helpful

---

### How to update a prompt — step by step

Step 1: Open this file in VS Code
        Aparna/Day10_Prompt_Library/prompt_library.py

Step 2: Find the prompt you want to change
        - Main report prompt → get_kpi_analysis_prompt()
        - Deal scoring prompt → get_scoring_prompt()
        - Narrative only prompt → get_narrative_prompt()

Step 3: Change the words inside the prompt
        The prompt is the text between the triple quotes
        Example: change "Write 3 sentences" to "Write 2 sentences"
        Example: change scoring rules if deal priorities change

Step 4: Test it by running:
        cd Aparna/Day10_Prompt_Library
        python prompt_library.py

Step 5: Run the full pipeline to confirm it works:
        cd Aparna/Day8_E2E_Test
        python e2e_ai_test.py

Step 6: Update the version number at the top of prompt_library.py
        Change PROMPT_VERSION = "v2" to "v3"
        Change PROMPT_LAST_UPDATED to today's date
        Change PROMPT_UPDATED_BY to your name

Step 7: Push to GitHub
        git add Aparna/
        git commit -m "Prompt updated to v3 - reason for change"
        git push

---

### Prompt Version History

| Version | Date       | Changed By | What Changed              |
|---------|------------|------------|---------------------------|
| v1      | 2025-06-16 | Aparna     | Initial prompt created    |
| v2      | 2025-06-26 | Aparna     | Improved after UAT feedback - more specific actions |

---

### Rules — NEVER do these

- Never delete old prompt versions, comment them out instead
- Never change the JSON format structure
- Never share the GROQ_API_KEY with anyone
- Always test before pushing to GitHub

---

### Contact
If something breaks, contact Aparna.