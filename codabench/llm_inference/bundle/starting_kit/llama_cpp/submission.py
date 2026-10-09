# =============================================================================
# Starter kit: llama.cpp backend (via llama-cpp-python)
# =============================================================================
# Downloads a GGUF file straight from the HF Hub and runs it with llama.cpp.
# Works on CPU or GPU (build llama-cpp-python with CUDA for GPU offloading).
# Edit the CONFIG block, then submit this file together with requirements.txt.
# =============================================================================
from llama_cpp import Llama

# ---- CONFIG -----------------------------------------------------------------
# Point at a GGUF repo and the GGUF filename (glob patterns allowed).
HF_REPO_ID = "bartowski/SmolLM2-135M-Instruct-GGUF"
GGUF_FILENAME = "*Q4_K_M.gguf"
HF_TOKEN = ""                 # only for PRIVATE / gated repos
SYSTEM_PROMPT = "You are a helpful assistant. Answer concisely."
TEMPERATURE = 0.7
TOP_P = 0.9
MAX_NEW_TOKENS = 128
N_CTX = 2048
N_GPU_LAYERS = -1             # -1 = offload all layers to GPU (0 = CPU only)
# -----------------------------------------------------------------------------


class Submission:

    backend = "llama.cpp"
    model_name = HF_REPO_ID.split("/")[-1]

    def setup(self):
        print(f"[llama.cpp] downloading {HF_REPO_ID} ({GGUF_FILENAME}) ...")
        self.llm = Llama.from_pretrained(
            repo_id=HF_REPO_ID,
            filename=GGUF_FILENAME,
            n_ctx=N_CTX,
            n_gpu_layers=N_GPU_LAYERS,
            token=HF_TOKEN or None,
            verbose=False,
        )

    def generate(self, prompt):
        messages = []
        if SYSTEM_PROMPT:
            messages.append({"role": "system", "content": SYSTEM_PROMPT})
        messages.append({"role": "user", "content": prompt})
        response = self.llm.create_chat_completion(
            messages=messages,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=MAX_NEW_TOKENS,
        )
        return response["choices"][0]["message"]["content"].strip()
