# ------------------------------------------
# Imports
# ------------------------------------------
import os
import json
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime as dt


class Ingestion:
    """
    Class for handling the ingestion process.

    Args:
        None

    Attributes:
        * start_time (datetime): The start time of the ingestion process.
        * end_time (datetime): The end time of the ingestion process.
        * model (object): The model object.
        * X_train (np.ndarray): The train images.
        * y_train (np.ndarray): The train labels.
        * X_test (np.ndarray): The test images.
        * y_pred (np.ndarray): The test predictions.
        * ingestion_result (dict): The ingestion result dict.
    """

    def __init__(self):
        """
        Initialize the Ingestion class.
        """
        self.start_time = None
        self.end_time = None
        self.model = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_pred = None
        self.ingestion_result = {}

    def start_timer(self):
        """
        Start the timer for the ingestion process.
        """
        self.start_time = dt.now()

    def stop_timer(self):
        """
        Stop the timer for the ingestion process.
        """
        self.end_time = dt.now()

    def get_duration(self):
        """
        Get the duration of the ingestion process.

        Returns:
            timedelta: The duration of the ingestion process.
        """
        if self.start_time is None:
            print("[-] Timer was never started. Returning None")
            return None

        if self.end_time is None:
            print("[-] Timer was never stopped. Returning None")
            return None

        return self.end_time - self.start_time

    def load_train_and_test_data(self, input_dir):
        """
        Load the training and testing data.

        Args:
            input_dir (str): The input directory name.
        """
        print("[*] Loading data")

        # Load Training Data
        train_data_dir = os.path.join(input_dir, "train_data")
        train_labels_file = os.path.join(input_dir, "train_labels.csv")
        if os.path.exists(train_labels_file) and os.path.isdir(train_data_dir):
            df_train = pd.read_csv(train_labels_file)
            images = []
            for filename in df_train['filename']:
                img_path = os.path.join(train_data_dir, filename)
                img = Image.open(img_path)
                images.append(np.array(img))
            self.X_train = np.array(images)
            self.y_train = df_train['label'].values

        # Load Test Data
        test_data_dir = os.path.join(input_dir, "test_data")
        if os.path.isdir(test_data_dir):
            # Sort files to ensure consistency with reference labels
            test_files = sorted([f for f in os.listdir(test_data_dir) if f.endswith('.png')])
            images = []
            for filename in test_files:
                img_path = os.path.join(test_data_dir, filename)
                img = Image.open(img_path)
                images.append(np.array(img))
            self.X_test = np.array(images)

    def init_submission(self, Model):
        """
        Initialize the submitted model.

        Args:
            Model (object): The model class.
        """
        print("[*] Initializing Submitted Model")
        self.model = Model()

    def fit_submission(self):
        """
        Fit the submitted model.
        """
        print("[*] Fitting Submitted Model")
        if self.X_train is not None and self.y_train is not None:
            self.model.fit(self.X_train, self.y_train)

    def predict_submission(self):
        """
        Make predictions using the submitted model.
        """
        print("[*] Predicting")
        if self.X_test is not None:
            self.y_pred = self.model.predict(self.X_test)

    def save_predictions(self, output_dir=None):
        """
        Save the ingestion result to files.

        Args:
            output_dir (str): The output directory to save the result files.
        """
        if self.y_pred is not None:
            prediction_file = os.path.join(output_dir, "predictions.npy")
            np.save(prediction_file, self.y_pred)
            print(f"[*] Saved predictions to {prediction_file}")
