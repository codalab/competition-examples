# Starter kits

Each folder is a complete, ready-to-submit example for one inference backend.
Pick one, edit the `CONFIG` block at the top of `submission.py` (set your HF
repo id, and a token if the repo is private), then **zip `submission.py` and
`requirements.txt` together** and upload as your submission.

| Backend | Folder | Notes |
| --- | --- | --- |
| Transformers | `transformers/` | Simplest; works on CPU or GPU. This is the default sample submission. |
| vLLM | `vllm/` | High throughput; needs a GPU. |
| Ollama | `ollama/` | Installs & runs a local Ollama server; pulls GGUF from `hf.co/<user>/<repo>`. |
| llama.cpp | `llama_cpp/` | Uses `llama-cpp-python`; downloads a single GGUF file from the HF Hub. |

## The contract every `submission.py` implements

```python
class Submission:
    def setup(self):                 # download / load model (called once)
        ...
    def generate(self, prompt: str) -> str:   # answer one prompt
        ...
    def teardown(self):              # optional cleanup
        ...
```

Set `self.model_name` / `self.backend` (or class attributes) to control what
appears on the leaderboard.
