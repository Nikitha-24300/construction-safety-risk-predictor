import pandas as pd
import os


# -----------------------------
# File paths
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "OSHA HSE DATA_ALL ABSTRACTS 15-17_FINAL.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "incidents.csv"
)


# -----------------------------
# Load dataset
# -----------------------------

def load_data():
    df = pd.read_csv(INPUT_FILE)

    print("Dataset loaded successfully")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    return df


# -----------------------------
# Clean text
# -----------------------------

def clean_text(value):
    if pd.isna(value):
        return ""

    return str(value).strip()


# -----------------------------
# Preprocess dataset
# -----------------------------

def preprocess_data(df):

    # Remove completely empty rows
    df = df.dropna(how="all").copy()

    # Clean important text fields
    text_columns = [
        "Abstract Text",
        "Event Description",
        "Event Keywords",
        "Task Assigned",
        "Degree of Injury",
        "Event type",
        "Environmental Factor",
        "Human Factor",
        "Nature of Injury",
        "Construction End Use",
        "Project Type"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].apply(clean_text)

    # Convert date
    df["Event Date"] = pd.to_datetime(
        df["Event Date"],
        errors="coerce"
    )

    # Create standardized project columns
    processed = pd.DataFrame()

    # Activity
    processed["activity"] = df["Task Assigned"]

    # Location/context
    processed["location_type"] = df["Construction End Use"]

    # Time
    processed["time"] = df["Event Date"]

    # Incident description
    processed["description"] = df["Abstract Text"]

    # Severity
    processed["severity"] = df["Degree of Injury"]

    # Additional useful information
    processed["event_type"] = df["Event type"]

    processed["environmental_factor"] = df[
        "Environmental Factor"
    ]

    processed["human_factor"] = df[
        "Human Factor"
    ]

    processed["nature_of_injury"] = df[
        "Nature of Injury"
    ]

    processed["part_of_body"] = df[
        "Part of Body"
    ]

    processed["construction_type"] = df[
        "Construction End Use"
    ]

    processed["project_type"] = df[
        "Project Type"
    ]

    processed["event_keywords"] = df[
        "Event Keywords"
    ]

    processed["fall_height"] = df[
        "fall_ht"
    ]

    # Remove rows where there is no description
    processed = processed[
        processed["description"].str.strip() != ""
    ]

    # Fill missing categorical/text values
    text_columns_processed = [
        "activity",
        "location_type",
        "severity",
        "event_type",
        "environmental_factor",
        "human_factor",
        "nature_of_injury",
        "part_of_body",
        "construction_type",
        "project_type",
        "event_keywords"
    ]

    for column in text_columns_processed:
        processed[column] = processed[column].fillna("Unknown")

    return processed


# -----------------------------
# Save processed dataset
# -----------------------------

def save_data(df):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nProcessed dataset saved to:")
    print(OUTPUT_FILE)

    print("\nFinal shape:")
    print(df.shape)


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    df = load_data()

    processed_df = preprocess_data(df)

    save_data(processed_df)

    print("\nPreprocessing completed successfully!")