from tracemalloc import start
import json
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

from pydantic import ValidationError
from Prompts.contactPrompt import contact_info_prompt
from Prompts.experiencePrompt import experience_agent_prompt
from Prompts.educationPrompt import education_details_prompt
from Prompts.remainingDetailsPrompt import remainingDetails_agent_prompt
from Prompts.candidateEvaluationPrompt import candidateevaluation_agent_prompt
from Prompts.tempprompt import tempprompt
from state_services import GraphState, resume_contactInfo_output,resume_work_experienceInfo_output,resume_educationInfo_output,professional_qualificationsInfo_output,candidate_evaluationInfo_output
import time
import pymupdf4llm
from datetime import date

load_dotenv()

nvidia_API_key = os.getenv("NVDIA_API_Key")
base_url='https://integrate.api.nvidia.com/v1/chat/completions'
model='qwen/qwen3-next-80b-a3b-instruct'
backup_Model='meta/llama-4-maverick-17b-128e-instruct'

CONTACT_MAX_TOKENS = 300

EDUCATION_MAX_TOKENS = 600

WORK_EXPERIENCE_MAX_TOKENS = 1500

PROFESSIONAL_QUALIFICATIONS_MAX_TOKENS = 2000

EVALUATION_MAX_TOKENS = 1500

TEMPERATURE=0.0

CONTACT_CHAT_MODEL = ChatNVIDIA(model=model,nvidia_api_key=nvidia_API_key,temperature=TEMPERATURE,max_completion_tokens=CONTACT_MAX_TOKENS,top_p=0.9)
EDUCATION_CHAT_MODEL = ChatNVIDIA(model=model,nvidia_api_key=nvidia_API_key,temperature=TEMPERATURE,max_completion_tokens=EDUCATION_MAX_TOKENS,top_p=0.9)
WORK_EXPERIENCE_CHAT_MODEL = ChatNVIDIA(model=model,nvidia_api_key=nvidia_API_key,temperature=TEMPERATURE,max_completion_tokens=WORK_EXPERIENCE_MAX_TOKENS,top_p=0.9)
REMAINING_DETAILS_CHAT_MODEL = ChatNVIDIA(model=model,nvidia_api_key=nvidia_API_key,temperature=TEMPERATURE,max_completion_tokens=PROFESSIONAL_QUALIFICATIONS_MAX_TOKENS,top_p=0.9)
EVALUATION_CHAT_MODEL = ChatNVIDIA(model=model,nvidia_api_key=nvidia_API_key,temperature=TEMPERATURE,max_completion_tokens=EVALUATION_MAX_TOKENS,top_p=0.9)

parser = StrOutputParser()
today = date.today().isoformat()


#-----------Node---------!

async def extract_text_from_pdf_to_markdown(state:GraphState):
    md = pymupdf4llm.to_markdown(state['path'])
    return {
        "resume_markdown":md
    }

async def contact_details_Node(state:GraphState):
    start = time.perf_counter()
    contact_info_chain=(
        contact_info_prompt
        |CONTACT_CHAT_MODEL.with_structured_output(resume_contactInfo_output)
    )
    try:
        result = await contact_info_chain.ainvoke({'resume_markdown':state['resume_markdown']})
        if result is None:
            raise ValueError("contact_info_chain returns None")
    except Exception as e:
        print(f"Contact Info LLm Agent Failed: {e}")
        return {"resume_contact_info":None}

    print(f'ContactInfo_LLM_Time: {time.perf_counter()-start:.2f}s')
    return {
        "resume_contact_info":result
    }

async def work_experience_details_Node(state:GraphState):
    start = time.perf_counter()
    work_experience_chain=(
        experience_agent_prompt
        |WORK_EXPERIENCE_CHAT_MODEL.with_structured_output(resume_work_experienceInfo_output)
    )
    try:
        result = await work_experience_chain.ainvoke({'resume_markdown':state['resume_markdown'],'current_date':today})
        if result is None:
            raise ValueError("work_experience_chain returns None")
    except Exception as e:
        print(f"Work experience Agent Failed: {e}")
        return {"resume_work_experience_info":None}
    
    print(f'work_experience_Info_LLM_Time: {time.perf_counter()-start:.2f}s')
    return {
        "resume_work_experience_info":result
    }

async def education_details_Node(state:GraphState):
    start = time.perf_counter()
    education_chain=(
        education_details_prompt
        |EDUCATION_CHAT_MODEL.with_structured_output(resume_educationInfo_output)
    )
    try:
        result = await education_chain.ainvoke({"resume_markdown":state['resume_markdown']})
        if result is None:
            raise ValueError("education_chain returns None")
    except Exception as e:
        print(f"Education agent Failed: {e}")
        return {"resume_education_info":None}
    
    print(f"education_details_Info_LLm_Time: {time.perf_counter()-start:.2f}s")
    return {
        "resume_education_info": result
    }

async def remaining_details_Node(state:GraphState):
    start = time.perf_counter()
    remaining_chain=(
        remainingDetails_agent_prompt
        |REMAINING_DETAILS_CHAT_MODEL.with_structured_output(professional_qualificationsInfo_output)
    )
    try:
        result = await remaining_chain.ainvoke({"resume_markdown":state['resume_markdown']})
        if result is None:
            raise ValueError("remaining_chain returns None")
    except Exception as e:
        print(f"Remaining agent failed: {e}")
        return {"resume_remaining_info":None}
    
    print(f"remaining_details_Info_LLm_Time: {time.perf_counter()-start:.2f}s")
    return {
        "resume_remaining_info": result
    }

async def candidate_evaluation_details_Node(state:GraphState):
    start = time.perf_counter()
    evaluation_chain=(
        candidateevaluation_agent_prompt
        |EVALUATION_CHAT_MODEL
    )
    try:
        result = await evaluation_chain.ainvoke(
            {
                "resume_json": state["resume_json"],
                "job_description": state["job_description"],
            }
        )
        with open("evaluation_raw.txt", "w", encoding="utf-8") as f:
            f.write(result.content)

        print(result.content)
        raw = json.loads(result.content)
        validated = candidate_evaluationInfo_output.model_validate(raw)

    except ValidationError as e:
        print("\n========= PYDANTIC VALIDATION ERROR =========")
        print(e)
        print("============================================\n")
        return {"candidate_evaluation": None}

    except Exception as e:

        import traceback

        print("\n========= GENERAL ERROR =========")
        traceback.print_exc()
        print("=================================\n")

        return {"candidate_evaluation": None}

    print(f"candidate_evaluation_Info_LLM_Time: {time.perf_counter()-start:.2f}s")

    return {
        "candidate_evaluation": validated
    }