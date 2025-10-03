# backend/app/tasks.py
import threading, time
from datetime import datetime
from .db import SessionLocal
from .models import Chat

def cleanup_expired():
    while True:
        session = SessionLocal()
        try:
            now = datetime.utcnow()
            expired = session.query(Chat).filter(Chat.expires_at <= now).all()
            for c in expired:
                session.delete(c)
            if expired:
                session.commit()
        finally:
            session.close()
        time.sleep(60*5)  # every 5 minutes

def start_cleanup_task():
    t = threading.Thread(target=cleanup_expired, daemon=True)
    t.start()