import os

from pinecone import ServerlessSpec


IS_GOOGLE_COLAB = os.environ.get("IS_GOOGLE_COLAB") == "true"


# Hugging Face Embeddings Model
EMBEDDINGS_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"

# Readme Files Directory (made by readme_downloader)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, "ingestion", "data", "readme_files")


# Pinecone Index and Vector Store Settings
INDEX_NAME = "capstone-project-recommender-index"
EMBEDDING_DIMENSION = 1024

# Free Indexes in Pinecone are limited to this Spec
INDEX_SPEC = ServerlessSpec(cloud="aws", region="us-east-1")
