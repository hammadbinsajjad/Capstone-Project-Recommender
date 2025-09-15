import os

from pinecone import ServerlessSpec

# Hugging Face Embeddings Model
EMBEDDINGS_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"


# LLM Configuration
LLM_MODEL = "gemini-2.5-flash-lite"

# Pinecone Index and Vector Store Settings
INDEX_NAME = "capstone-project-recommender-index"
EMBEDDING_DIMENSION = 1024

# Free Indexes in Pinecone are limited to this Spec
INDEX_SPEC = ServerlessSpec(cloud="aws", region="us-east-1")


# Similarity Search Settings
SIMILARITY_TOP_K = 40


# Chat Memory Settings
POSTGRES_CHAT_STORE_URI = os.environ.get("POSTGRES_CHAT_STORE_URI") or ""
CHAT_MEMORY_TOKEN_LIMIT = 3000


# Hugging Face Hub API Token
HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN") or ""
