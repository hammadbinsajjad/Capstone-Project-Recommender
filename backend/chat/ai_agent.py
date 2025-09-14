from google import genai
from llama_index.storage.chat_store.postgres import PostgresChatStore

from .constants import GEMINI_MODEL,  POSTGRES_CHAT_STORE_URI


class BaseAIAgent:
    def __init__(self):
        raise NotImplementedError

    def generate_response(self, user_query, chat_id):
        raise NotImplementedError

    def chat_messages(self, chat_id):
        raise NotImplementedError


class GeminiTestingAgent(BaseAIAgent):
    def __init__(self):
        self.client = genai.Client()
        self.messages = []

    def generate_response(self, user_query, chat_id):
        prompt = (
            "You are a helpful AI assistant for a project recommendation system. "
            f"Answer the following query:\n{user_query}\n"
            "Provide a concise and informative response."
        )

        self.add_message("user", user_query)

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        self.add_message("assistant", response.text)

        return response.text

    def chat_messages(self, chat_id):
        return self.messages

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})


class AIAgent(BaseAIAgent):
    ...
    # Need to implement this once the AI Agent is developed

    def chat_messages(self, chat_id):
        chat_store = PostgresChatStore.from_uri(POSTGRES_CHAT_STORE_URI)
        return [{"role": message.role, "content": message.content}
                for message in chat_store.get_messages(chat_id)]
