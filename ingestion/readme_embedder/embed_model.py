from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.huggingface_openvino import OpenVINOEmbedding

from config import EMBEDDINGS_MODEL_NAME, IS_GOOGLE_COLAB


def load_embed_model():
    if IS_GOOGLE_COLAB:
        return HuggingFaceEmbedding(model_name=EMBEDDINGS_MODEL_NAME, device="gpu")

    return OpenVINOEmbedding(model_id_or_path=EMBEDDINGS_MODEL_NAME, device="auto")
