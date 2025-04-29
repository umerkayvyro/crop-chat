from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, home, files
from app.utils.error_handler import add_exception_handlers
from app.dependencies import init_agent

app = FastAPI(title="FastAPI LangChain Chatbot")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(home.router)
app.include_router(chat.router)
app.include_router(files.router)

# Add global error handlers
add_exception_handlers(app)

@app.on_event("startup")
async def startup_event():
    await init_agent()

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
