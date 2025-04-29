from langchain.tools import tool
from langchain_community.utilities import SearxSearchWrapper
import traceback

@tool
async def searxNG_search(query: str):
    """SearxNG internet search engine. It can be used to search for any information on the web."""
    try:
        print(f"Searching for: {query}")
        result = SearxSearchWrapper().run(query)
        print(result)
        return result
    except Exception as e:
        traceback.print_exc()
        return f"Error retrieving information: {str(e)}"
