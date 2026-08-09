import os
import joblib


# -----------------------------
# Project paths
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "src",
    "ml",
    "model.pkl"
)


# -----------------------------
# Load trained model
# -----------------------------

if not os.path.exists(MODEL_FILE):
    raise FileNotFoundError(
        "model.pkl not found. "
        "Please run train.py first."
    )

model = joblib.load(MODEL_FILE)


# -----------------------------
# Risk prediction function
# -----------------------------

def predict_risk(
    activity="",
    location_type="",
    description="",
    event_type="",
    environmental_factor="",
    human_factor=""
):
    """
    Predict risk for a construction incident/activity.
    """

    text = " ".join([
        str(activity),
        str(location_type),
        str(description),
        str(event_type),
        str(environmental_factor),
        str(human_factor)
    ])

    # Prediction
    prediction = model.predict([text])[0]

    # Probability
    probabilities = model.predict_proba([text])[0]

    classes = model.classes_

    probability_dict = {
        class_name: round(float(probability), 4)
        for class_name, probability
        in zip(classes, probabilities)
    }

    return {
        "risk_level": prediction,
        "probabilities": probability_dict
    }


# -----------------------------
# Test prediction
# -----------------------------

if __name__ == "__main__":

    result = predict_risk(
        activity="Working at height",
        location_type="Building construction",
        description=(
            "Employee is working on a roof "
            "near an unprotected edge."
        ),
        event_type="Fall",
        environmental_factor="Unprotected edge",
        human_factor="Unsafe work practice"
    )

    print("\nRisk Prediction")
    print("----------------")
    print("Risk Level:", result["risk_level"])

    print("\nProbabilities:")

    for risk, probability in result["probabilities"].items():
        print(
            f"{risk}: "
            f"{probability * 100:.2f}%"
        )