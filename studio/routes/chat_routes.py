# studio/routes/chat_routes.py
from pathlib import Path
from typing import Dict, List

from fastapi import APIRouter, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from chat_client.generic_model_config import MODEL_REGISTRY, get_model_handler

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

router = APIRouter()

DEFAULT_MODEL_ID = next(iter(MODEL_REGISTRY.keys()))

# very simple in‑memory store (move to Redis/DB later)
conversations_store: Dict[str, List[Dict[str, str]]] = {}


# ---------- NEW: /chat entry ----------
@router.get("/", response_class=HTMLResponse)
async def chat_entry(request: Request):
    if not request.session.get("user_id"):
        return templates.TemplateResponse(
            "chat_guest.html",
            {
                "request": request,
                "models": MODEL_REGISTRY,
                "DEFAULT_MODEL_ID": DEFAULT_MODEL_ID,  # FIX: Pass model id
            }
        )
    return RedirectResponse(url=f"/chat/{DEFAULT_MODEL_ID}", status_code=303)


@router.get("/{model_id}", response_class=HTMLResponse)
async def get_chat_view(
    request: Request,
    model_id: str,
    conversation_name: str = Query(default=None),
):
    print(f"Model used: {model_id}")
    # handler = get_model_handler(model_id)
    # if not handler:
    #     return {"error": f"No handler found for model: {model_id}"}
    
    user_id = request.session.get("user_id")
    template = "chat_guest.html" if not user_id else "chat.html"

    conversation = conversations_store.get(conversation_name, []) if (user_id and conversation_name) else []

    return templates.TemplateResponse(
        template,
        {
            "request": request,
            "agent": model_id,
            "DEFAULT_MODEL_ID": DEFAULT_MODEL_ID,  # FIX: Also pass here
            "response": None,
            "user_input": None,
            "conversation_name": conversation_name,
            "conversation": conversation,
            "conversations": conversations_store if user_id else {},
            "models": MODEL_REGISTRY,
        },
    )


@router.post("/{model_id}/send")
async def post_chat_message(
    request: Request,
    model_id: str,
    user_input: str = Form(...),
    conversation_name: str = Form("guest"),
):
    if not conversation_name:
        conversation_name = "guest"

    handler = get_model_handler(model_id)
    ai_response = handler(user_input) if handler else "Error: No valid model handler"

    # Only persist if logged in
    if request.session.get("user_id"):
        if conversation_name not in conversations_store:
            conversations_store[conversation_name] = []
        conversations_store[conversation_name].append({"user": user_input, "ai": ai_response})

    return {"user": user_input, "ai": ai_response}


@router.post("/public/send")
async def guest_chat_send(user_input: str = Form(...)):
    handler = get_model_handler(DEFAULT_MODEL_ID)
    if not handler:
        return {"error": f"No handler found for model Default Model"}
    ai_response = handler(user_input)
    print(f"Model used: {handler}\nInput: {user_input}\nResponse: {ai_response}")
    return {"user": user_input, "ai": ai_response}
