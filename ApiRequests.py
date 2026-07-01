from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
from prompts import contact_info_prompt
from state_services import GraphState, resume_contactInfo_output
import time
import asyncio
import pymupdf4llm

load_dotenv()

nvidia_API_key = os.getenv("NVDIA_API_Key")
base_url='https://integrate.api.nvidia.com/v1/chat/completions'
model='meta/llama-4-maverick-17b-128e-instruct'
max_tokens = 500
temperature=0.0
chat_model = ChatNVIDIA(model=model,nvidia_api_key=nvidia_API_key,temperature=temperature,max_completion_tokens=max_tokens,top_p=0.9)
parser = StrOutputParser()

async def extract_text_from_pdf_to_markdown(state:GraphState):
    md = pymupdf4llm.to_markdown(state['path'])
    return {
        "resume_markdown":md
    }

async def contact_details_Node(state:GraphState):
    start = time.perf_counter()
    contact_info_chain=(
        contact_info_prompt
        |chat_model.with_structured_output(resume_contactInfo_output)
    )
    result = await contact_info_chain.ainvoke({'resume_markdown':state['resume_markdown']})
    # print(f'\n\n promptResult: {result}')
    print(f'ContactInfo_LLM_Time: {time.perf_counter()-start:.2f}s')
    return {
        "resume_contact_info":result
    }