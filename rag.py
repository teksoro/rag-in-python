import re
from pathlib import Path

import chromadb

from models import embed_docs, embed_query, ask
from show import step, sample, reply

# 1. load
source = "refunds.md"
text = Path("docs", source).read_text()
step(1, "load", len(text.split()), "words")

# 2. chunk
ENDS = re.compile(r"(?<=[.?!]) ")


def split(text, limit=60):
    chunks, heading = [], ""
    for para in text.split("\n\n"):
        para = " ".join(para.split())
        if para.startswith("#"):
            heading = para + " "
            continue
        para, heading = heading + para, ""
        current = ""
        for sentence in ENDS.split(para):
            longer = f"{current} {sentence}".strip()
            too_long = len(longer.split()) > limit
            if current and too_long:
                chunks.append(current)
                current = sentence
            else:
                current = longer
        chunks.append(current)
    return chunks


chunks = split(text)
step(2, "chunk", len(chunks), "chunks")

# 3. embed
vectors = embed_docs(chunks)
dims = len(vectors[0])
step(3, "embed", len(vectors), "x", dims, "numbers")

# 4. store
client = chromadb.PersistentClient(path="store")
cosine = {"hnsw": {"space": "cosine"}}
pages = client.get_or_create_collection(
    "help", configuration=cosine
)
ids = [f"{source}-{i}" for i in range(len(chunks))]
pages.upsert(
    ids=ids,
    embeddings=vectors,
    documents=chunks,
    metadatas=[{"source": source} for _ in chunks],
)
step(4, "store", pages.count(), "chunks saved")


def answer(question, k=2):
    # 5. search
    query = embed_query(question)
    found = pages.query(
        query_embeddings=[query], n_results=k
    )
    texts = found["documents"][0]
    scores = [1 - d for d in found["distances"][0]]
    step(5, "search", [round(s, 3) for s in scores])

    # 6. answer
    context = "\n\n".join(texts)
    prompt = (
        "Answer only from the context. If the "
        "answer is not there, say you don't know."
        f"\n\nContext:\n{context}"
        f"\n\nQuestion: {question}"
    )
    notes = found["metadatas"][0]
    sources = sorted({n["source"] for n in notes})
    step(6, "answer", "using", *sources)
    reply(ask(prompt))


answer(
    "I bought the annual plan 12 days ago. "
    "Can I get my money back?"
)
answer("Who is the chief executive of Hazelpad?")
