from app.kpis import get_schedule_kpis, get_budget_kpis
from app.agents import run_schedule_agent
from app.agents import run_schedule_agent, run_budget_agent, run_executive_agent
from app.kpis import get_schedule_kpis, get_budget_kpis, detect_primary_constraint
from fastapi import FastAPI 
from dotenv import load_dotenv
from pathlib import Path 
import os 
from supabase import create_client 
import google.generativeai as genai
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path, override=True)
print("ENV PATH:", env_path)
print("NEXT_PUBLIC_SUPABASE_URL:", os.getenv("NEXT_PUBLIC_SUPABASE_URL"))
supabase = create_client( os.getenv("NEXT_PUBLIC_SUPABASE_URL"), os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY") ) 
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) 
model = genai.GenerativeModel("gemini-3.5-flash-lite") 
app = FastAPI() 
@app.post("/analyze")
def analyze():
    data = (
        supabase.table("production_reports")
        .select("*")
        .order("report_date", desc=True)
        .limit(50)
        .execute()
        .data
    )

    summary_data = {
        "scheduled_scenes": sum(r["scenes_scheduled"] for r in data),
        "completed_scenes": sum(r["scenes_completed"] for r in data),
    }

    schedule_kpis = get_schedule_kpis(data)
    budget_kpis = get_budget_kpis(data)

    primary_constraint, time_score, budget_score = detect_primary_constraint( schedule_kpis, budget_kpis )

    schedule_result = run_schedule_agent(schedule_kpis)
    budget_result = run_budget_agent(budget_kpis)
    executive_result = run_executive_agent( primary_constraint, 
                                           schedule_result, 
                                           budget_result )

    return {

        "primary_constraint": primary_constraint, 
        "time_pressure_score": time_score,
        "budget_pressure_score": budget_score,

        "schedule_kpis": schedule_kpis,
        "schedule_agent": schedule_result,

        "budget_kpis": budget_kpis,
        "budget_agent": budget_result,

        "executive_agent": executive_result,
    }