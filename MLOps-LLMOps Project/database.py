"""
Database module for LLMOps project.
Provides:
- SQLAlchemy engine and session setup
- PromptResponse table for logging user prompts and model responses
- Utility functions to initialize the DB and save entries
"""

from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file
DATABASE_URL = "sqlite:///llmops.db"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Table for storing user prompts and LLM responses
class PromptResponse(Base):
    __tablename__ = "prompt_responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    prompt = Column(Text)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# Initialize the database and tables
def init_db():
    Base.metadata.create_all(bind=engine)


# Helper function to save a prompt and response
def save_prompt_response(user_id: str, prompt: str, response: str):
    db = SessionLocal()
    db_entry = PromptResponse(user_id=user_id, prompt=prompt, response=response)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    db.close()

    return db_entry
