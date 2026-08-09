"""Risk Prediction — core interactive page."""

from __future__ import annotations

import streamlit as st

from ml.predict import predict_risk
from utils.recommendations import get_toolbox_talk
from utils.ui import (
    ACTIVITIES,
    DISCLAIMER,
    LOCATIONS,
    PPE_OPTIONS,
    RISK_BG,
    RISK_COLORS,
    SHIFTS,
    page_header,
)

page_header(
    "Risk Prediction",
    "Assess a planned activity against historical incident patterns before work starts",
)
st.info(DISCLAIMER, icon="ℹ️")

prefill = st.session_state.get("prefill", {})

with st.form("risk_form"):
    c1, c2, c3 = st.columns(3)
    activity = c1.selectbox(
        "Activity",
        ACTIVITIES,
        index=ACTIVITIES.index(prefill["activity"]) if prefill.get("activity") in ACTIVITIES else 0,
    )
    location = c2.selectbox(
        "Location type",
        LOCATIONS,
        index=LOCATIONS.index(prefill["location_type"]) if prefill.get("location_type") in LOCATIONS else 0,
    )
    shift = c3.selectbox(
        "Shift / time",
        SHIFTS,
        index=SHIFTS.index(prefill["shift"]) if prefill.get("shift") in SHIFTS else 0,
    )
    description = st.text_area(
        "Description",
        value=prefill.get("description", ""),
        height=140,
        placeholder="Describe the planned activity, working conditions, hazards, or relevant context.",
        help="Do not include worker names or ID numbers. Describe conditions and hazards only.",
    )
    ppe = st.selectbox("PPE compliance (optional)", PPE_OPTIONS, index=0)
    submitted = st.form_submit_button("Predict Risk", type="primary", use_container_width=True)

if submitted:
    if not description.strip():
        st.error("Please add a short description of the activity and conditions before predicting.")
    else:
        try:
            result = predict_risk(
                activity, location, shift, description,
                None if ppe == "Unknown" else ppe,
            )
            st.session_state["last_prediction"] = {**result, "activity": activity,
                                                   "location": location, "shift": shift}
        except ValueError as exc:
            st.error(str(exc))
        except Exception:  # noqa: BLE001
            st.error("The prediction service is temporarily unavailable. Please try again.")

result = st.session_state.get("last_prediction")
if result:
    level = result["risk_level"]
    st.write("")
    st.markdown("<div class='csrp-section'>Risk assessment</div>", unsafe_allow_html=True)
    if result.get("demo_mode"):
        st.warning(
            "Demo Mode — synthetic demonstration prediction, not a real-world model output.",
            icon="⚠️",
        )
    st.markdown(
        f"<div class='csrp-risk' style='background:{RISK_BG[level]};border-color:{RISK_COLORS[level]}'>"
        f"<div class='lvl' style='color:{RISK_COLORS[level]}'>{level} RISK</div>"
        f"<div class='scr'>Model risk score: {result['risk_score'] * 100:.0f}% "
        f"&nbsp;·&nbsp; {result['activity']} · {result['location']} · {result['shift']} shift</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.caption(
        "The risk score is a model prediction based on historical patterns. It is not a "
        "guarantee of safety and does not replace site risk assessment."
    )

    a, b = st.columns(2)
    with a:
        st.markdown("<div class='csrp-section'>Top contributing factors</div>", unsafe_allow_html=True)
        for f in result["contributing_factors"]:
            st.markdown(f"- {f}")
    with b:
        st.markdown("<div class='csrp-section'>Recurring patterns</div>", unsafe_allow_html=True)