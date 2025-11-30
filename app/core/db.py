import os
from sqlmodel import Session, create_engine
from dotenv import load_dotenv

load_dotenv()

# Creates the PostgreSQL connection string with SSL enabled
DATABASE_URL = (
    f"postgresql://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}"
    f"@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DATABASE')}?sslmode=require"
)

# Creates the SQLModel engine
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    return Session(engine)
