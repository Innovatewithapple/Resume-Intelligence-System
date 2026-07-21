---
title: Resume Intelligence Analyser
emoji: 📄
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# 📄 Resume Intelligence System

> **A production-ready multi-agent AI platform that uses parallel LangGraph workflows to parse resumes, generate structured candidate profiles, and semantically evaluate them against job descriptions.**

This project demonstrates an end-to-end AI recruitment workflow built with **LangGraph**, **FastAPI**, **Streamlit**, and **Docker**. Instead of analyzing an entire resume with a single LLM prompt, the system distributes the workload across multiple specialized agents running in parallel, combines their outputs into a structured Resume JSON, and semantically compares it against a Job Description to generate a comprehensive hiring report.

---

## 🚀 Live Demo

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow)](https://huggingface.co/spaces/Innovatewithapple/Resume-Intelligence-Analyser)

[![GitHub](https://img.shields.io/badge/GitHub-Source%20Code-181717?logo=github)](https://github.com/Innovatewithapple/Resume-Intelligence-System)

---

# 🎯 Project Highlights

- 📄 Intelligent PDF resume parsing
- ⚡ Parallel multi-agent workflow using LangGraph
- 🤖 Four specialized AI extraction agents
- 📋 Structured Resume JSON generation
- 🎯 Semantic Resume ↔ Job Description matching
- 📊 AI-generated compatibility score
- ✅ Required skills matching
- ❌ Missing skills identification
- ⭐ Optional qualification detection
- 💼 Experience comparison
- 💡 Personalized resume improvement recommendations
- 🌐 FastAPI backend
- 💻 Streamlit frontend
- 🐳 Dockerized deployment
- ☁️ Deployed on Hugging Face Spaces

---

# 📌 Project Overview

Instead of relying on a single prompt to understand an entire resume, this project orchestrates a **parallel LangGraph workflow** to analyze different sections independently.

The uploaded PDF is first converted into Markdown. Four specialized extraction agents then process **Contact Details**, **Work Experience**, **Education**, and **Remaining Resume Details** simultaneously. Their outputs are merged into a structured Resume JSON, which is finally compared against the supplied Job Description using semantic AI techniques to generate a complete candidate evaluation report.

This architecture improves modularity, makes the pipeline easier to extend, and demonstrates practical multi-agent orchestration for real-world recruitment workflows.

---

# 🏗️ System Architecture

```text
                          User
                           │
                           ▼
                 Streamlit Frontend
                           │
                           ▼
          Resume PDF + Job Description
                           │
                           ▼
                  FastAPI Backend
                           │
                           ▼
            Resume → Markdown Conversion
                           │
                           ▼
                 LangGraph Workflow
                           │
        ┌──────────┬──────────┬──────────┬──────────┐
        │          │          │          │
        ▼          ▼          ▼          ▼
 Contact Details  Work Exp   Education  Remaining
      Agent        Agent       Agent      Agent
        │          │          │          │
        └──────────┴──────────┴──────────┘
                           │
                           ▼
             Resume JSON Generation Node
                           │
                           ▼
          Resume ↔ Job Description Matcher
                           │
                           ▼
         AI Candidate Evaluation Report
```

---

# ⚙️ Technology Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | LangGraph |
| LLM Framework | LangChain |
| Backend | FastAPI |
| Frontend | Streamlit |
| API Documentation | Swagger / OpenAPI |
| Deployment | Hugging Face Spaces |
| Containerization | Docker |
| Language | Python |

---

# ✨ Features

- Resume PDF upload
- Automatic Markdown conversion
- Parallel AI resume parsing
- Contact information extraction
- Work experience extraction
- Education extraction
- Additional details extraction
- Structured Resume JSON generation
- Semantic Resume ↔ Job Description comparison
- Overall candidate compatibility score
- Required skills analysis
- Missing skills detection
- Optional/preferred qualification analysis
- Experience evaluation
- Resume improvement recommendations
- Interactive Streamlit interface
- REST API support
- Docker deployment

---

# 📊 AI Evaluation Report

For every uploaded resume, the system generates a comprehensive hiring report including:

- 🎯 Overall Resume Match Score
- 📊 Candidate Compatibility Percentage
- ✅ Matched Skills
- ❌ Missing Required Skills
- ⭐ Optional / Preferred Qualifications
- 💼 Work Experience Analysis
- 🎓 Education Analysis
- 📄 Contact Information Extraction
- 📋 Structured Resume JSON
- 💡 Personalized Resume Improvement Suggestions
- 📝 Detailed reasoning behind every evaluation

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/Innovatewithapple/Resume-Intelligence-System.git

cd Resume-Intelligence-System
```

## Build Docker Image

```bash
docker build -t resume-intelligence .
```

## Run the Application

```bash
docker run \
    -p 7860:7860 \
    -p 8000:8000 \
    resume-intelligence
```

Open:

- 🌐 Streamlit UI → http://localhost:7860
- 📖 FastAPI Documentation → http://localhost:8000/docs
- ⚙️ FastAPI API → http://localhost:8000

---

# 📂 Repository Structure

```text
.
├── agents/
├── api/
├── app/
├── graph/
├── streamlit/
├── Dockerfile
├── start.sh
├── requirements.txt
└── README.md
```

---

# 💡 Example Use Cases

- Resume screening
- Candidate evaluation
- Resume optimization
- Recruitment assistance
- HR automation
- Skill gap analysis
- Job application review

---

# 🔮 Future Improvements

- 🧩 Chrome Extension for analyzing resumes directly on LinkedIn, Indeed, Naukri, and other job portals
- 📊 Interactive recruiter analytics dashboard
- 📁 Batch resume evaluation
- 🌍 Multi-language resume analysis
- 📄 Support for DOCX and additional resume formats
- 📈 Candidate comparison across multiple resumes
- 🤖 Additional specialized AI agents
- 🔗 ATS (Applicant Tracking System) integration
