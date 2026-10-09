# Overview
***

This is an example **LLM inference** competition where **you choose the
inference backend**. Use whatever you like — Hugging Face **Transformers**,
**vLLM**, **Ollama**, or **llama.cpp** — as long as your code implements a tiny
contract.

## What you submit

Just **two files** (zip them together and upload):

| File | Purpose |
| --- | --- |
| `requirements.txt` | Extra pip packages your backend needs. Installed by the worker before running. |
| `submission.py` | Defines a `Submission` class that loads your model and answers prompts. |

### The `Submission` contract

```python
class Submission:
    def setup(self):
        """Download / load the model, start the backend. Called once."""

    def generate(self, prompt: str) -> str:
        """Return the model's answer to a single prompt."""

    def teardown(self):          # optional
        """Free resources / stop servers."""
```

Optionally set `self.model_name` and `self.backend` (or class attributes) so
they show up on the leaderboard.

Your `submission.py` also holds your **Hugging Face repo id** and, if the repo
is **private / gated**, an **HF token** — right in the CONFIG block at the top
of the file. Submissions are visible to the organizers, so use a disposable,
read-only token.

## Starter kits

Ready-to-edit `submission.py` + `requirements.txt` for every backend live in
[`starting_kit/`](starting_kit/):

* `starting_kit/transformers/` — Hugging Face Transformers
* `starting_kit/vllm/` — vLLM (high throughput, GPU)
* `starting_kit/ollama/` — Ollama (pulls GGUF from HF Hub)
* `starting_kit/llama_cpp/` — llama.cpp via `llama-cpp-python` (GGUF)

Pick one, edit the CONFIG block, zip the two files, and submit. The default
sample submission uses the Transformers backend.

## Goal

Answer the hidden questions accurately while keeping latency low. See the
**Evaluation** page for the metrics.
