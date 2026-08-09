import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# -----------------------------
# Project paths
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "incidents.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "src",
    "ml",
    "model.pkl"
)


# -----------------------------
# Load and prepare data
# -----------------------------

def load_data():

    df = pd.read_csv(DATA_FILE)

    feature_columns = [
        "activity",
        "location_type",
        "description",
        "event_type",
        "environmental_factor",
        "human_factor"
    ]

    for column in feature_columns:

        if column not in df.columns:
            df[column] = ""

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
        )

    # Combine all features
    df["text"] = df[feature_columns].agg(
        " ".join,
        axis=1
    )

    # Create the same labels used in train.py
    df["severity"] = (
        df["severity"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["risk_level"] = df["severity"].map({
        "fatal": "HIGH",
        "nonfatal": "NON-HIGH"
    })

    df = df.dropna(
        subset=["risk_level"]
    )

    return df


# -----------------------------
# Evaluate model
# -----------------------------

def evaluate_model():

    print("Loading dataset...")

    df = load_data()

    X = df["text"]
    y = df["risk_level"]

    print("\nDataset size:", len(df))

    print("\nRisk distribution:")
    print(y.value_counts())

    # Same split used during training
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # Load trained model
    print("\nLoading trained model...")

    model = joblib.load(MODEL_FILE)

    # Predict test data
    predictions = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\n==============================")
    print("       MODEL EVALUATION")
    print("==============================")

    print(
        f"\nAccuracy: {accuracy:.4f}"
    )

    print(
        f"Accuracy percentage: {accuracy * 100:.2f}%"
    )

    # Classification report
    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions
        )
    )

    # Confusion matrix
    print("Confusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    evaluate_model()