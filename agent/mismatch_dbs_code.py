pip install pinecone google-generativeai sqlalchemy psycopg2-binary openai



"""
Fixed agent scaffold using Pinecone (new SDK) + Gemini + Postgres.
- Embeddings: OpenAI embeddings (requires OPENAI_API_KEY) by default.
- If you don't have OpenAI, see the comments below to replace with your own embedder.
"""

import os
import time
from datetime import datetime
from typing import List, Dict, Any

# -------------------------
# Credentials - set these (or set via env variables for safety)
# -------------------------
PINECONE_API_KEY = "pcsk_gKMU8_ASfcTRRf1hEjqMekgV3udwEW6Y8NbcPZAFYE4FjHxvFbUR8vDGQmGvgdPoAxfJA"
PINECONE_INDEX_NAME = "capstone-project-recommender-index"

GEMINI_API_KEY = "AIzaSyDoUsHjqXHfxq69RVYVrVbs7DJpwRIDisk"

POSTGRES_CONN_STR = (
    "postgresql://neondb_owner:npg_VG0B6Ydyetlx@ep-falling-dream-adwbl6j1-pooler.c-2.us-east-1.aws.neon.tech"
    "/neondb?sslmode=require&channel_binding=require"
)

# Optional: OpenAI API key for embeddings. If you don't want to use OpenAI embeddings,
# replace embed_text(...) with another provider implementation.
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)  # set this in your env if available

# -------------------------
# Install / import Pinecone (new SDK)
# -------------------------
from pinecone import Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Ensure index exists and get an Index handle
all_indexes = pc.list_indexes().names()
if PINECONE_INDEX_NAME not in all_indexes:
    raise RuntimeError(f"Pinecone index '{PINECONE_INDEX_NAME}' not found. Available: {all_indexes}")

index = pc.Index(PINECONE_INDEX_NAME)

# -------------------------
# Helper: inspect index to find dimension
# -------------------------
def get_index_dimension(idx) -> int:
    # best-effort: try describe_index_stats() or describe_index()
    try:
        stats = idx.describe_index_stats()
        # stats may contain 'dimension' somewhere or you may need to get from index.describe_index()
        # The new SDK sometimes needs describe_index()
    except Exception:
        stats = None

    try:
        desc = idx.describe_index()
    except Exception:
        desc = None

    # Try to read dimension from desc
    if desc and isinstance(desc, dict):
        # path depends on SDK; try a few possibilities
        for key in ["dimension", "metadata", "index_config"]:
            if key in desc:
                if isinstance(desc[key], int):
                    return desc[key]
                # else continue
    # fallback: ask user to provide dimension or default to 1536
    print("WARNING: Couldn't automatically detect index dimension. Defaulting to 1536.")
    return 1536

INDEX_DIMENSION = get_index_dimension(index)
print(f"Using index dimension = {INDEX_DIMENSION}")

# -------------------------
# Embedding function (OpenAI default)
# -------------------------
# If you want to use a different embedder, replace the body of embed_text()
import openai
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def embed_text(text: str) -> List[float]:
    """
    Returns an embedding vector of length INDEX_DIMENSION.
    Default: uses OpenAI text-embedding-3-small (1536 dims).
    Replace with your own embedding provider if you cannot use OpenAI.
    """
    if OPENAI_API_KEY:
        # use OpenAI's text-embedding-3-small (1536) or text-embedding-3-large (3072)
        # adjust model name if you prefer
        model_name = "text-embedding-3-small"
        resp = openai.Embedding.create(input=text, model=model_name)
        vec = resp["data"][0]["embedding"]
        if len(vec) != INDEX_DIMENSION:
            print(f"Warning: embedding length {len(vec)} != index dimension {INDEX_DIMENSION}")
        return vec
    else:
        # Fallback: deterministic dummy embedding (NOT recommended for production).
        # This ensures the code runs for testing; replace with a real embedding provider sooner.
        import hashlib
        import struct
        h = hashlib.sha256(text.encode("utf-8")).digest()
        # create pseudo-random floats from the hash, repeat to reach INDEX_DIMENSION
        nums = []
        i = 0
        while len(nums) < INDEX_DIMENSION:
            chunk = h[i % len(h)]
            # map byte 0..255 to -1..1
            nums.append((chunk / 255.0) * 2 - 1)
            i += 1
        return nums[:INDEX_DIMENSION]

# -------------------------
# Simple Pinecone query wrapper
# -------------------------
def pinecone_query(query_text: str, top_k: int = 5, namespace: str = None) -> List[Dict[str, Any]]:
    vec = embed_text(query_text)
    # ensure vector length matches
    if len(vec) != INDEX_DIMENSION:
        raise RuntimeError(f"Embedding length {len(vec)} doesn't match index dimension {INDEX_DIMENSION}")

    # Query the index
    resp = index.query(
        vector=vec,
        top_k=top_k,
        include_metadata=True,
        include_values=False,  # don't fetch vectors
        namespace=namespace
    )
    # resp format depends on SDK. Return a normalized list of hits.
    hits = []
    # Try a few possible response shapes
    if hasattr(resp, "matches"):
        # older style
        for m in resp.matches:
            hits.append({
                "id": getattr(m, "id", None) or m.get("id"),
                "score": getattr(m, "score", None) or m.get("score"),
                "metadata": getattr(m, "metadata", None) or m.get("metadata"),
            })
    elif isinstance(resp, dict) and "matches" in resp:
        for m in resp["matches"]:
            hits.append({
                "id": m.get("id"),
                "score": m.get("score"),
                "metadata": m.get("metadata"),
            })
    else:
        # last resort, dump the whole response
        print("DEBUG: Unexpected Pinecone response shape:", type(resp))
        hits = [{"raw": resp}]
    return hits

# -------------------------
# Gemini wrapper (google-generativeai)
# -------------------------
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

class GeminiLLM:
    def __init__(self, model: str = "models/text-bison-001"):
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        # using chat.create for safe chat-style interface
        try:
            resp = genai.chat.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_output_tokens=max_tokens,
            )
            # Extract text from typical response shapes:
            if hasattr(resp, "message") and hasattr(resp.message, "content"):
                return resp.message.content
            if hasattr(resp, "candidates") and len(resp.candidates) > 0:
                return resp.candidates[0].content
            # if resp is dict-like:
            if isinstance(resp, dict):
                # try common keys
                if "candidates" in resp and len(resp["candidates"]) > 0:
                    return resp["candidates"][0].get("content", str(resp))
                if "message" in resp:
                    return resp["message"].get("content", str(resp))
            return str(resp)
        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {e}")

# -------------------------
# Postgres chat store (SQLAlchemy)
# -------------------------
from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_message = Column(Text, nullable=False)
    assistant_message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = create_engine(POSTGRES_CONN_STR, echo=False, future=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

class PostgresChatStore:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    def save_chat(self, user_message: str, assistant_message: str):
        session = self.session_maker()
        try:
            rec = ChatHistory(user_message=user_message, assistant_message=assistant_message)
            session.add(rec)
            session.commit()
            session.refresh(rec)
            return rec.id
        finally:
            session.close()

    def load_recent(self, limit: int = 20):
        session = self.session_maker()
        try:
            rows = session.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).limit(limit).all()
            return [
                {"id": r.id, "user_message": r.user_message, "assistant_message": r.assistant_message, "timestamp": r.timestamp}
                for r in rows
            ]
        finally:
            session.close()

# -------------------------
# Memory (uses Postgres store)
# -------------------------
class SimpleMemory:
    def __init__(self, chat_store: PostgresChatStore, max_items: int = 10):
        self.chat_store = chat_store
        self.max_items = max_items

    def add(self, user_msg: str, assistant_msg: str):
        self.chat_store.save_chat(user_msg, assistant_msg)

    def get_context(self) -> str:
        items = self.chat_store.load_recent(limit=self.max_items)
        items = list(reversed(items))
        return "\n".join([f"User: {i['user_message']}\nAssistant: {i['assistant_message']}" for i in items])

# -------------------------
# Agent tying everything together
# -------------------------
class RecommenderAgent:
    def __init__(self, pinecone_index, gemini_llm: GeminiLLM, chat_store: PostgresChatStore, memory: SimpleMemory):
        self.index = pinecone_index
        self.llm = gemini_llm
        self.chat_store = chat_store
        self.memory = memory

    def suggest(self, user_message: str, top_k: int = 5) -> str:
        # 1) retrieve
        hits = pinecone_query(user_message, top_k=top_k)
        snippets = []
        for h in hits:
            md = h.get("metadata") or {}
            # assume metadata contains "text" or "content"
            txt = md.get("text") or md.get("content") or md.get("source") or str(md)
            snippets.append(txt)

        # 2) build prompt (include memory + retrieved snippets)
        memory_ctx = self.memory.get_context()
        prompt_parts = [
            "You are a capstone project recommender assistant. Use the conversation memory and the retrieved snippets to answer.",
            f"Conversation memory:\n{memory_ctx}" if memory_ctx else "Conversation memory: (none)",
            "Retrieved snippets:\n" + ("\n---\n".join(snippets) if snippets else "(no snippets found)"),
            f"User question: {user_message}",
            "Provide a clear list of 5 recommended project ideas (title + short description + suggested dataset/techniques)."
        ]
        prompt = "\n\n".join(prompt_parts)

        # 3) synthesize with Gemini
        answer = self.llm.generate(prompt)
        # 4) store chat
        self.chat_store.save_chat(user_message, answer)
        return answer

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    gemini = GeminiLLM(model="models/text-bison-001")
    chat_store = PostgresChatStore(SessionLocal)
    memory = SimpleMemory(chat_store, max_items=10)
    agent = RecommenderAgent(index, gemini, chat_store, memory)

    q = "Suggest capstone project ideas related to time-series anomaly detection in finance."
    print("Querying...")
    resp = agent.suggest(q, top_k=5)
    print("Assistant response:\n", resp)

    print("\nRecent chats (db):", chat_store.load_recent(5))
