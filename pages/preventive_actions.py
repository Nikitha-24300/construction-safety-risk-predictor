"""Preventive Actions — hazard → risk → control."""

from __future__ import annotations

import streamlit as st

from utils.recommendations import get_controls, get_hazards, get_toolbox_talk
from utils.ui import ACTIVITIES, RISK_BG, RISK_COLORS, page_header, risk_pill

page_header(
    "Preventive Actions",
    "Standard preventive controls framed as hazard → risk → control",
)

last = st.session_state.get("last_prediction")

source = st.radio(
    "Source",
    ["Select an activity", "Use latest prediction"],
    horizontal=True,
    index=1 if last else 0,
    disabled=last is None,
)

if source == "Use latest prediction" and last:
    activity = last["activity"]
    level = last["risk_level"]
    score = last["risk_score"]
else:
    activity = st.selectbox("Activity", ACTIVITIES)
    level, score = None, None

st.write("")
header = f"### {activity}"
if level:
    st.markdown(
        f"<div class='csrp-risk' style='background:{RISK_BG[level]};border-color:{RISK_COLORS[level]}'>"
        f"<div class='lvl' style='color:{RISK_COLORS[level]};font-size:1.4rem'>{activity} — {level} RISK</div>"
        f"<div class='scr'>Model risk score: {score * 100:.0f}%</div></div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(header)

c1, c2 = st.columns([1, 1.3])
with c1:
    st.markdown("<div class='csrp-section'>Detected hazards</div>", unsafe_allow_html=True)
    for h in get_hazards(activity):
        st.markdown(f"- {h}")
with c2:
    st.markdown("<div class='csrp-section'>Recommended controls</div>", unsafe_allow_html=True)
    for c in get_controls(activity):
        st.markdown(f"✓ {c}")

talk = get_toolbox_talk(activity)
st.markdown("<div class='csrp-section'>Toolbox talk</div>", unsafe_allow_html=True)
with st.expander(f"Toolbox Talk: {talk['topic']}", expanded=True):
    st.markdown(f"**Why it matters** — {talk['why']}")
    st.markdown("**Key discussion points**")
    for p in talk["points"]:
        st.markdown(f"- {p}")

st.divider()
st.markdown("<div class='csrp-section'>All activities at a glance</div>", unsafe_allow_html=True)
for act in ACTIVITIES:
    if act == "Other":
        continue
    with st.expander(f"{act} — {get_toolbox_talk(act)['topic']}"):
        st.markdown("**Hazards:** " + ", ".join(get_hazards(act)))
        for c in get_controls(act):
            st.markdown(f"✓ {c}")

st.caption(
    "Recommendations address hazards, conditions and controls. They never assign fault "
    "to individuals and contain standard safe practices only."
)
st.markdown(risk_pill("LOW") + " " + risk_pill("MEDIUM") + " " + risk_pill("HIGH"),
            unsafe_allow_html=True)
