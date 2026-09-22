# ------------------------------------------
# Scoring program for the LLM Inference competition
#
# It compares the model's generated answers (from the ingestion program)
# against the hidden reference answers and computes:
#   - accuracy   : fraction of answers that contain the reference (normalized)
#   - f1         : mean token-level F1 between prediction and reference
#   - avg_latency: mean generation time per prompt (seconds)
# ------------------------------------------
import os
import re
import json
import string


def normalize(text):
    """Lower-case, strip punctuation/articles/extra whitespace (SQuAD-style)."""
    text = text.lower()
    text = "".join(ch for ch in text if ch not in string.punctuation)
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    return " ".join(text.split())


def token_f1(prediction, reference):
    pred_tokens = normalize(prediction).split()
    ref_tokens = normalize(reference).split()
    if not pred_tokens or not ref_tokens:
        return float(pred_tokens == ref_tokens)
    common = {}
    for t in pred_tokens:
        if t in ref_tokens:
            common[t] = min(pred_tokens.count(t), ref_tokens.count(t))
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0
    precision = num_same / len(pred_tokens)
    recall = num_same / len(ref_tokens)
    return 2 * precision * recall / (precision + recall)


def contains_match(prediction, reference):
    """1 if the normalized reference appears in the normalized prediction."""
    return float(normalize(reference) in normalize(prediction))


class Scoring:

    def load_predictions(self, prediction_dir):
        preds_file = os.path.join(prediction_dir, "predictions.jsonl")
        self.predictions = {}
        self.latencies = []
        if not os.path.exists(preds_file):
            raise FileNotFoundError(
                f"{preds_file} is missing, so the ingestion program produced no "
                f"predictions. Check the ingestion logs above for the real error "
                f"(model download or inference most likely failed)."
            )
        with open(preds_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                p = json.loads(line)
                self.predictions[p["id"]] = p.get("prediction", "")
                if "latency" in p:
                    self.latencies.append(float(p["latency"]))

        self.model_name = "unknown-model"
        meta_file = os.path.join(prediction_dir, "metadata.json")
        if os.path.exists(meta_file):
            with open(meta_file) as f:
                self.model_name = json.load(f).get("model_name", "unknown-model")
        print(f"[scoring] Loaded {len(self.predictions)} predictions "
              f"for model '{self.model_name}'.")

    def load_reference(self, reference_dir):
        ref_file = os.path.join(reference_dir, "reference.jsonl")
        self.reference = {}
        with open(ref_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                self.reference[r["id"]] = r["answer"]
        print(f"[scoring] Loaded {len(self.reference)} reference answers.")

    def compute_scores(self):
        acc, f1 = [], []
        for qid, gold in self.reference.items():
            pred = self.predictions.get(qid, "")
            acc.append(contains_match(pred, gold))
            f1.append(token_f1(pred, gold))

        n = max(len(self.reference), 1)
        self.scores = {
            "accuracy": round(sum(acc) / n, 4),
            "f1": round(sum(f1) / n, 4),
            "avg_latency": round(
                sum(self.latencies) / len(self.latencies), 4
            ) if self.latencies else 0.0,
            "model_name": self.model_name,
        }
        print(f"[scoring] Scores: {self.scores}")
        return self.scores

    def save_scores(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        score_file = os.path.join(output_dir, "scores.json")
        with open(score_file, "w") as f:
            json.dump(self.scores, f, indent=4)
        print(f"[scoring] Wrote {score_file}")
