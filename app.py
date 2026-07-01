import asyncio
import time
import json
from langgraph.graph import StateGraph, START,END
from ApiRequests import extract_text_from_pdf_to_markdown, contact_details_Node
from state_services import GraphState

app_start = time.time()

builder = StateGraph(GraphState)

builder.add_node("create_markdown",extract_text_from_pdf_to_markdown)
builder.add_node("contact_details_node",contact_details_Node)

builder.add_edge(START,'create_markdown')
builder.add_edge('create_markdown','contact_details_node')
builder.add_edge('contact_details_node',END)

graph = builder.compile()

async def main():
    input="/Users/himanshuvyas/Documents/testcvs/karan_resume.pdf"
    contact = await graph.ainvoke({"path":input})
    result = contact['resume_contact_info']
    print(json.dumps(result.model_dump(), indent=4)) 

if __name__ == "__main__":
    asyncio.run(main())
    print(f"Total App Time: {time.time()-app_start:.2f}s")