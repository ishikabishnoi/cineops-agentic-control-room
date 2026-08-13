import json
import google.generativeai as genai

model = genai.GenerativeModel("gemini-3.5-flash-lite")


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

    response = model.generate_content(prompt)
    return json.loads(response.text)


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

    response = model.generate_content(prompt)
    return json.loads(response.text)


def run_executive_agent(primary_constraint, schedule_result, budget_result):
    payload = {
        "primary_constraint": primary_constraint,
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
  "executive_summary": "2-3 sentence executive summary"
  "confidence": "HIGH or MEDIUM or LOW" 
}}
"""

    response = model.generate_content(prompt)
    return json.loads(response.text)