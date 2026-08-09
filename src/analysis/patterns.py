
import os
import pandas as pd

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

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

# -----------------------------
# Load dataset
# -----------------------------

def load_data():
    df = pd.read_csv(DATA_FILE)
    return df

# -----------------------------
# Analyze patterns
# -----------------------------

def analyze_patterns(df):

    print("\n========== CONSTRUCTION SAFETY ANALYSIS ==========\n")

    # 1. Top activities
    activity = (
        df["activity"]
        .value_counts()
        .head(10)
    )

    print("Top 10 Risk Activities\n")
    print(activity)

    # 2. Event types
    events = (
        df["event_type"]
        .value_counts()
        .head(10)
    )

    print("\nTop Event Types\n")
    print(events)

    # 3. Environmental factors
    env = (
        df["environmental_factor"]
        .value_counts()
        .head(10)
    )

    print("\nTop Environmental Factors\n")
    print(env)

    # 4. Human factors
    human = (
        df["human_factor"]
        .value_counts()
        .head(10)
    )

    print("\nTop Human Factors\n")
    print(human)

    # 5. Construction type
    construction = (
        df["construction_type"]
        .value_counts()
        .head(10)
    )

    print("\nTop Construction Types\n")
    print(construction)

    return {
        "activity": activity,
        "events": events,
        "environment": env,
        "human": human,
        "construction": construction
    }

# -----------------------------
# Save summaries
# -----------------------------

def save_summary(results):

    summary = pd.DataFrame({
        "Top Activities": results["activity"].index,
        "Activity Count": results["activity"].values
    })

    output_file = os.path.join(
        OUTPUT_DIR,
        "pattern_summary.csv"
    )

    summary.to_csv(
        output_file,
        index=False
    )

    print("\nSummary saved to:")
    print(output_file)

# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    df = load_data()

    results = analyze_patterns(df)

    save_summary(results)