from pydantic import BaseModel
from typing import TypedDict

class resume_contactInfo_output(BaseModel):
    contact_information:dict

class GraphState(TypedDict):
    path:str
    resume_contact_info:dict
    resume_markdown:str