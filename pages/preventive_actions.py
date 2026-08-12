import streamlit as st
import pandas as pd

from src.recommendations.safety_rules import (
    SAFETY_RULES,
    get_recommendation
)


# ------------------------------------
# Page Title
# ------------------------------------

st.title("🛡️ Preventive Actions")

st.write(
    "Select a hazard or construction activity to view "
    "the corresponding risk level, toolbox talk topic, "
    "and standard preventive controls."
)


# ------------------------------------
# Load Dataset
# ------------------------------------

try:

    df = pd.read_csv(
        "data/processed/incidents.csv"
    )

except Exception as e:

    st.error(
        f"Could not load incidents: {e}"
    )

    st.stop()


# ------------------------------------
# Historical Event Types
# ------------------------------------

historical_events = []

if "event_type" in df.columns:

    historical_events = (
        df["event_type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


# ------------------------------------
# Combine Dataset Events + Safety Rules
# ------------------------------------

available_options = sorted(
    set(historical_events) |
    set(SAFETY_RULES.keys())
)


# ------------------------------------
# Event Selection
# ------------------------------------

selected_event = st.selectbox(
    "Select a hazard / event / construction activity",
    available_options
)


# ------------------------------------
# Show Preventive Actions
# ------------------------------------

if st.button(
    "Show Preventive Actions",
    type="primary"
):

    recommendation = get_recommendation(
        selected_event
    )

    st.divider()

    # --------------------------------
    # Risk Level
    # --------------------------------

    risk = recommendation["risk"]

    if risk == "HIGH":

        st.error(
            f"🔴 Risk Level: {risk}"
        )

    elif risk == "MEDIUM":

        st.warning(
            f"🟠 Risk Level: {risk}"
        )

    else:

        st.info(
            f"🟢 Risk Level: {risk}"
        )


    # --------------------------------
    # Toolbox Talk
    # --------------------------------

    st.subheader(
        "🗣️ Toolbox Talk"
    )

    st.write(
        recommendation["toolbox"]
    )


    # --------------------------------
    # Recommended Controls
    # --------------------------------

    st.subheader(
        "✅ Recommended Preventive Controls"
    )

    for action in recommendation["actions"]:

        st.write(
            f"• {action}"
        )


    # --------------------------------
    # Historical Evidence
    # --------------------------------

    if "event_type" in df.columns:

        matching_incidents = df[
            df["event_type"]
            .astype(str)
            .str.lower()
            ==
            selected_event.lower()
        ]

        if len(matching_incidents) > 0:

            st.subheader(
                "📊 Historical Evidence"
            )

            st.metric(
                "Matching Historical Incidents",
                len(matching_incidents)
            )


    # --------------------------------
    # Safety Disclaimer
    # --------------------------------

    st.info(
        "Recommendations focus on standard safe practices "
        "and hazard controls rather than worker blame."
    )