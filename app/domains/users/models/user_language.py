from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class UserLanguage(SQLModel, table=True):
    __tablename__ = "user_languages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(nullable=False, foreign_key="users.id")
    language: str = Field(nullable=False)
    bytes: int | None = Field(default=None)
    repos_count: int | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
 