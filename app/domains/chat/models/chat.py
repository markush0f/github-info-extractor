from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime


class Chat(SQLModel, table=True):
    __tablename__ = "chats"  # type: ignore

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    user_id: str = Field(index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
