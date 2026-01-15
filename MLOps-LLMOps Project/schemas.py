from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    user_id: str
    prompt: str


class ChatResponse(BaseModel):
    response: str
    retrieved_chunks: List[str]
