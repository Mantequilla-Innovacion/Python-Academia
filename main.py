from fastapi import FastAPI, HTTPException, Depends, Header
from helpers.open_ai_chat import  open_ai_request
from utils.firestore import chats_collection
from models.models import Message, Chat

app = FastAPI(
    description="Made by Mantequilla, feel free to let me know problems "
)

@app.post("/chat", tags=["Chat"])
def create_chat(chat: Chat):
    doc_ref = chats_collection.document()
    doc_ref.set({"id": doc_ref.id, "name": chat.name, "history": []})
    return {"id": doc_ref.id, "name": chat.name, "history": []}

@app.get("/chats", tags=["Chat"])
def get_all_chats():
    docs = chats_collection.stream()
    chat_list = []

    for doc in docs:
        data = doc.to_dict()
        chat_list.append(data)

    return {"chats": chat_list}

@app.delete("/chat/{chat_id}", tags=["Chat"])
def delete_chat(chat_id: str):
    doc = chats_collection.document(chat_id)
    if not doc.get().exists:
        raise HTTPException(status_code=404, detail="chat not found")
    doc.delete()
    return {"message": "Chat deleted Successfully"}

@app.put("/chat/{chat_id}", tags=["Chat"])
def update_chat(chat_id: str, chat: Chat):
    doc = chats_collection.document(chat_id)
    if not doc.get().exists:
        raise HTTPException(status_code=404, detail="chat not found")
    doc.update({"name": chat.name})
    return {"message": "Chat name updated Successfully"}

@app.get("/chat/{chat_id}", tags=["Chat"], description="Methos for Chats")
def get_chat(chat_id: str):
    doc = chats_collection.document(chat_id)
    chat = doc.get()
    if not chat.exists:
        raise HTTPException(status_code=404, detail="chat not found")
    return chat.to_dict()


@app.post("/{chat_id}", tags=["Bot"])
def chat_with_bot(chat_id: str, message_content: Message):
    response = open_ai_request(chat_id, message_content.message)
    if response is None:
        raise HTTPException(status_code=404, detail="chat not found")
    return {"response": response}