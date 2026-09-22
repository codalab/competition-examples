# =============================================================================
# Starter kit: Hugging Face Transformers backend
# =============================================================================
# Edit the CONFIG block, then submit this file together with requirements.txt.
# The ingestion program calls: setup() once, generate(prompt) per prompt.
# =============================================================================
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

# ---- CONFIG -----------------------------------------------------------------
HF_REPO_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"  # namespace/name on HF Hub
HF_TOKEN = ""                 # only for PRIVATE / gated repos (use a disposable token)
SYSTEM_PROMPT = "You are a helpful assistant. Answer concisely."
TEMPERATURE = 0.7
TOP_P = 0.9
DO_SAMPLE = True              # False => deterministic greedy decoding
MAX_NEW_TOKENS = 128
MAX_CONTEXT_LENGTH = 2048
# -----------------------------------------------------------------------------


class Submission:

    backend = "transformers"
    model_name = HF_REPO_ID.split("/")[-1]

    def setup(self):
        if HF_TOKEN:
            login(token=HF_TOKEN)
        token = HF_TOKEN or None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[transformers] device: {self.device}, downloading {HF_REPO_ID} ...")
        self.tokenizer = AutoTokenizer.from_pretrained(HF_REPO_ID, token=token)
        self.model = AutoModelForCausalLM.from_pretrained(
            HF_REPO_ID,
            token=token,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
        ).to(self.device)
        self.model.eval()
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def _build_input(self, prompt):
        if getattr(self.tokenizer, "chat_template", None):
            messages = []
            if SYSTEM_PROMPT:
                messages.append({"role": "system", "content": SYSTEM_PROMPT})
            messages.append({"role": "user", "content": prompt})
            try:
                return self.tokenizer.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True
                )
            except Exception:
                # Some chat templates reject a system role outright (Gemma's
                # raises "System role not supported"). Fold the system prompt
                # into the first user turn instead.
                merged = f"{SYSTEM_PROMPT}\n\n{prompt}" if SYSTEM_PROMPT else prompt
                return self.tokenizer.apply_chat_template(
                    [{"role": "user", "content": merged}],
                    tokenize=False,
                    add_generation_prompt=True,
                )
        prefix = (SYSTEM_PROMPT + "\n\n") if SYSTEM_PROMPT else ""
        return f"{prefix}Question: {prompt}\nAnswer:"

    def generate(self, prompt):
        text = self._build_input(prompt)
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, max_length=MAX_CONTEXT_LENGTH
        ).to(self.device)
        do_sample = DO_SAMPLE and TEMPERATURE > 0
        gen_kwargs = dict(
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=do_sample,
            pad_token_id=self.tokenizer.pad_token_id,
        )
        if do_sample:
            gen_kwargs.update(temperature=TEMPERATURE, top_p=TOP_P)
        with torch.no_grad():
            output_ids = self.model.generate(**inputs, **gen_kwargs)
        new_tokens = output_ids[0][inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
