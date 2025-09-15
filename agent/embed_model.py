# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.huggingface_api import HuggingFaceInferenceAPIEmbedding

from .config import EMBEDDINGS_MODEL_NAME, HUGGINGFACEHUB_API_TOKEN


def load_embed_model():
    return HuggingFaceInferenceAPIEmbedding(
        model_name=EMBEDDINGS_MODEL_NAME,
        token=HUGGINGFACEHUB_API_TOKEN,
    )
