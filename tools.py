import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def google_search_tool(query: str):
    """
    Executes a Google Custom Search to retrieve relevant information.
    
    Args:
        query (str): The search term or question.
        
    Returns:
        str: A formatted string containing titles, links, and snippets of the top 3 results.
    """
    print(f"\n[System] Executing Google Search for: {query}...")
    
    try:
        service = build("customsearch", "v1", developerKey=SEARCH_API_KEY)
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=3).execute()
        results = res.get('items', [])
        
        if not results:
            return "No relevant results found."
        
        formatted_results = ""
        for item in results:
            formatted_results += f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}\n\n"
            
        return formatted_results
        
    except Exception as e:
        return f"Error executing search: {str(e)}"