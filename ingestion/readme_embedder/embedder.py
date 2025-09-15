from llama_index.core import VectorStoreIndex, StorageContext

from config import EMBEDDINGS_MODEL_NAME, INDEX_NAME
from document_parser import load_document_parser
from documents import load_documents
from vector_store import load_vector_store
from embed_model import load_embed_model

storage_context = StorageContext.from_defaults(vector_store=load_vector_store())

index = VectorStoreIndex.from_documents(
    load_documents(),
    storage_context=storage_context,
    embed_model=load_embed_model(),
    transformations=[load_document_parser()],
    show_progress=True,
)

print(f"✅ Embeddings saved to Pinecone Index {INDEX_NAME} using model {EMBEDDINGS_MODEL_NAME}")
