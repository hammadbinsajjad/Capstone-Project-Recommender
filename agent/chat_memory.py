from llama_index.storage.chat_store.postgres import PostgresChatStore
from llama_index.core.memory import ChatMemoryBuffer

from .config import CHAT_MEMORY_TOKEN_LIMIT, POSTGRES_CHAT_STORE_URI


def load_chat_memory(chat_id):
    chat_store = PostgresChatStore.from_uri(
        uri=POSTGRES_CHAT_STORE_URI,
    )

    return ChatMemoryBuffer.from_defaults(
        token_limit=CHAT_MEMORY_TOKEN_LIMIT,
        chat_store=chat_store,
        chat_store_key=chat_id,
    )
