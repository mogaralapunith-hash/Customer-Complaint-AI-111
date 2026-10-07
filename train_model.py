import os
import pickle
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


# -----------------------------------------
# PROJECT PATH
# -----------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# -----------------------------------------
# DATASET PATH
# -----------------------------------------

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "complaints.csv"
)


# -----------------------------------------
# MODEL FOLDER
# -----------------------------------------

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

os.makedirs(MODEL_DIR, exist_ok=True)


# -----------------------------------------
# LOAD DATASET
# -----------------------------------------

data = pd.read_csv(DATASET_PATH)


# -----------------------------------------
# CHECK DATA
# -----------------------------------------

print("Dataset loaded successfully!")

print("Number of complaints:", len(data))

print("Columns:", list(data.columns))


# -----------------------------------------
# REMOVE EMPTY VALUES
# -----------------------------------------

data = data.dropna(
    subset=["complaint", "category"]
)


# -----------------------------------------
# INPUT AND OUTPUT
# -----------------------------------------

X = data["complaint"].astype(str)

y = data["category"].astype(str)


# -----------------------------------------
# CREATE MACHINE LEARNING PIPELINE
# -----------------------------------------

model = Pipeline([

    (
        "vectorizer",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 3),
            sublinear_tf=True
        )
    ),

    (
        "classifier",
        LinearSVC()
    )

])


# -----------------------------------------
# TRAIN MODEL
# -----------------------------------------

print("Training Customer Complaint AI...")

model.fit(X, y)


# -----------------------------------------
# SAVE MODEL
# -----------------------------------------

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "classifier.pkl"
)

with open(
    MODEL_PATH,
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


# -----------------------------------------
# SUCCESS
# -----------------------------------------

print()
print("===================================")
print(" CUSTOMER COMPLAINT AI")
print("===================================")

print("Training completed successfully!")

print("Total training examples:", len(data))

print(
    "Categories:",
    sorted(y.unique())
)

print(
    "Model saved at:",
    MODEL_PATH
)

print("===================================")