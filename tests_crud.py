# backend/app/tests/test_crud.py
from app import db, models
from app.crud import create_chat, add_message, get_chat
from datetime import datetime, timedelta

def test_create_chat(tmp_path, monkeypatch):
    # use sqlite in-memory by overriding DB URL
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    db.init_db()
    session = db.SessionLocal()
    chat = create_chat(session, user_email="a@b.com")
    assert chat.id is not None
    assert chat.expires_at > datetime.utcnow()