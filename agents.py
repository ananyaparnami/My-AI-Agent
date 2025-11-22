import os
import google.generativeai as genai
from dotenv import load_dotenv
from tools import google_search_tool
import sys

# 1. Configuration and Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Critical Error: GOOGLE_API_KEY not found. Please verify your .env file configuration.")
    sys.exit()

genai.configure(api_key=api_key)

# 2. Model Configuration
# YOUR LIST SHOWS 'gemini-2.0-flash', SO WE USE THAT EXACTLY.
MODEL_NAME = 'gemini-2.0-flash' 

print(f"[System] Initialized with Model: {MODEL_NAME}")

# 3. Agent Definitions

# Agent 1: The Hunter (Information Retrieval)
hunter_agent = genai.GenerativeModel(
    model_name=MODEL_NAME,
    tools=[google_search_tool],
    system_instruction="You are a Hackathon Retrieval Specialist. Your objective is to find live, upcoming Data Science and AI hackathons using the provided Google Search tool. Be precise and strictly factual."
)

# Agent 2: The Ideator (Creative Brainstorming)
brainstorm_agent = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction="You are a Creative Solution Architect. When provided with a hackathon theme, generate 3 unique, high-impact project ideas. For each idea, outline the Problem Statement, Proposed Solution, and Recommended Tech Stack."
)

# Agent 3: The Tutor (Academic Planning)
tutor_agent = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction="You are an Expert Academic Advisor. Your task is to create detailed, week-by-week study schedules for competitive exams like GATE DA. Prioritize a balance between theoretical concepts and practical application."
)

# 4. Router Logic
def router_decision(user_query):
    """
    Determines the intent of the user query and routes it to the appropriate agent.
    """
    router = genai.GenerativeModel(MODEL_NAME)
    prompt = (
        f"Analyze the intent of this user query: '{user_query}'. "
        "Route it to the most suitable agent. "
        "Reply ONLY with one of the following keywords: 'HUNTER' (for searching events/hackathons), "
        "'BRAINSTORM' (for generating ideas), or 'TUTOR' (for study plans/academic advice)."
    )
    try:
        return router.generate_content(prompt).text.strip()
    except Exception as e:
        # Fallback to Tutor agent in case of routing failure
        return "TUTOR"