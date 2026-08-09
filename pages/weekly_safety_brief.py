"""Weekly Safety Brief — Azure OpenAI generated summary."""

from __future__ import annotations

import json

import streamlit as st

from azure_integration.brief_generator import (
    BriefGenerationError,
    generate_weekly_brief,
    is_configured,
)
from utils.data_loader import load_incidents
from utils.summary import build_summary
from utils.ui import page_header

page_header(
    "Weekly Safety Brief",
    "A professional brief generated from the model and dataset results only",
)

df, demo = load_incidents()
if demo:
    st.warning("Demo Mode — brief is based on synthetic demonstration data.", icon="⚠️")

if not is_configured():
    st.info(
        "Azure OpenAI is not configured. The brief will be produced offline directly from "
        "the structured results. Add your Azure settings to Streamlit secrets to enable "
        "AI-written narrative.",
        icon="ℹ️",
    )

summary = build_summary(df, demo)

with st.expander("Structured data sent to the model", expanded=False):
    st.caption(
        "Only aggregated results are shared. The model is instructed to use these figures "
        "verbatim and never to invent statistics."
    )
    st.code(json.dumps(summary, indent=2, default=str), language="json")

if st.button("Generate Weekly Safety Brief", type="primary"):
    with st.spinner("Preparing the weekly safety brief..."):
        try:
            brief, source = generate_weekly_brief(summary)
            st.session_state["weekly_brief"] = brief
            st.session_state["weekly_brief_source"] = source
        except BriefGenerationError as exc:
            st.error(str(exc))
        except Exception:  # noqa: BLE001
            st.error("The brief could not be generated right now. Please try again later.")

brief = st.session_state.get("weekly_brief")
if brief:
    source = st.session_state.get("weekly_brief_source")
    if source == "offline":
        st.caption("Generated offline from structured results (Azure OpenAI unavailable).")
    else:
        st.caption("Generated with Azure OpenAI from the structured results above.")
    st.markdown(brief)
    st.download_button(
        "Download brief (Markdown)",
        brief,
        file_name="weekly_safety_brief.md",
        mime="text/markdown",
    )
else:
    st.caption(
        "The brief covers: Weekly Safety Overview, Key High-Risk Activities, Recurring "
        "Hazards, Priority Preventive Controls, Recommended Toolbox Talks and Management "
        "Attention Items."
    )
