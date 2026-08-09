import streamlit as st
import pandas as pd

from src.recommendations.safety_rules import (
    get_recommendation
)


st.title("🛡️ Preventive Actions")

try:

    df = pd.read_csv(
        "data/processed/incidents.csv"
    )

except Exception as e:

    st.error(
        f"Could not load incidents: {e}"
    )

    st.stop()


if "event_type" not in df.columns:

    st.warning(
        "The dataset does not contain an event_type column."
    )

    st.stop()


event_types = (
    df["event_type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

event_types.sort()


selected_event = st.selectbox(
    "Select a hazard/event type",
    event_types
)


if st.button(
    "Show Preventive Actions",
    type="primary"
):

    recommendation = get_recommendation(
        selected_event
    )

    st.subheader(
        f"Risk Level: {recommendation['risk']}"
    )

    st.write(
        f"### Toolbox Talk: "
        f"{recommendation['toolbox']}"
    )

    st.write("### Recommended Controls")

    for action in recommendation["actions"]:

        st.write(
            f"✅ {action}"
        )

    st.info(
        "Recommendations focus on standard safe practices "
        "and hazard controls rather than worker blame."
    )