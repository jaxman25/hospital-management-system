from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

router = APIRouter()

try:
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if JINJA2_AVAILABLE:
        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request, "title": "Dashboard"}
        )
    else:
        return HTMLResponse("""
        <html>
            <body>
                <h1>Hospital Management System</h1>
                <p>Jinja2 templates not available. Please install jinja2.</p>
                <p>Run: pip install jinja2</p>
            </body>
        </html>
        """)

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if JINJA2_AVAILABLE:
        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request, "title": "Dashboard"}
        )
    else:
        return JSONResponse({
            "message": "Dashboard endpoint",
            "note": "Jinja2 not installed. Install with: pip install jinja2"
        })
