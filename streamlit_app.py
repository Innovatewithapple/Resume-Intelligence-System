import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/analyze-resume"

st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Intelligence")
st.caption("Semantic Resume Parsing & Candidate Evaluation")

st.divider()

resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Job Description",
    height=250,
    placeholder="Paste the complete Job Description here..."
)

# if "processing" not in st.session_state:
#     st.session_state.processing = False

button_placeholder = st.empty()
analyze = button_placeholder.button(
    "Analyze Resume",
    use_container_width=True
)

if analyze:
    # Immediately swap in a disabled button — no session_state needed

    if resume_file is None:
        st.error("Please upload a resume.")
        st.stop()

    job_description = job_description.strip()

    if len(job_description.split()) < 20:
        st.error("Please provide a valid Job Description (minimum 20 words).")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        files = {
            "resume": (
                resume_file.name,
                resume_file.getvalue(),
                "application/pdf"
            )
        }

        data = {
            "job_description": job_description
        }

        response = requests.post(
            API_URL,
            files=files,
            data=data
        )

    if response.status_code != 200:
        st.error("Server Error")
        st.code(response.text)
        st.stop()

    result = response.json()

    evaluation = result.get("candidate_evaluation")

    if evaluation is None:
        st.error(
            "Unable to evaluate this resume. Please provide a more detailed Job Description."
        )
        st.stop()

    st.success(
        f"Completed in {result['processing_time']} seconds"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Overall Match Score",
            f"{evaluation['overall_match_score']}%"
        )

    with col2:
        st.metric(
            "Recommendation",
            evaluation["recommendation"]
        )

    st.subheader("Summary")

    st.write(evaluation["summary"])

    st.divider()

    matched = []
    transferable = []
    missing = []

    for skill in evaluation["skill_analysis"]:

        if skill["status"] == "matched":
            matched.append(skill["skill"])

        elif skill["status"] == "transferable":
            transferable.append(skill["skill"])

        else:
            missing.append(skill["skill"])

    c1, c2, c3 = st.columns(3)

    with c1:

        st.subheader("🟢 Matched")

        for skill in matched:
            st.write(f"• {skill}")

    with c2:

        st.subheader("🟡 Transferable")

        for skill in transferable:
            st.write(f"• {skill}")

    with c3:

        st.subheader("🔴 Missing")

        for skill in missing:
            st.write(f"• {skill}")

    st.divider()

    st.subheader("Strengths")

    if evaluation["strengths"]:

        for item in evaluation["strengths"]:
            st.write(f"• {item}")

    else:
        st.write("-")

    st.subheader("Concerns")

    if evaluation["concerns"]:

        for item in evaluation["concerns"]:
            st.write(f"• {item}")

    else:
        st.write("-")

    st.divider()

    with st.expander("Parsed Resume JSON"):

        st.json(result["parsed_resume"])

    with st.expander("Candidate Evaluation JSON"):

        st.json(result["candidate_evaluation"])