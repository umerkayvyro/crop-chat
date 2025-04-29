from fastapi import HTTPException, UploadFile
import os
import mimetypes  # Import the mimetypes module
import traceback
import uuid
from typing import List, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain_community.document_loaders import (
    JSONLoader,  # Import JSONLoader
)
from langchain_core.documents import Document
# from app.dependencies import vectorstore


LOADER_MAPPING = {
    ".json": (JSONLoader, {"jq_schema": ".", "text_content": False}),  # Set text_content=False
}


SUPPORTED_MIME_TYPES = [
    "application/json",  # Support only JSON MIME type
]

async def process_documents(directory: str):
    """Processes all documents in the given directory and adds them to the vectorstore."""

    # messages = []
    chunks = []
    # try:
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {file_path}")
        mime_type = mimetypes.guess_type(file_path)[0]
        if mime_type not in SUPPORTED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {filename} (MIME type: {mime_type})",
            )

        file_extension = os.path.splitext(filename)[1]
        loader_class, loader_args = LOADER_MAPPING.get(file_extension, (None, None))
        if loader_class:
            loader = loader_class(file_path, **loader_args)
            documents = loader.load()
            # Remove the call to split_text
            # documents = split_text(documents)  # Split the text content of the documents

            # Add metadata and conversation_id
            for doc in documents:
                doc.metadata["source"] = filename

            chunks.extend(documents)
            # Generate UUIDs for the documents
            # ids = [str(uuid.uuid4()) for _ in documents]

            # vectorstore.add_documents(documents=documents, ids=ids)

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")

    # return messages
    return chunks

    # except Exception as e:
    #     print(f"Error processing documents: {e}\n{traceback.format_exc()}")
    #     raise HTTPException(status_code=500, detail=f"Document processing error: {e}")
