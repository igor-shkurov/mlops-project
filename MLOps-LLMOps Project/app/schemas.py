from pydantic import BaseModel
from typing import List


# Request Schema
class ChatRequest(BaseModel):
    user_id: str
    prompt: str


# Response Schema
class ChatResponse(BaseModel):
    response: str
    retrieved_chunks: List[str]
