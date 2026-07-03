import asyncio
import time
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import os

load_dotenv()

chat_model = ChatNVIDIA(
    model="mistralai/mixtral-8x7b-instruct-v0.1",
    api_key=os.getenv("NVDIA_API_Key")   # or load from .env like you normally do
)

async def main():
    start = time.perf_counter()

    result = await chat_model.ainvoke("Reply with only the word Hello.")

    print(result.content)
    print(f"Time: {time.perf_counter() - start:.2f} seconds")

asyncio.run(main())