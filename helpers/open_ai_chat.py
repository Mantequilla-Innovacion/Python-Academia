import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.firestore import chats_collection

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL") ## https://api.openai.com/v1 -> Custom server
)


def open_ai_request(chat_id: str, user_message) -> dict:
    chat = chats_collection.document(chat_id)
    doc = chat.get()
    if not doc.exists:
        return {"error": f"ERROR THERE IS NOT CHATBOT WITH THIS ID({chat_id})"}
    doc_content = doc.to_dict()
    history = doc_content.get("history", [])
    history.append({"role": "user", "content": user_message})
    open_ai_request = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that can answer questions and help with tasks." ## Prompt Engineering
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.5, # Que tan creativo es el modelo
        max_tokens=600, ## Cantidad de palabras/silabas que se van a generar por el model 
        top_p=1, ## El modelo va a tener en cuenta el 100% de las palabras/silabas que se le dan
        n=3, ## Cantidad de respuestas que se van a generar
        user="yahir.ponce@softtek.com" # Para poder hacer un seguimiento de las respuestas
    )

    open_ai_response = open_ai_request.choices[0].message.content
    history.append({"role": "assistant", "content": open_ai_response})
    chat.update({"history": history})
    return  open_ai_response