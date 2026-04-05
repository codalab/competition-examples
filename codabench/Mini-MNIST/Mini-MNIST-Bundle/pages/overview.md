# 🏆 Mini-MNIST Digit Classification Challenge

Welcome to the **Mini-MNIST Challenge!** This is a streamlined, lightweight version of the classic MNIST benchmark. 

Whether you are a beginner experimenting with your first computer vision models or an expert trying to squeeze maximum accuracy out of a tiny dataset, this challenge is designed to be accessible, fast, and fun!

---

## 🎯 Challenge Objective
The goal is simple: classify handwritten digits from **0 to 9**. 

However, there's a twist! Unlike the standard MNIST dataset which provides 60,000 training images, you are faced with a **few-shot learning** scenario. You will only have access to a severely restricted number of training samples. Your algorithm must learn generalized features from minimal data.

---

## 📊 Dataset Constraints
We have curated a perfectly balanced mini-dataset. While the backend handles images natively as PNGs formats, the ingestion system automatically loads them as NumPy arrays for your model:

*   **Training Set:** Exactly **200 images** (20 images per digit).
*   **Test Set:** Exactly **50 images** (5 images per digit) kept hidden for final scoring.
*   **Image Format:** The ingestion program passes the data to your model as `(28, 28)` grayscale NumPy arrays

---

## 💻 How to Participate
* Register to the competition
* Follow the instructions below:

### 1. Build Your Model
Create a single Python file named `model.py`. Inside this file, implement a `Model` class with two required methods:

```python
class Model:
    def __init__(self):
        # Initialize your classifier here
        pass

    def fit(self, X_train, y_train):
        # X_train shape: (N, 28, 28)
        # y_train shape: (N,)
        pass

    def predict(self, X_test):
        # X_test shape: (M, 28, 28)
        # return prediction array of shape (M,)
        pass
```

### 2. Submit to Codabench
Once your script is ready:
1. Zip your `model.py` file into a `.zip` archive.
2. Navigate to the **My Submissions** tab.
3. Upload your archive and watch your score appear on the leaderboard!
