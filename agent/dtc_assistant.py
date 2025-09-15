import os

from llama_index.core import VectorStoreIndex
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.google_genai import GoogleGenAI

from .chat_memory import load_chat_memory
from .config import LLM_MODEL
from .embed_model import load_embed_model
from .vector_store import load_vector_store
from .tools import query_engine_tool


class DataTalksClubAssistant:
    def __init__(self):
        self.vector_index = VectorStoreIndex.from_vector_store(
            vector_store=load_vector_store(),
            embed_model=load_embed_model(),
        )
        self.tools = [query_engine_tool(self.vector_index)]
        self.llm = GoogleGenAI(model=LLM_MODEL)
        self.load_memory = load_chat_memory

        self.agent = FunctionAgent(
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            max_iterations=3,
            system_prompt=self.__read_system_prompt()
        )

    def __read_system_prompt(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(base_dir, "prompts", "system_prompt.txt")

        with open(prompt_path, "r") as f:
            return f.read()

    async def run(self, user_input, chat_id):
        chat_memory = self.load_memory(chat_id)
        response = await self.agent.run(
            user_input,
            memory=chat_memory
        )

        return response.response.content
