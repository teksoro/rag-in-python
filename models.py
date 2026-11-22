# The two models this file talks to.
# Vectors: a small open embedding model,
#          running in Docker on this machine.
# Answers: Claude Haiku, over the API.
import json
import urllib.request
import anthropic

URL = "http://127.0.0.1:11434/api/embed"
client = anthropic.Anthropic()


def embed(texts, model="nomic-embed-text"):
    body = {"model": model, "input": texts}
    data = json.dumps(body).encode()
    request = urllib.request.Request(URL, data)
    with urllib.request.urlopen(request) as r:
        return json.load(r)["embeddings"]


def embed_docs(chunks):
    return embed(
        ["search_document: " + c for c in chunks]
    )


def embed_query(question):
    return embed(["search_query: " + question])[0]


def ask(prompt):
    message = {"role": "user", "content": prompt}
    reply = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1500,
        messages=[message],
    )
    texts = [
        block.text
        for block in reply.content
        if block.type == "text"
    ]
    return "".join(texts)
