import asyncio
import time
import json
from langgraph.graph import StateGraph, START,END
from ApiRequests import extract_text_from_pdf_to_markdown, contact_details_Node, work_experience_details_Node, education_details_Node, remaining_details_Node
from state_services import GraphState,ResumeParserOutput
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

async def main():
    contact = await graph.ainvoke({"path":"/Users/himanshuvyas/Desktop/tempvc/testresumes/White Simple Student CV Resume.pdf"})
    result = contact
    final_output = ResumeParserOutput(
        contact_information=result["resume_contact_info"],
        work_experience=result["resume_work_experience_info"],
        education=result["resume_education_info"],
        professional_qualifications=result["resume_remaining_info"]
    )
    if result is None:
        print(f"❌ Failed")
    print(final_output.model_dump_json(indent=4))
    # resume_dir = Path("/Users/himanshuvyas/Desktop/tempvc/testresumes")
    # for pdf in resume_dir.glob("*.pdf"):
    #     print(f"\n\nProcessing: {pdf.name}")
    #     contact = await graph.ainvoke({"path":str(pdf)})
    #     result = contact['resume_education_info']
        
    #     if result is None:
    #         print(f"❌ Failed: {pdf.name}")
    #         continue
    #     print(json.dumps(result.model_dump(), indent=4)) 

if __name__ == "__main__":
    asyncio.run(main())
    print(f"Total App Time: {time.time()-app_start:.2f}s")