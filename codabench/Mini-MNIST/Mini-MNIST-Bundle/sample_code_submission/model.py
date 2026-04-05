import numpy as np
from sklearn.ensemble import RandomForestClassifier


class Model:
    """
    A simple baseline model for digit classification using Scikit-learn.
    Uses a Random Forest Classifier.
    """
    def __init__(self):
        # A light-weight Random Forest with 10 trees for fast execution
        self.clf = RandomForestClassifier(n_estimators=10, random_state=42)

    def fit(self, X_train, y_train):
        """
        Train the model using Scikit-learn's RandomForestClassifier.

        Args:
            X_train (np.ndarray): Training images (N, 28, 28)
            y_train (np.ndarray): Training labels (N,)
        """
        # Flatten images from (N, 28, 28) to (N, 784) for sklearn
        X_train_flat = X_train.reshape(X_train.shape[0], -1)
        
        print(f"[*] Training RandomForestClassifier on {X_train_flat.shape[0]} samples...")
        self.clf.fit(X_train_flat, y_train)
        print("[+] Training complete.")

    def predict(self, X_test):
        """
        Predict labels for the test set using the trained classifier.
        
        Args:
            X_test (np.ndarray): Test images (M, 28, 28)
            
        Returns:
            np.ndarray: Predicted labels (M,)
        """
        # Flatten images from (M, 28, 28) to (M, 784) for sklearn
        X_test_flat = X_test.reshape(X_test.shape[0], -1)
        
        print(f"[*] Predicting labels for {X_test_flat.shape[0]} test samples...")
        return self.clf.predict(X_test_flat)
