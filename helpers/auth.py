from fastapi import HTTPException, Header
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def authenticate(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")