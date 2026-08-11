import os
from datetime import date

import pandas as pd
import streamlit as st

from src.ml.predict import predict_risk


WEEKLY_FILE = "data/processed/weekly_inputs.csv"


# ============================================================
# PAGE
# ============================================================

st.title("🎯 Risk Prediction")

st.write(
    "Enter the current construction activity information. "
    "When you predict the risk, the same input is automatically "
    "recorded for the Weekly Safety Brief."
)


# ============================================================
# DROPDOWN OPTIONS
# ============================================================

ACTIVITIES = [
    "Not Regularly Assigned",
    "Regularly Assigned",
]

LOCATIONS = [
    "Bridge",
    "Commercial building",
    "Contractor's yard/facility",
    "Excavation, landfill",
    "Highway, road, street",
    "Manufacturing plant",
    "Multi-family dwelling",
    "Other building",
    "Other heavy construction",
]

HAZARD_EVENT_TYPES = [
    "Absorption",
    "Bite/sting/scratch",
    "Card-vascular/resp. fail.",
    "Caught in or between",
    "Fall (from elevation)",
    "Fall (same level)",
    "Ingestion",
    "Inhalation",
    "Other",
    "Rep. Motion/pressure",
    "Rubbed/abraded",
    "Shock",
    "Struck against",
    "Struck-by",
]

ENVIRONMENTAL_FACTORS = [
    "Catch Point/Puncture Action",
    "Chemical Action/Reaction Expos",
    "Flammable Liquid/Solid Exposure",
    "Flying Object Action",
    "Gas/Vapor/Mist/Fume/Smoke/Dust",
    "Illumination",
    "Materials Handling Equip./Method",
    "Other",
    "Overhead Moving/Falling Object Action",
    "Overpressure/Underpressure",
    "Pinch Point Action",
    "Radiation Condition",
    "Shear Point Action",
    "Sound Level",
    "Temperature +/- Tolerance Lev.",
    "Weather, Earthquake, Etc.",
    "Work-Surface/Facility-Layout Condition",
]

HUMAN_FACTORS = [
    "Defective Equipment In Use",
    "Distracting Actions By Others",
    "Equipment Inappropriate For Operation",
    "Insufficient /Lack/Engineering Controls",
    "Insufficient /Lack/Expose/Biological Monitoring.",
    "Insufficient /Lack/Protective Work Clothing/Equipment",
    "Insufficient /Lack/Respiratory Protection",
    "Insufficient /Lack/Written Work Practice Program",
    "Insufficient/Lack/Housekeeping Program",
    "Lockout/Tagout Procedure Malfunction",
    "Malfunction In Securing/Warning Op",
    "Malfunction Neuromuscular System",
    "Mater-Handling Procedure Inappropriate",
    "Misjudgment, Hazardous Situation",
    "Other",
    "Perception Malfunction Task-Environment",
    "Position Inappropriate For Task",
    "Safety Devices Removed/Inoperable",
]


# ============================================================
# INPUT FORM
# ============================================================

with st.form("risk_prediction_form"):

    st.subheader("Construction Activity Information")

    input_date = st.date_input(
        "Date",
        value=date.today()
    )

    activity = st.selectbox(
        "Activity",
        ACTIVITIES,
        index=None,
        placeholder="Select activity..."
    )

    location = st.selectbox(
        "Location",
        LOCATIONS,
        index=None,
        placeholder="Select location..."
    )

    event_type = st.selectbox(
        "Hazard / Event Type",
        HAZARD_EVENT_TYPES,
        index=None,
        placeholder="Select hazard/event..."
    )

    environmental_factor = st.selectbox(
        "Environmental Factor",
        ENVIRONMENTAL_FACTORS,
        index=None,
        placeholder="Select environmental factor..."
    )

    human_factor = st.selectbox(
        "Human Factor",
        HUMAN_FACTORS,
        index=None,
        placeholder="Select human factor..."
    )

    description = st.text_area(
        "Description",
        placeholder="Describe the activity or safety observation...",
        height=120
    )

    submitted = st.form_submit_button(
        "🔍 Predict Risk",
        type="primary"
    )


# ============================================================
# VALIDATE + PREDICT + SAVE
# ============================================================

if submitted:

    missing = []

    if not activity:
        missing.append("Activity")

    if not location:
        missing.append("Location")

    if not event_type:
        missing.append("Hazard / Event Type")

    if not environmental_factor:
        missing.append("Environmental Factor")

    if not human_factor:
        missing.append("Human Factor")

    if missing:

        st.error(
            "Please select: " + ", ".join(missing)
        )

        st.stop()


    # --------------------------------------------------------
    # Prepare data for ML model
    # --------------------------------------------------------

    input_data = pd.DataFrame([
        {
            "activity": activity,
            "location_type": location,
            "event_type": event_type,
            "environmental_factor": environmental_factor,
            "human_factor": human_factor,
            "description": description,
        }
    ])


    # --------------------------------------------------------
    # Run ML prediction
    # --------------------------------------------------------

    try:

        with st.spinner("Analyzing safety risk..."):

            risk_result = predict_risk(
                input_data
            )

    except Exception as e:

        st.error(
            f"Risk prediction failed: {e}"
        )

        st.stop()


    # --------------------------------------------------------
    # Display prediction
    # --------------------------------------------------------

    st.divider()

    st.subheader("Risk Prediction")

    st.success(
        f"Predicted Risk: **{risk_result}**"
    )


    # --------------------------------------------------------
    # Save automatically for Weekly Safety Brief
    # --------------------------------------------------------

    try:

        os.makedirs(
            os.path.dirname(WEEKLY_FILE),
            exist_ok=True
        )


        # Existing weekly data
        if os.path.exists(WEEKLY_FILE) and os.path.getsize(WEEKLY_FILE) > 0:
            weekly_df = pd.read_csv(WEEKLY_FILE)
        else:
            weekly_df = pd.DataFrame()
        # New record
        new_record = pd.DataFrame([
            {
                "date": input_date.isoformat(),
                "activity": activity,
                "location_type": location,
                "event_type": event_type,
                "environmental_factor": environmental_factor,
                "human_factor": human_factor,
                "description": description,
                "risk_level": risk_result,
            }
        ])


        # Append
        weekly_df = pd.concat(
            [
                weekly_df,
                new_record
            ],
            ignore_index=True
        )


        # Save
        weekly_df.to_csv(
            WEEKLY_FILE,
            index=False
        )


        st.info(
            "✅ This prediction has also been recorded "
            "for the Weekly Safety Brief."
        )


    except Exception as e:

        st.warning(
            f"Risk prediction succeeded, but weekly "
            f"record could not be saved: {e}"
        )