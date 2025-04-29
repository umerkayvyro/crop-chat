from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

def add_exception_handlers(app: FastAPI):
    """Registers global exception handlers for the FastAPI app."""
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
    
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred.", "details": str(exc)}
        )
