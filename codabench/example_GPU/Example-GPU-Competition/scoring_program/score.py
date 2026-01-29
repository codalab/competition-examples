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

    def load_ingestion_results(self, prediction_dir="./", score_dir="./"):
        """
        Load the ingestion results.

        Args:
            prediction_dir (str, optional): location of the predictions. Defaults to "./".
            score_dir (str, optional): location of the scores. Defaults to "./".
        """
        ingestion_results_with_set_index = []
        # loop over sets (1 set = 1 value of mu)
        for file in os.listdir(prediction_dir):
            if file.startswith("result_"):
                set_index = int(
                    file.split("_")[1].split(".")[0]
                )  # file format: result_{set_index}.json
                results_file = os.path.join(prediction_dir, file)
                with open(results_file) as f:
                    ingestion_results_with_set_index.append(
                        {"set_index": set_index, "results": json.load(f)}
                    )
        ingestion_results_with_set_index = sorted(
            ingestion_results_with_set_index, key=lambda x: x["set_index"]
        )
        self.ingestion_results = [
            x["results"] for x in ingestion_results_with_set_index
        ]

        self.score_file = os.path.join(score_dir, "scores.json")
        self.html_file = os.path.join(score_dir, "detailed_results.html")
        self.score_dir = score_dir
        logger.info(f"Read ingestion results from {prediction_dir}")

    def save_leaderboard_result(self, output_dir):

        score_file = os.path.join(output_dir, "scores.json")
        with open(score_file, "w") as f_score:
            f_score.write(json.dumps({"gpu_detected": self.gpu_detected}, indent=4))

    def write_html(self, content):
        with open(self.html_file, "a", encoding="utf-8") as f:
            f.write(content)
