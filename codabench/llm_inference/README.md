# LLM Inference

A [Codabench](https://www.codabench.org/) bundle for LLM inference where
participants **choose their own inference library**. The goal is to run
inference on a **GPU worker**: participants submit code, the ingestion
program runs it against a hidden set of prompts, and the scoring program
evaluates the generated answers.

* [View the bundle](bundle/)
* [Download the bundle](bundle.zip)
* [Download example submissions](submission_examples/)

A submission is just two files — `requirements.txt` and `submission.py` —
where `submission.py` implements a tiny `Submission` contract (`setup` /
`generate` / `teardown`). The **ingestion** program installs the requirements
and runs the model on a hidden set of prompts; the **scoring** program
evaluates the answers and writes the leaderboard metrics.

Starter kits are provided for **Transformers**, **vLLM**, **Ollama**, and
**llama.cpp** — so a participant can bring any of them without the organizer
changing the competition.

---

## Table of contents

1. [How it works](#how-it-works)
2. [Bundle layout](#bundle-layout)
3. [The `Submission` contract](#the-submission-contract)
4. [Run it locally](#run-it-locally)
5. [Make it YOUR challenge](#make-it-your-challenge)
6. [Backends and Docker images](#backends-and-docker-images)
7. [Deploy to Codabench](#deploy-to-codabench)

---

## How it works

```text
participant submits                organizer's bundle runs on a GPU worker
┌──────────────────┐               ┌───────────────────────────────────────────┐
│ requirements.txt │──pip install─▶│ ingestion_program/                        │
│ submission.py    │──import ─────▶│   setup() ▸ generate(prompt)×N ▸ teardown │
└──────────────────┘               │        │ predictions.jsonl                 │
                                   │        ▼                                   │
        input_data/prompts.jsonl ─▶│ scoring_program/  ── scores.json ──▶ leaderboard
        reference_data/*  (hidden) │   accuracy · token-F1 · avg latency        │
                                   └───────────────────────────────────────────┘
```

1. **Ingestion** ([`ingestion_program/`](bundle/ingestion_program/))
   pip-installs the submission's `requirements.txt`, imports its `Submission`
   class, calls `setup()` once, then `generate(prompt)` for every prompt in
   `input_data/prompts.jsonl`, and writes `predictions.jsonl` (+ latency).
2. **Scoring** ([`scoring_program/`](bundle/scoring_program/))
   compares predictions to the hidden `reference_data/reference.jsonl` and
   reports **accuracy**, **token F1**, and **average latency**.

## Bundle layout

```text
.
├── README.md                   # this file
├── bundle.zip                  # zipped bundle, ready to upload to Codabench
├── submission_examples/        # ready-to-upload example submissions, one per backend
└── bundle/                     # the Codabench bundle
    ├── competition.yaml            # phases, tasks, leaderboard, docker_image
    ├── logo.png
    ├── pages/                      # overview / evaluation / terms (markdown)
    ├── input_data/prompts.jsonl    # prompts shown to the model (public here)
    ├── reference_data/reference.jsonl  # gold answers (KEEP HIDDEN in real use)
    ├── ingestion_program/          # runs the submission -> predictions.jsonl
    ├── scoring_program/            # predictions vs reference -> scores.json
    ├── sample_code_submission/     # default solution (Transformers)
    ├── sample_result_submission/   # example ingestion output
    └── starting_kit/               # ready-to-edit submissions, one per backend
        ├── transformers/  vllm/  ollama/  llama_cpp/
        └── README.md
```

## The `Submission` contract

Everything a participant writes implements this:

```python
class Submission:
    backend = "transformers"        # optional: shows on the leaderboard
    model_name = "my-model"         # optional: shows on the leaderboard

    def setup(self):
        """Download / load the model, start the backend. Called ONCE.
        Not counted toward latency — do the heavy lifting here."""

    def generate(self, prompt: str) -> str:
        """Return the model's answer to a single prompt. Must return a string;
        if it raises, the answer is recorded empty and the run continues."""

    def teardown(self):             # optional
        """Free resources / stop servers. Called once at the end."""
```

## Run it locally

No Codabench needed to test the flow. From this folder:

```bash
cd bundle

# Run the sample (Transformers) submission end-to-end.
# Needs the sample deps (torch + transformers); a GPU is optional for the
# tiny 135M default model but recommended.
pip install -r sample_code_submission/requirements.txt
python3 ingestion_program/run_ingestion.py     # -> sample_result_submission/predictions.jsonl

# Scoring uses only the Python standard library:
python3 scoring_program/run_scoring.py          # -> scoring_output/scores.json
```

To test a *different* backend locally, copy that starter kit's two files into a
folder and point ingestion at it (or drop them into `sample_code_submission/`).

## Make it YOUR challenge

The defaults are a trivial trivia task (capital of France, 2+2, …) so the
plumbing is easy to verify. To turn it into a real competition:

1. **Swap the data.** Replace
   [`input_data/prompts.jsonl`](bundle/input_data/prompts.jsonl)
   (`{"id": ..., "prompt": ...}` per line) and
   [`reference_data/reference.jsonl`](bundle/reference_data/reference.jsonl)
   (`{"id": ..., "answer": ...}` per line). Keep the `id`s aligned.
   **In a real competition the reference data stays hidden on the server** — it
   is public here only because this is a template.
2. **Adjust the metrics** in
   [`scoring_program/score.py`](bundle/scoring_program/score.py).
   It currently does SQuAD-style `accuracy` (reference contained in answer),
   token `f1`, and `avg_latency`. Change these to fit your task (exact match,
   BLEU, an LLM judge, cost, …) and update the leaderboard `columns` in
   `competition.yaml` to match the keys you emit in `scores.json`.
3. **Edit the pages** in
   [`pages/`](bundle/pages/) (overview / evaluation /
   terms) and `competition.yaml` (title, dates, phases). Replace `logo.png`.
4. **Pick the worker image** — see below.

## Backends and Docker images

The ingestion program installs each submission's `requirements.txt` at run
time, so **any** backend works on a GPU worker with internet access. Some
backends run much faster (or, for llama.cpp, only reach the GPU) when their
runtime is **baked into the worker image** — the Dockerfiles for these worker
images live in a separate repo: [worker images]().


| Backend          | Starter kit                  | Worker image needed?                                                                                                                                                                                                                                |
| ------------------ | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Transformers** | `starting_kit/transformers/` | None — stock `codalab/codalab-legacy:gpu310` already has torch + CUDA. This is the default sample submission.                                                                                                                                         |
| **vLLM**         | `starting_kit/vllm/`         | *Recommended:* [moujar/codabench-gpu-vllm:0.6.3](https://hub.docker.com/repository/docker/moujar/codabench-gpu-vllm). Without it, vLLM re-downloads its own multi-GB torch build every run.                                                         |
| **llama.cpp**    | `starting_kit/llama_cpp/`    | *Recommended:* [moujar/codabench-llama_cpp:0.1](https://hub.docker.com/repository/docker/moujar/codabench-llama_cpp). GPU offload needs `llama-cpp-python` compiled with CUDA — the worker can't compile it, so without the image it runs CPU-only. |
| **Ollama**       | `starting_kit/ollama/`       | **Required:** [moujar/codabench-gpu-ollama:0.32.0](https://hub.docker.com/repository/docker/moujar/codabench-gpu-ollama). The worker can't apt-install; otherwise every run downloads a 1.4 GB tarball.                                             |

## Deploy to Codabench

1. Choose and set `docker_image` in
   [`competition.yaml`](bundle/competition.yaml)
   (stock image for Transformers; otherwise the matching custom image you built
   and pushed).
2. Zip the **contents** of `bundle/` (so
   `competition.yaml` sits at the zip root) — or use the prebuilt
   [`bundle.zip`](bundle.zip).
3. On [Codabench](https://www.codabench.org/): **Benchmarks → Management →
   Upload**, then attach the competition to a **queue with GPU workers**.
   Workers need **internet access** to `pip install` requirements and download
   models from the Hugging Face Hub.
