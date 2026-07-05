from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path
import shutil
import time

from app import parse_resume
from candidate_evaluation import evaluate_candidate

app = FastAPI(
    title="Resume Intelligence API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze-resume")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    start = time.perf_counter()

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    resume_path = upload_dir / resume.filename

    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    parsed_resume = await parse_resume(str(resume_path))

    evaluation = await evaluate_candidate(
        parsed_resume,
        job_description
    )

    return {
        "success": True,
        "processing_time": round(
            time.perf_counter() - start,
            2,
        ),
        "parsed_resume": parsed_resume,
        "candidate_evaluation": evaluation,
    }