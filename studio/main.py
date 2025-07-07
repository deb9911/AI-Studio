from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi import Query
import uvicorn
from docx import Document
import uuid
import os
from typing import Dict, List

from chat_client.generic_model_config import MODEL_REGISTRY, get_model_handler

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

conversations_store: Dict[str, List[Dict[str, str]]] = {}  # {conversation_name: [ {"user":..., "ai":...}, ... ]}


@app.post("/generate-doc")
async def generate_doc(request: Request, content: str = Form(...)):
    doc = Document()
    doc.add_heading("AI Response", level=1)
    doc.add_paragraph(content)

    filename = f"response_{uuid.uuid4().hex[:8]}.docx"
    filepath = os.path.join(BASE_DIR, "generated", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    doc.save(filepath)

    return FileResponse(path=filepath, filename=filename, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "models": MODEL_REGISTRY
    })


@app.get("/chat/{model_id}", response_class=HTMLResponse)
async def get_chat_view(request: Request, model_id: str, conversation_name: str = Query(default=None)):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "agent": model_id,
        "response": None,
        "user_input": None,
        "conversation_name": conversation_name,
        "conversations": conversations_store,
        "models": MODEL_REGISTRY
    })


@app.post("/chat/{model_id}", response_class=HTMLResponse)
async def post_chat_view(
    request: Request,
    model_id: str,
    user_input: str = Form(...),
    conversation_name: str = Form(...)
):
    handler = get_model_handler(model_id)
    ai_response = handler(user_input)

    # Save to conversation store
    if conversation_name not in conversations_store:
        conversations_store[conversation_name] = []

    conversations_store[conversation_name].append({
        "user": user_input,
        "ai": ai_response
    })

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "agent": model_id,
        "user_input": user_input,
        "response": ai_response,
        "conversation_name": conversation_name,
        "conversations": conversations_store,
        "models": MODEL_REGISTRY
    })


if __name__ == "__main__":
    uvicorn.run("studio.main:app", host="127.0.0.1", port=8030, reload=True)
