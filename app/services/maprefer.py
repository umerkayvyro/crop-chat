from langchain.tools import tool

@tool
async def show_map(location: str, type: str):
    """
    Call this tool whenever user refers to a location in Pakistan to show them a map
    args:
        location: str: Name of the location in Pakistan
        type: str: District or Province
    return:
        str
    """
    try:
        return "User is being shown the map"
    except Exception as e:
        return f"Error retrieving information: {str(e)}"