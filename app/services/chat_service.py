import json
from app.dependencies import get_agent_executor
from langchain_core.messages import HumanMessage
from datetime import datetime
import re


async def chat_stream(data: str, conversation_id: str = "abc123"):
    """Handles streaming chat responses from LangChain."""
    tool_mapper = {
        "duckduckgo_search": "Searching the internet for relevant information",
        "tavily_search_results_json": "Searching the internet for relevant information",
        "searxNG_search": "Searching the internet for relevant information",
        "show_map" : "Showing a map of the location",
        "rag_tool": "Searching for land use and crop data"
    }
    config = {"configurable": {"thread_id": conversation_id}}
    try:
        async for chunk in get_agent_executor().astream_events({"messages": [HumanMessage(content=data)]}, config, stream_mode="messages", version="v2"):
            kind = chunk["event"]

            if kind == "on_chat_model_stream":
                content = chunk["data"]["chunk"].content
                if content:
                    yield chat_response(conversation_id, content, "")
            elif kind in ("on_tool_start"): #, "on_tool_end"):
                tool_name = chunk["name"]
                if(tool_name == "show_map"):
                    yield chat_response(conversation_id, {"location": chunk["data"]["input"]["location"], "type": chunk["data"]["input"]["type"]} , tool_name)
                # else:
                #     message = f"{tool_mapper.get(tool_name, tool_name)}"
                #     yield chat_response(conversation_id, message, tool_name)
            elif kind == "on_tool_end":
                tool_name = chunk["name"]
                if(tool_name == 'rag_retriever'):
                    msg_content = chunk["data"]["output"].content
                    match = re.search(r'^(.*?)==========', msg_content, re.MULTILINE)
                    first_filename = match.group(1).strip() if match else ""
                    yield chat_response(conversation_id, first_filename, tool_name)
                    

        yield chat_response(conversation_id, "", "", "stop")
    except Exception as e:
        yield json.dumps({"error": str(e)}) + "\n"


def chat_response(conversation_id, content, tool, finish_reason=None):
    response = {
        "conversation_id": conversation_id,
        "object": "chat.completion.chunk",
        "created": str(datetime.now().timestamp()),
        "model": "gemini-2.0-flash",
        "system_fingerprint": "agro-ai",
        "choices": [
            {
                "index": 0,
                "delta": {
                    "content": content,
                    "tool": tool
                },
                "logprobs": None,
                "finish_reason": finish_reason
            }
        ]
    }
    
    return "data: " + json.dumps(response) + "\n\n"
