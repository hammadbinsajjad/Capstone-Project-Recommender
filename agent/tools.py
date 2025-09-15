from llama_index.core.tools import QueryEngineTool
from llama_index.llms.google_genai import GoogleGenAI

from .config import LLM_MODEL, SIMILARITY_TOP_K


def query_engine_tool(vector_index):
    llm = GoogleGenAI(model=LLM_MODEL)
    query_engine = vector_index.as_query_engine(similarity_top_k=SIMILARITY_TOP_K, llm=llm)

    return QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name="Projects_Data_Query_Tool",
        description=(
            "Fetches past student projects from DataTalkClub Zoomcamp cohorts "
            "(Data Engineering, ML Engineering, MLOps, etc.) to provide examples"
            " and inspiration."
        )
    )
