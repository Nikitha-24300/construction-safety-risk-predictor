import streamlit as st
import pandas as pd

from src.ml.predict import predict_risk


st.title("🎯 Risk Prediction")

st.write(
    "Enter the context of a construction activity "
    "to estimate its safety risk."
)


try:
    df = pd.read_csv(
        "data/processed/incidents.csv"
    )
except Exception as e:
    st.error(f"Could not load dataset: {e}")
    st.stop()


# ---------------------------------------
# Build input fields from dataset
# ---------------------------------------

def get_options(column):

    if column not in df.columns:
        return ["Unknown"]

    values = (
        df[column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    values.sort()

    return values if values else ["Unknown"]


activity = st.selectbox(
    "Activity",
    get_options("activity")
)

location = st.selectbox(
    "Location Type",
    get_options("location_type")
)

event_type = st.selectbox(
    "Event Type",
    get_options("event_type")
)

environment = st.selectbox(
    "Environmental Factor",
    get_options("environmental_factor")
)

human_factor = st.selectbox(
    "Human Factor",
    get_options("human_factor")
)


if st.button("Predict Risk", type="primary"):

    input_data = pd.DataFrame(
        [{
            "activity": activity,
            "location_type": location,
            "event_type": event_type,
            "environmental_factor": environment,
            "human_factor": human_factor
        }]
    )

    try:

        result = predict_risk(input_data)

        st.subheader("Prediction")

        st.success(
            f"Predicted Risk: **{result}**"
        )

    except Exception as e:

        st.error(
            f"Prediction failed: {e}"
        )