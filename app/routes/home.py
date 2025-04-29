from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

#return public/index.html
@router.get("/")
def home():
    return HTMLResponse(content=open("app/public/index.html").read(), status_code=200)
