"""Application entry point.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.predict import is_demo_mode  # noqa: E402
from utils.data_loader import load_incidents  # noqa: E402
from utils.ui import APP_TITLE, PRIVACY_NOTE, inject_css  # noqa: E402

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🦺",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

_, data_is_demo = load_incidents()
model_is_demo = is_demo_mode()

with st.sidebar:
    st.markdown("### 🦺 Safety Risk Predictor")
    st.caption("Construction safety decision support")

if model_is_demo or data_is_demo:
    with st.sidebar:
        st.warning(
            "**Demo Mode**\n\nUsing synthetic demonstration data"
            + (" and heuristic predictions." if model_is_demo else ".")
            + " Results are illustrative only.",
            icon="⚠️",
        )

pages = [
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊", default=True),
    st.Page("pages/risk_prediction.py", title="Risk Prediction", icon="🎯"),
    st.Page("pages/planned_activities.py", title="Planned Activities", icon="🗓️"),
    st.Page("pages/risk_patterns.py", title="Risk Patterns", icon="📈"),
    st.Page("pages/preventive_actions.py", title="Preventive Actions", icon="🛡️"),
    st.Page("pages/weekly_safety_brief.py", title="Weekly Safety Brief", icon="📝"),
    st.Page("pages/about.py", title="About / Model Info", icon="ℹ️"),
]

nav = st.navigation(pages)

with st.sidebar:
    st.divider()
    st.caption(PRIVACY_NOTE)

nav.run()
