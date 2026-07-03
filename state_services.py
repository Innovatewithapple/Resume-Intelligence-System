from numpy import double
from pydantic import BaseModel
from typing import TypedDict

class Security(BaseModel):
    prompt_injection_detected: bool
    reason: str

class Datesstr(BaseModel):
    start:str
    end:str

#-------Contact Info---------!

class contact_info(BaseModel):
    name:str | None
    phone_numbers:list[str] | None
    email_addresses:list[str] | None
    locations:list[str] | None
    websites:list[str] | None
    github:str | None
    linkedin:str | None
    addresses:list[str] | None
    portfolio:list[str] | None

class resume_contactInfo_output(contact_info):
    confidence_score:float | None
    security:Security | None


#-------Work Experience--------!

class work_info(BaseModel):
    company:str | None
    employment_title:str | None
    dates:Datesstr | None
    total_years:float | None
    location:str | None
    details:list[str] | None
    links:list[str] | None

class resume_work_experienceInfo_output(BaseModel):
    work_experience:list[work_info] | None
    total_experience:float | None
    confidence_score:float | None
    security:Security | None


#-------Education Info------!

class education_info(BaseModel):
    education_title:str | None
    institution:str | None
    dates:Datesstr | None
    academic_result:str
    location:str | None

class resume_educationInfo_output(BaseModel):
    education:list[education_info]
    confidence_score:float | None
    security:Security | None


#--------Remaining Info------!

class Achievement(BaseModel):
    type:str | None
    title:str | None
    details: list[str] | None

class Project(BaseModel):
    name: str | None
    description: str | None
    technologies: list[str] | None
    links: list[str] | None   

class professional_info(BaseModel):
    technical_skills:list[str]
    soft_skills:list[str]
    expertise:list[str]
    languages:list[str]
    certifications:list[str]
    licenses:list[str]
    professional_affiliations:list[str]
    awards:list[str]
    achievements:list[Achievement] | None
    projects: list[Project] | None
    training:list[str]


class professional_qualificationsInfo_output(BaseModel):
    professional_qualifications:professional_info
    confidence_score:float | None
    security:Security | None


class GraphState(TypedDict):
    path:str
    resume_contact_info:dict
    resume_work_experience_info:dict
    resume_education_info:dict
    resume_remaining_info:dict
    resume_info:dict
    resume_markdown:str