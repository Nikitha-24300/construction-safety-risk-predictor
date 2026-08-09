"""Planned Activities — evaluate today's plan against historical risk patterns."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ml.predict import predict_batch
from utils.data_loader import load_planned_activities
from utils.recommendations import get_toolbox_talk
from utils.ui import RISK_BG, RISK_COLORS, page_header

page_header(
    "Planned Activities",
    "Score daily planned activities against historical incident patterns",
)

planned, demo = load_planned_activities()
if demo:
    st.warning("Demo Mode — using synthetic demonstration activities.", icon="⚠️")

uploaded = st.file_uploader(
    "Upload planned activities (CSV)",
    type="csv",
    help="Expected columns: activity, location_type, shift, description, planned_date. "
         "Do not include worker names or IDs.",
)
if uploaded is not None:
    try:
        planned = pd.read_csv(uploaded)
        if "activity" not in planned.columns:
            raise ValueError("missing activity column")
        st.success(f"Loaded {len(planned)} planned activities.")
    except Exception:  # noqa: BLE001
        st.error(
            "That file could not be read. Please upload a CSV containing at least an "
            "'activity' column."
        )
        planned, _ = load_planned_activities()

if planned.empty:
    st.info("No planned activities available.")
    st.stop()

results = predict_batch(planned.to_dict("records"))
view = planned.copy()
view["Risk"] = [r["risk_level"] for r in results]
view["Score"] = [f"{r['risk_score'] * 100:.0f}%" for r in results]

st.markdown("<div class='csrp-section'>Today's planned activities</div>", unsafe_allow_html=True)
table = view.rename(
    columns={"activity": "Activity", "location_type": "Location", "shift": "Shift"}
)
cols = [c for c in ["Activity", "Location", "Shift", "Risk", "Score"] if c in table]
st.dataframe(table[cols], use_container_width=True, hide_index=True)

labels = [
    f"{row['activity']} · {row.get('location_type', '')} — {results[i]['risk_level']}"
    for i, row in enumerate(planned.to_dict("records"))
]
choice = st.selectbox("Select an activity for detail", range(len(labels)),
                      format_func=lambda i: labels[i])

record = planned.to_dict("records")[choice]
res = results[choice]
level = res["risk_level"]

st.markdown(
    f"<div class='csrp-risk' style='background:{RISK_BG[level]};border-color:{RISK_COLORS[level]}'>"
    f"<div class='lvl' style='color:{RISK_COLORS[level]};font-size:1.5rem'>{level} RISK</div>"
    f"<div class='scr'>Model risk score: {res['risk_score'] * 100:.0f}% · "
    f"{record.get('activity')} · {record.get('location_type', 'n/a')} · "
    f"{record.get('shift', 'n/a')} shift</div></div>",
    unsafe_allow_html=True,
)
st.caption(record.get("description", ""))

c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='csrp-section'>Contributing factors</div>", unsafe_allow_html=True)
    for f in res["contributing_factors"]:
        st.markdown(f"- {f}")
with c2:
    st.markdown("<div class='csrp-section'>Recurring patterns</div>", unsafe_allow_html=True)
    for p in res["recurring_patterns"]:
        st.markdown(f"- {p}")

st.markdown("<div class='csrp-section'>Preventive controls</div>", unsafe_allow_html=True)
for r in res["recommendations"]:
    st.markdown(f"✓ {r}")

talk = get_toolbox_talk(record.get("activity", "Other"))
with st.expander(f"Toolbox Talk: {talk['topic']}"):
    st.markdown(f"**Why it matters** — {talk['why']}")
    for p in talk["points"]:
        st.markdown(f"- {p}")

if st.button("Open in Risk Prediction", type="secondary"):
    st.session_state["prefill"] = {
        "activity": record.get("activity"),
        "location_type": record.get("location_type"),
        "shift": record.get("shift"),
        "description": record.get("description", ""),
    }
    st.switch_page("pages/risk_prediction.py")
