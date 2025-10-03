# backend/app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageCreate(BaseModel):
    role: str
    content: str

class ChatCreate(BaseModel):
    user_email: Optional[str] = None

class ChatRead(BaseModel):
    id: str
    created_at: datetime
    expires_at: datetime
    title: Optional[str]