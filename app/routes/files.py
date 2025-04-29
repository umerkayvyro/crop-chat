from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import List
import json

router = APIRouter(prefix="/files", tags=["files"])

@router.get("/json/{file_name}", response_model=dict)
async def get_json_file(file_name: str):
    shared_docs_path = Path("/Users/vyromacbook/Desktop/langchain-agent/cricket-chatbot/shared_docs")
    file_path = shared_docs_path / file_name
    if not file_path.exists() or file_path.suffix != ".json":
        raise HTTPException(status_code=404, detail="File not found")
    with file_path.open("r") as file:
        return json.load(file)
