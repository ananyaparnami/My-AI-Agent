import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def google_search_tool(query: str):
    """Searches Google for hackathons or study info."""
    print(f"\n🔎 Searching Google for: {query}...")
    try:
        service = build("customsearch", "v1", developerKey=SEARCH_API_KEY)
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=3).execute()
        results = res.get('items', [])
        if not results: return "No results found."
        
        formatted = ""
        for item in results:
            formatted += f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}\n\n"
        return formatted
    except Exception as e:
        return f"Error: {str(e)}"