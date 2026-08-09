import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# Project root
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


def load_data():

    df = pd.read_csv(DATA_FILE)

    print("Dataset loaded successfully.")
    print("Dataset shape:", df.shape)

    return df


def prepare_data(df):

    feature_columns = [
        "activity",
        "location_type",
        "description",
        "event_type",
        "environmental_factor",
        "human_factor"
    ]

    # Make sure all feature columns exist
    for column in feature_columns:

        if column not in df.columns:
            df[column] = ""

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
        )

    # Combine structured + text information
    df["text"] = df[feature_columns].agg(
        " ".join,
        axis=1
    )

    # Clean severity
    df["severity"] = (
        df["severity"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Create risk label from actual OSHA severity
    df["risk_level"] = df["severity"].map({
        "fatal": "HIGH",
        "nonfatal": "NON-HIGH"
    })

    # Remove unexpected severity values
    df = df.dropna(subset=["risk_level"])

    return df


def train_model(df):

    X = df["text"]
    y = df["risk_level"]

    print("\nRisk distribution:")
    print(y.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                max_features=10000
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ])

    print("\nTraining model...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nModel Evaluation")
    print("----------------")

    print(
        "Accuracy:",
        round(accuracy_score(y_test, predictions), 4)
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions
        )
    )

    print("\nConfusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )

    return model


def main():

    df = load_data()

    df = prepare_data(df)

    model = train_model(df)

    joblib.dump(
        model,
        MODEL_FILE
    )

    print("\nModel saved successfully:")
    print(MODEL_FILE)


if __name__ == "__main__":
    main()