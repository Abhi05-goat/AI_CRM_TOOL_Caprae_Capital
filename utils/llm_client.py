import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GET_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def call_llm(user_prompt, system="You are a helpful assistant."):
    return client.chat.completions.create(
        model="tokyotech-llm/llama-3.1-swallow-70b-instruct-v0.3",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt}
        ],
        extra_headers={
            "HTTP-Referer": "https://caprae.vc",
            "X-Title": "Caprae Enrichment Tool"
        }
    )
