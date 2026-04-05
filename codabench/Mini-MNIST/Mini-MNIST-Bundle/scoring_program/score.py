# ------------------------------------------
# Imports
# ------------------------------------------
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime as dt

from sklearn.metrics import accuracy_score


class Scoring:
    """
    This class is used to compute the scores for the competition.

    Atributes:
        * start_time (datetime): The start time of the scoring process.
        * end_time (datetime): The end time of the scoring process.
        * y_true (np.ndarray): The ground truth test labels.
        * y_pred (np.ndarray): The model's predictions.
        * scores_dict (dict): The scores dictionary.
    """

    def __init__(self):
        """
        Initialize the Scoring class.
        """
        self.start_time = None
        self.end_time = None
        self.y_true = None
        self.y_pred = None
        self.scores_dict = {}

    def start_timer(self):
        """
        Start the timer for the scoring process.
        """
        self.start_time = dt.now()

    def stop_timer(self):
        """
        Stop the timer for the scoring process.
        """
        self.end_time = dt.now()

    def get_duration(self):
        """
        Get the duration of the scoring process.

        Returns:
            timedelta: The duration of the scoring process.
        """
        if self.start_time is None:
            print("[-] Timer was never started. Returning None")
            return None

        if self.end_time is None:
            print("[-] Timer was never stoped. Returning None")
            return None

        return self.end_time - self.start_time

    def load_reference_data(self, reference_dir):
        """
        Load the reference data.

        Args:
            reference_dir (str): The reference data directory name.
        """
        print("[*] Reading reference data")
        reference_data_file = os.path.join(reference_dir, "test_labels.csv")
        if os.path.exists(reference_data_file):
            df_ref = pd.read_csv(reference_data_file)
            # Ensure sorting to match predictions order in ingestion
            df_ref = df_ref.sort_values(by="filename")
            self.y_true = df_ref['label'].values

    def load_ingestion_result(self, predictions_dir):
        """
        Load the ingestion result.

        Args:
            predictions_dir (str): The predictions directory name.
        """
        print("[*] Reading ingestion result (predictions)")
        prediction_file = os.path.join(predictions_dir, "predictions.npy")
        if os.path.exists(prediction_file):
            self.y_pred = np.load(prediction_file)

    def compute_scores(self):
        """
        Compute the scores for the competition.

        """
        print("[*] Computing scores")
        if self.y_true is not None and self.y_pred is not None:
            if len(self.y_true) != len(self.y_pred):
                print(f"[-] Shape mismatch: y_true {len(self.y_true)}, y_pred {len(self.y_pred)}")
                self.scores_dict = {"score": 0.0}
                return

            accuracy = accuracy_score(self.y_true, self.y_pred)
            self.scores_dict = {"score": accuracy}
            print(f"[*] Accuracy: {accuracy}")
        else:
            print("[-] Missing ground truth or predictions")
            self.scores_dict = {"score": 0.0}

    def write_scores(self, output_dir):
        """
        Write the scoring results to a file.

        Args:
            output_dir (str): The output directory name.
        """
        print("[*] Writing scores")
        score_file = os.path.join(output_dir, "scores.json")
        with open(score_file, "w") as f_score:
            f_score.write(json.dumps(self.scores_dict, indent=4))
