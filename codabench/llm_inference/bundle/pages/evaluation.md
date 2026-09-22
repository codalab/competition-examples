# Evaluation
***

The ingestion program installs your `requirements.txt`, imports your
`Submission` class, calls `setup()` once, then `generate(prompt)` for every
hidden prompt. The scoring program compares each answer to the reference answer.

| Metric | Description | Better |
| --- | --- | --- |
| **Accuracy** | Fraction of answers that *contain* the (normalized) reference answer. | higher |
| **Token F1** | Mean token-level F1 overlap between answer and reference (SQuAD-style normalization). | higher |
| **Avg latency (s)** | Mean wall-clock time of your `generate()` call per prompt. | lower |

The leaderboard is ranked primarily by **Accuracy**.

## Rules of the contract

- `setup()` is called **once** before any prompt (do the model download /
  server start there — it is not counted in latency).
- `generate(prompt)` must return a **string**. If it raises, the answer is
  recorded as empty and inference continues with the next prompt.
- `teardown()` is optional and called once at the end.

## Notes for organizers

- This is a **template**. Swap `input_data/prompts.jsonl` and
  `reference_data/reference.jsonl` for your own task, and adjust the metrics in
  `scoring_program/score.py`.
- Inference needs a **GPU worker**: set the queue to a GPU queue and keep the
  `codalab/codalab-legacy:gpu310` Docker image (or one with `torch` + CUDA).
- The worker needs **internet access** to `pip install` the submission's
  requirements and to download models from the Hugging Face Hub.
