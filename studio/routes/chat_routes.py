# studio/routes/chat_routes.py
from pathlib import Path
from typing import Dict, List

from fastapi import APIRouter, Form, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from chat_client.generic_model_config import MODEL_REGISTRY, get_model_handler

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

router = APIRouter()

# very simple in‑memory store (move to Redis/DB later)
conversations_store: Dict[str, List[Dict[str, str]]] = {}


@router.get("/{model_id}", response_class=HTMLResponse)
async def get_chat_view(
    request: Request,
    model_id: str,
    conversation_name: str = Query(default=None),
):
    conversation = conversations_store.get(conversation_name, []) if conversation_name else []

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "agent": model_id,
            "response": None,
            "user_input": None,
            "conversation_name": conversation_name,
            "conversation": conversation,
            "conversations": conversations_store,
            "models": MODEL_REGISTRY,
        },
    )


@router.post("/{model_id}", response_class=HTMLResponse)
async def post_chat_view(
    request: Request,
    model_id: str,
    user_input: str = Form(...),
    conversation_name: str = Form(...),
):
    handler = get_model_handler(model_id)
    ai_response = handler(user_input)

    if conversation_name not in conversations_store:
        conversations_store[conversation_name] = []

    conversations_store[conversation_name].append({"user": user_input, "ai": ai_response})
    conversation = conversations_store[conversation_name]

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "agent": model_id,
            "user_input": user_input,
            "response": ai_response,
            "conversation_name": conversation_name,
            "conversation": conversation,
            "conversations": conversations_store,
            "models": MODEL_REGISTRY,
        },
    )


