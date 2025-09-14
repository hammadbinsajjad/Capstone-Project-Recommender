import os

from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

from .config import EMBEDDING_DIMENSION, INDEX_NAME, INDEX_SPEC


def load_vector_store():
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

    if not pc.has_index(INDEX_NAME):
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=INDEX_SPEC
        )

    return PineconeVectorStore(pc.Index(INDEX_NAME))
