from pydantic import BaseModel

class Chat(BaseModel):
    name: str

class Message(BaseModel):
    chat_id: str
    message: str