from dotenv import load_dotenv
from pathlib import Path
import os
import google.generativeai as genai

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content("Say exactly: Gemini connection successful")

print(response.text)