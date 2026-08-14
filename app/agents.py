import json
import os
from functools import lru_cache

from google import genai
from google.genai import types


MODEL_NAME = "gemini-3.5-flash-lite"


@lru_cache(maxsize=1)
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    return genai.Client(api_key=api_key)


def generate_json(prompt):
    response = get_gemini_client().models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return json.loads(response.text)


def run_schedule_agent(schedule_kpis):
    prompt = f"""
You are a film production scheduling specialist.

Analyze these KPIs and return ONLY valid JSON.

KPIs:
{json.dumps(schedule_kpis)}

Return this exact structure:
{{
  "risk": "HIGH or MEDIUM or LOW",
  "finding": "one sentence",
  "action": "one sentence"
}}
"""

    return generate_json(prompt)


def run_budget_agent(budget_kpis):
    prompt = f"""
You are a film production finance specialist.

Analyze these KPIs and return ONLY valid JSON.

KPIs:
{json.dumps(budget_kpis)}

Return this exact structure:
{{
  "risk": "HIGH or MEDIUM or LOW",
  "finding": "one sentence",
  "action": "one sentence"
}}
"""

    return generate_json(prompt)


def run_executive_agent(
    primary_constraint,
    time_score,
    budget_score,
    schedule_result,
    budget_result,
):
    payload = {
        "primary_constraint": primary_constraint,
        "time_pressure_score": time_score,
        "budget_pressure_score": budget_score,
        "schedule_agent": schedule_result,
        "budget_agent": budget_result,
    }

    prompt = f"""
You are a film studio executive.

The primary operational constraint has already been determined by the analytics engine.

Analyze the specialist agent outputs and return ONLY valid JSON.

Input:
{json.dumps(payload)}

Return this exact structure:
{{
  "overall_risk": "HIGH or MEDIUM or LOW",
  "priority_action": "one short sentence",
  "executive_summary": "2-3 sentence executive summary",
  "confidence": {{
    "level": "HIGH or MEDIUM or LOW",
    "reason": "one short sentence"
  }}
}}
"""

    return generate_json(prompt)