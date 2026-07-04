from langchain_core.prompts import ChatPromptTemplate

tempprompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        ROLE

        You are an evaluator.

        Return:

        overall_match = 90

        recommendation = Strong Match


        Resume_Json:
        <{resume_json}>

        Job Description:
        <{job_description}>
        """
    )
])