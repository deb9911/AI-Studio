# routes/auth.py
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from studio.services.db import get_session
from studio.services.crud import create_user, authenticate_user
from studio.services.schemas import UserCreate

router = APIRouter(tags=["auth"])

@router.post("/register")
def register(
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form("user"),
    session: Session = Depends(get_session)
):
    create_user(session, email, password, role)
    return RedirectResponse(url="/login", status_code=303)

@router.get("/login")
def login_page():
    # return a Jinja template if you want; for brevity keeping plain
    return {"msg": "POST /login with email & password"}

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = authenticate_user(session, email, password)
    if not user:
        return RedirectResponse(url="/login?error=1", status_code=303)
    request.session["user_id"] = user.id
    return RedirectResponse(url="/", status_code=303)

@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
