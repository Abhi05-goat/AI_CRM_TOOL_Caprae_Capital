import json
from utils.llm_client import call_llm

GENERAL_SYSTEM_PROMPT = """
You are a structured company intelligence assistant for a venture capital fund. You extract useful investment signals from company descriptions. Always return valid JSON. Use your best judgment when inferring missing info. Do NOT include revenue here.
"""

GENERAL_USER_TEMPLATE = """
From the company text, extract and infer the following:

1. Whether the company fits Caprae’s thesis (founder-led, SaaS, high growth).
2. Key executive: name and title.
3. Executive email (if available).
4. Business model or industry: summarize in plain terms, and give a confidence rating.
5. Funding stage: estimate (e.g. "Seed", "Series A", "Bootstrapped", "Public", etc.) and confidence.
6. Additional insights: 2–4 notable qualitative takeaways (e.g. product strategy, geography, uniqueness).
7. 3–5 competitors (if available).

Return valid JSON:

{
  "fit_with_caprae_thesis": true,
  "founder_exec": {
    "name": "",
    "title": ""
  },
  "executive_email": null,
  "business_model_industry": {
    "value": "",
    "confidence": ""
  },
  "funding_stage": {
    "value": "",
    "confidence": ""
  },
  "additional_insights": [
    { "value": "", "confidence": "" },
    { "value": "", "confidence": "" }
  ],
  "competitors": ["", "", ""]
}
"""

REVENUE_SYSTEM_PROMPT = "You are a financial analyst AI. Estimate revenue from company descriptions."
REVENUE_USER_TEMPLATE = """
From the following company description, estimate the company's annual revenue or revenue range. If no revenue is mentioned, try to estimate a ballpark figure based on context. Be honest if confidence is low.

Return ONLY this JSON:
{
  "value": "$10-50M",
  "confidence": "Medium"
}
"""

def enrich_company_features(text: str) -> dict:
    prompt = GENERAL_USER_TEMPLATE + "\n\n" + text
    for _ in range(3):
        try:
            response = call_llm(prompt, system=GENERAL_SYSTEM_PROMPT)
            content = response.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(content)
            return parsed
        except Exception:
            continue
    return {"error": "Failed to extract company enrichment details after multiple attempts."}

def extract_revenue_estimate(text: str) -> dict:
    prompt = REVENUE_USER_TEMPLATE + "\n\n" + text
    for _ in range(3):
        try:
            response = call_llm(prompt, system=REVENUE_SYSTEM_PROMPT)
            content = response.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except Exception:
            continue
    return {
        "value": "Not found",
        "confidence": "Low"
    }
