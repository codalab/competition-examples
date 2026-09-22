# ------------------------------------------
# Ingestion program for the "bring your own backend" LLM Inference competition
#
# The participant submits exactly two files:
#   - requirements.txt : extra pip packages for their inference backend
#   - submission.py    : defines a `Submission` class (see the contract below)
#
# This program:
#   1. pip-installs the submission's requirements.txt.
#   2. Imports `Submission` from submission.py.
#   3. Calls setup() once, generate(prompt) for every hidden prompt, teardown().
#   4. Saves predictions.jsonl for the scoring program.
#
# ---- Submission contract -------------------------------------------------
#   class Submission:
#       def setup(self) -> None:
#           '''Download / load the model, start the backend. Called once.'''
#       def generate(self, prompt: str) -> str:
#           '''Return the model's answer to a single prompt.'''
#       def teardown(self) -> None:   # optional
#           '''Free resources / stop servers.'''
# --------------------------------------------------------------------------
import os
import sys
import json
import time
import importlib
import subprocess


class Ingestion:

    def install_requirements(self, submission_dir):
        """pip-install the submission's requirements.txt (if present)."""
        req = os.path.join(submission_dir, "requirements.txt")
        if os.path.exists(req) and os.path.getsize(req) > 0:
            print(f"[ingestion] Installing requirements from {req} ...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet", "-r", req]
            )
        else:
            print("[ingestion] No requirements.txt found (or empty); skipping.")

    def load_submission(self, submission_dir):
        """Import submission.py and instantiate the participant's Submission."""
        sys.path.insert(0, submission_dir)
        if "submission" in sys.modules:
            importlib.reload(sys.modules["submission"])
        submission_module = importlib.import_module("submission")
        if not hasattr(submission_module, "Submission"):
            raise AttributeError(
                "submission.py must define a class named `Submission`."
            )
        self.model = submission_module.Submission()
        for method in ("setup", "generate"):
            if not hasattr(self.model, method):
                raise AttributeError(
                    f"Submission class must implement `{method}(...)`."
                )
        print("[ingestion] Submission loaded.")

    def load_prompts(self, input_dir):
        prompts_file = os.path.join(input_dir, "prompts.jsonl")
        self.prompts = []
        with open(prompts_file) as f:
            for line in f:
                line = line.strip()
                if line:
                    self.prompts.append(json.loads(line))
        print(f"[ingestion] Loaded {len(self.prompts)} prompts.")

    def run_inference(self):
        print("[ingestion] Running setup() ...")
        self.model.setup()

        self.predictions = []
        for item in self.prompts:
            start = time.time()
            try:
                answer = self.model.generate(item["prompt"])
            except Exception as exc:  # keep going, record the failure
                answer = ""
                print(f"[ingestion] generate() failed for id={item['id']}: {exc}")
            latency = time.time() - start
            answer = "" if answer is None else str(answer).strip()
            self.predictions.append({
                "id": item["id"],
                "prediction": answer,
                "latency": round(latency, 4),
            })
            print(f"[ingestion] id={item['id']} ({latency:.2f}s): {answer[:80]!r}")

        if hasattr(self.model, "teardown"):
            print("[ingestion] Running teardown() ...")
            try:
                self.model.teardown()
            except Exception as exc:
                print(f"[ingestion] teardown() raised (ignored): {exc}")

    def save_predictions(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        out_file = os.path.join(output_dir, "predictions.jsonl")
        with open(out_file, "w") as f:
            for p in self.predictions:
                f.write(json.dumps(p) + "\n")

        model_name = getattr(self.model, "model_name", "unknown-model")
        backend = getattr(self.model, "backend", "unknown")
        with open(os.path.join(output_dir, "metadata.json"), "w") as f:
            json.dump({
                "model_name": model_name,
                "backend": backend,
                "num_predictions": len(self.predictions),
            }, f, indent=4)
        print(f"[ingestion] Saved {len(self.predictions)} predictions to {out_file}")
