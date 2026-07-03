import asyncio
import time
import json
from langgraph.graph import StateGraph, START,END
from ApiRequests import extract_text_from_pdf_to_markdown, contact_details_Node, work_experience_details_Node, education_details_Node, remaining_details_Node
from state_services import GraphState
from pathlib import Path

app_start = time.time()

builder = StateGraph(GraphState)

builder.add_node("create_markdown",extract_text_from_pdf_to_markdown)
builder.add_node("contact_details_node",contact_details_Node)
builder.add_node("work_experience_details_node",work_experience_details_Node)
builder.add_node("education_details_node",education_details_Node)
builder.add_node("remaining_details_Node",remaining_details_Node)

builder.add_edge(START,'create_markdown')
builder.add_edge('create_markdown','contact_details_node')
builder.add_edge('contact_details_node',END)

builder.add_edge('create_markdown','work_experience_details_node')
builder.add_edge('work_experience_details_node',END)

builder.add_edge('create_markdown','education_details_node')
builder.add_edge('education_details_node',END)

builder.add_edge('create_markdown','remaining_details_Node')
builder.add_edge('remaining_details_Node',END)

graph = builder.compile()

# async def process_resume(pdf: Path):
#     resume_start = time.perf_counter()
#     try:
#         print(f"🚀 Started : {pdf.name}")

#         result = await graph.ainvoke({"path": str(pdf)})

#         resume = ResumeParserOutput(
#             contact_information=result["resume_contact_info"],
#             work_experience=result["resume_work_experience_info"],
#             education=result["resume_education_info"],
#             professional_qualifications=result["resume_remaining_info"],
#         )

#         output_dir = Path("output_json")
#         output_dir.mkdir(exist_ok=True)

#         output_file = output_dir / f"{pdf.stem}.json"

#         output_file.write_text(
#             resume.model_dump_json(indent=4),
#             encoding="utf-8"
#         )
#         elapsed = time.perf_counter() - resume_start
#         print(f"✅ Finished : {pdf.name} ({elapsed:.2f}s)")

#     except Exception as e:
#         elapsed = time.perf_counter() - resume_start
#         print(f"❌ Failed : {pdf.name} ({elapsed:.2f}s)")
#         print(e)


#     resume_dir = Path("/Users/himanshuvyas/Desktop/tempvc/testresumes/parallel")

# async def main():
#     batch_start = time.perf_counter()
#     resume_dir = Path("/Users/himanshuvyas/Desktop/tempvc/testresumes/parallel")
#     tasks = [
#         process_resume(pdf)
#         for pdf in resume_dir.glob("*.pdf")
#     ]
#     await asyncio.gather(*tasks)
#     print(
#         f"\n🎉 All resumes completed in "
#         f"{time.perf_counter()-batch_start:.2f}s"
#     )
async def main():
    try:
        resume_path = "/Users/himanshuvyas/Desktop/tempvc/testresumes/karan_resume.pdf"
        result = await graph.ainvoke({"path": resume_path})
        output_dir = Path("output_json")
        output_dir.mkdir(exist_ok=True)
        final_output = {
            "contact_information": result["resume_contact_info"].model_dump(),
            "work_experience": result["resume_work_experience_info"].model_dump(),
            "education": result["resume_education_info"].model_dump(),
            "professional_qualifications": result["resume_remaining_info"].model_dump()
        }

        output_file = output_dir / Path(resume_path).with_suffix(".json").name

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=4, ensure_ascii=False)

        print("✅ JSON Saved")

    except Exception as e:
        print("❌ Server is busy. Please try again later.")
        print(f"Actual Error: {e}")    

if __name__ == "__main__":
    asyncio.run(main())
    print(f"Total App Time: {time.time()-app_start:.2f}s")