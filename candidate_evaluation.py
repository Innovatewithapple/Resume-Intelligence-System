import json
import asyncio
import time
from pathlib import Path
from state_services import GraphState
from langgraph.graph import StateGraph, START,END
from ApiRequests import candidate_evaluation_details_Node

app_start = time.time()

builder = StateGraph(GraphState)
builder.add_node( "candidate_evaluation",candidate_evaluation_details_Node)
builder.add_edge(START, "candidate_evaluation")
builder.add_edge("candidate_evaluation", END)
evaluation_graph = builder.compile()

async def evaluate_candidate(resume_json: dict,job_description: str,):
    try:
        start = time.perf_counter()
        job_description = job_description
        result = await evaluation_graph.ainvoke(
            {
                "resume_json": resume_json,
                "job_description": job_description,
            }
        )
        if result is None:
            raise ValueError("Candidate evaluation returned None.")
        
        # output_dir = Path("evaluation_output")
        # output_dir.mkdir(exist_ok=True)
        # output_file = (
        #     output_dir
        #     / f"{Path(resume_json_path).stem}_evaluation.json"
        # )

        # with open(output_file, "w", encoding="utf-8") as f:
        #     json.dump(
        #         result["candidate_evaluation"].model_dump(),
        #         f,
        #         indent=4,
        #         ensure_ascii=False,
        #     )
        print(f"Evaluation Time: {time.perf_counter()-start:.2f}s")
        return result["candidate_evaluation"].model_dump()
    except Exception as e:
        print("❌ Server is busy. Please try again later.")
        print(f"Actual Error: {e}")

if __name__ == "__main__":
    with open(
        "output_json/Finance Sample Resume.json","r",encoding="utf-8") as f:
        resume_json = json.load(f)

    asyncio.run(evaluate_candidate(resume_json,jd))