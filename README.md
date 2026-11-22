# RAG in Python

The program from the teksoro video series "RAG in Python": retrieval-augmented generation in 91 lines, and the help page it reads.

It answers a customer's question from one page. It loads the page, cuts it into chunks, embeds them, stores them, searches for the chunks closest to the question, and hands those to a language model with a rule: answer only from the context, and if the answer is not there, say you don't know.

Hazelpad, the company on the help page, is made up for this example and is not related to any real product.

## Files

| File | What it is |
|---|---|
| `rag.py` | The whole program, as read from top to bottom in lesson 7 |
| `models.py` | The two models it talks to: an embedding model for vectors, and Claude Haiku for answers |
| `show.py` | Prints one aligned line per step |
| `docs/refunds.md` | The help page |

## Run it

You need Python 3, an Ollama server with the `nomic-embed-text` model, and an Anthropic API key.

Start Ollama in Docker and get the embedding model:

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull nomic-embed-text
```

Install the two libraries and set your key:

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key
```

Run the program:

```bash
python3 rag.py
```

Each run makes two calls to Claude Haiku, one for each question at the bottom of `rag.py`.

## What it prints

```text
1. load    443 words
2. chunk   10 chunks
3. embed   10 x 768 numbers
4. store   10 chunks saved
5. search  [0.708, 0.672]
6. answer  using refunds.md
  Yes. Annual plans can be refunded within
  30 days of purchase, and you bought
  yours 12 days ago, so you're within the
  refund window.
5. search  [0.605, 0.601]
6. answer  using refunds.md
  I don't know. The context covers refund
  windows and refunds and cancellations
  for Hazelpad plans, but it doesn't
  mention who the chief executive is.
```

This is one run. The model's wording changes from run to run, and the scores can shift with the version of the embedding model. The program keeps its stored chunks in a `store` folder next to it.

## The lessons

1. Build RAG in Python: a working program in 5 steps: https://youtu.be/3BjM6wEEltw
2. Chunking: https://youtu.be/bYzzIiTymKc
3. Embeddings: https://youtu.be/sYy_BgnVueU
4. Cosine similarity: https://youtu.be/GGOfO_0EYvU
5. Vector databases: https://youtu.be/r2LGli_eAjM
6. The prompt: https://youtu.be/utd0Yf7mbbs
7. The finished program: https://youtu.be/VGs1zypRYqM

## Licence

MIT. See `LICENSE`.

teksoro: AI engineering explained. teksoro.com
