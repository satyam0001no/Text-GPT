# backend/app/models.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timedelta
import uuid

Base = declarative_base()

def gen_id():
    return uuid.uuid4().hex

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_id)
    email = Column(String, unique=True, nullable=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Chat(Base):
    __tablename__ = "chats"
    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    title = Column(String, default="New chat")
    messages = relationship("Message", cascade="all, delete-orphan", back_populates="chat")

    @staticmethod
    def make_expiry(hours=2):
        return datetime.utcnow() + timedelta(hours=hours)

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=gen_id)
    chat_id = Column(String, ForeignKey('chats.id'))
    role = Column(String, nullable=False)  # 'user' | 'assistant' | 'system'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    chat = relationship("Chat", back_populates="messages")