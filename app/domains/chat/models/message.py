from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class Message(SQLModel, table=True):
    __tablename__ = "messages"  # type: ignore

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    chat_id: str = Field(index=True, foreign_key="chats.id")
    role: str = Field(index=True)  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
