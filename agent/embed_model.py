from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from .config import EMBEDDINGS_MODEL_NAME


def load_embed_model():
    return HuggingFaceEmbedding(
        model_name=EMBEDDINGS_MODEL_NAME,
        device="cpu",
    )
