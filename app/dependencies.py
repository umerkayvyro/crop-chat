from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from app.services.maprefer import show_map
from app.config import settings
from app.services.searxng import searxNG_search
from app.services.rag_tool import create_retrieval_tool
import datetime


# Setup LangChain Agent
memory = MemorySaver()
model = ChatGoogleGenerativeAI(
    model=settings.GOOGLE_MODEL, 
    temperature=settings.TEMPERATURE, 
    streaming=settings.STREAMING
)

def get_agent_executor():
    return agent_executor

async def init_agent():

    global agent_executor
    # search = DuckDuckGoSearchRun(max_results=4)
    # search = searxNG_search
    search = TavilySearchResults(max_results=2)
    rag = await create_retrieval_tool()
    tools = [search, show_map, rag]

    agent_executor = create_react_agent(
        model, tools, checkpointer=memory, 
        prompt=SystemMessage(
            "You are an AI expert in agricultural data with tools to access data and generate insights. "
            "Your primary focus is on agriculture in Pakistan. "
            "Whenever user or you mention a location, use show_map to show the map of that location."
            "Tools:"
            "For land use and crop data, you can use the RAG tool."
            "You can use web search tools to find information on the internet. "
            "If you dont find data in RAG, you can use web search."
            "Do multiple tool calls for multiple locations"
            f"Today is {datetime.datetime.now().strftime('%Y-%m-%d')}"
        )
    )
