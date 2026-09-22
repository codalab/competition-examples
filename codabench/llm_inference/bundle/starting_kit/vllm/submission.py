# =============================================================================
# Starter kit: vLLM backend
# =============================================================================
# High-throughput inference. Requires a GPU. Edit the CONFIG block, then submit
# this file together with requirements.txt.
# =============================================================================
import os
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

# ---- CONFIG -----------------------------------------------------------------
HF_REPO_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"
HF_TOKEN = ""                 # only for PRIVATE / gated repos
SYSTEM_PROMPT = "You are a helpful assistant. Answer concisely."
TEMPERATURE = 0.7
TOP_P = 0.9
MAX_NEW_TOKENS = 128
MAX_MODEL_LEN = 2048
# -----------------------------------------------------------------------------


class Submission:

    backend = "vllm"
    model_name = HF_REPO_ID.split("/")[-1]

    def setup(self):
        if HF_TOKEN:
            os.environ["HF_TOKEN"] = HF_TOKEN
        print(f"[vllm] loading {HF_REPO_ID} ...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            HF_REPO_ID, token=HF_TOKEN or None
        )
        self.llm = LLM(model=HF_REPO_ID, max_model_len=MAX_MODEL_LEN)
        self.sampling = SamplingParams(
            temperature=TEMPERATURE, top_p=TOP_P, max_tokens=MAX_NEW_TOKENS
        )

    def _build_input(self, prompt):
        if getattr(self.tokenizer, "chat_template", None):
            messages = []
            if SYSTEM_PROMPT:
                messages.append({"role": "system", "content": SYSTEM_PROMPT})
            messages.append({"role": "user", "content": prompt})
            return self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        prefix = (SYSTEM_PROMPT + "\n\n") if SYSTEM_PROMPT else ""
        return f"{prefix}Question: {prompt}\nAnswer:"

    def generate(self, prompt):
        text = self._build_input(prompt)
        outputs = self.llm.generate([text], self.sampling)
        return outputs[0].outputs[0].text.strip()
