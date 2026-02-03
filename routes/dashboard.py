from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Setup templates
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "title": "Hospital Dashboard"}
    )

@router.get("/")
async def api_root():
    return {
        "message": "Dashboard API",
        "endpoints": ["/dashboard"]
    }
