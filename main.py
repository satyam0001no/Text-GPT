# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from . import db, models, schemas, llm_adapter, image_adapter
from sqlalchemy.orm import Session
from datetime import datetime
from .crud import create_chat, add_message, get_chat, list_user_chats
from .tasks import start_cleanup_task

app = FastAPI(title="Text GPT (self-hosted)")

@app.on_event("startup")
def startup():
    db.init_db()
    # start background cleanup or rely on external cron
    start_cleanup_task()

@app.post("/chat", response_model=schemas.ChatRead)
def create_new_chat(payload: schemas.ChatCreate, session: Session = Depends(db.SessionLocal)):
    chat = create_chat(session, user_email=payload.user_email)
    return chat

@app.post("/chat/{chat_id}/message")
def send_message(chat_id: str, msg: schemas.MessageCreate, session: Session = Depends(db.SessionLocal)):
    chat = get_chat(session, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    # store user message
    add_message(session, chat_id, msg.role, msg.content)
    # build prompt from recent messages (simple)
    prompt = build_prompt_from_chat(chat)
    reply = llm_adapter.generate_reply(prompt)
    add_message(session, chat_id, "assistant", reply)
    return {"reply": reply}

@app.post("/image")
def gen_image(prompt: dict):
    data = image_adapter.generate_image(prompt["prompt"])
    return data