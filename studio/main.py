from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from chat_client.groq_client import chat_with_groq
from chat_client.together_ai import chat_with_together
import uvicorn
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat/{agent}", response_class=HTMLResponse)
async def get_chat_page(request: Request, agent: str):
    return templates.TemplateResponse("chat.html", {"request": request, "agent": agent, "response": None})

@app.post("/chat/{agent}", response_class=HTMLResponse)
async def post_chat(request: Request, agent: str, user_input: str = Form(...)):
    if agent == "groq":
        ai_response = chat_with_groq(user_input)
    elif agent == "together":
        ai_response = chat_with_together(user_input)
    else:
        ai_response = "Unknown agent"
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "agent": agent,
        "user_input": user_input,
        "response": ai_response
    })

if __name__ == "__main__":
    uvicorn.run("studio.main:app", host="127.0.0.1", port=8030, reload=True)
