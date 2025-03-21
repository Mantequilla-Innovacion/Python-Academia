import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL") ## https://api.openai.com/v1 -> Custom server
)