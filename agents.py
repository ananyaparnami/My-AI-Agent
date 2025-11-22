import os
import google.generativeai as genai
from dotenv import load_dotenv
from tools import google_search_tool
import sys

# --- 1. Setup ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: API Key nahi mili! .env file check karo.")
    sys.exit()

genai.configure(api_key=api_key)

# --- 2. AUTO-DETECT MODEL (Universal Fix) ---
print("🔍 Checking compatible models...")
MODEL_NAME = "gemini-pro" # Fallback (Sabse purana aur reliable)

try:
    # Check karo ki list mein kya available hai
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            name = m.name.replace('models/', '')
            # Agar Flash mil jaye toh best hai
            if 'flash' in name:
                MODEL_NAME = name
                break
            # Agar 1.5 Pro mil jaye
            elif 'gemini-1.5-pro' in name:
                MODEL_NAME = name
except Exception as e:
    print(f"⚠️ Auto-detect fail hua, using default: {MODEL_NAME}")

print(f"✅ LOCKED ON MODEL: {MODEL_NAME}")

# --- 3. AGENTS SETUP ---

hunter_agent = genai.GenerativeModel(
    model_name=MODEL_NAME,
    tools=[google_search_tool],
    system_instruction="You are a Hackathon Finder. Find live AI hackathons using Google Search."
)

brainstorm_agent = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction="You are a Creative Genius. Give 3 winning project ideas for any hackathon theme."
)

tutor_agent = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction="You are a Study Planner. Create detailed weekly schedules for exams like GATE."
)

# --- 4. ROUTER FUNCTION ---
def router_decision(user_query):
    router = genai.GenerativeModel(MODEL_NAME)
    prompt = f"Who should handle this: '{user_query}'? Reply ONLY: 'HUNTER', 'BRAINSTORM', or 'TUTOR'."
    try:
        response = router.generate_content(prompt)
        return response.text.strip()
    except:
        return "TUTOR"