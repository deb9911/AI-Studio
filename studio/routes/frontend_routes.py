from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="studio/templates")

# ---------- Home Page ----------
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    # If user is logged in, redirect to /chat
    if request.session.get("user_id"):
        return RedirectResponse(url="/chat", status_code=302)
    return templates.TemplateResponse("home.html", {"request": request})

# ---------- Chat Page ----------
@router.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    user_id = request.session.get("user_id")
    role = request.session.get("role", "guest")

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "user_id": user_id,
        "role": role
    })

# ---------- Optional: Profile Page ----------
@router.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user_id": user_id,
        "role": request.session.get("role")
    })
