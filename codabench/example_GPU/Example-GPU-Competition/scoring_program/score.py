# ------------------------------------------
# Imports
# ------------------------------------------
import json
import os


class Scoring:

    def load_ingestion_output(self, prediction_dir):

        ingestion_output_file = os.path.join(prediction_dir, "gpu_status.json")
        with open(ingestion_output_file) as f:
            self.gpu_detected = json.load(f)["gpu_detected"]
        print(f"GPU Detected: {self.gpu_detected}")

    def save_leaderboard_result(self, output_dir):

        score_file = os.path.join(output_dir, "scores.json")
        with open(score_file, "w") as f_score:
            f_score.write(json.dumps({"gpu_detected": self.gpu_detected}, indent=4))
