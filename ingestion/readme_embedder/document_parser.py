from llama_index.core.node_parser import MarkdownNodeParser


def load_document_parser():
    return MarkdownNodeParser(chunk_size=512)
