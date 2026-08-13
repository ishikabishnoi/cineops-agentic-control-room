from dotenv import load_dotenv
from pathlib import Path 
import os 
from supabase import create_client
env_path = Path(__file__).resolve().parent.parent / ".env" 
load_dotenv(env_path) 
url = os.getenv("NEXT_PUBLIC_SUPABASE_URL") 
key = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY") 
supabase = create_client(url, key)
response = ( supabase .table("production_reports") .select("report_id, production_status") .limit(3) .execute() ) 
print(response.data)