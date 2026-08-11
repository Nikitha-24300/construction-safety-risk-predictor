import os

import pandas as pd
import streamlit as st

from src.reports.weekly_brief import (
    get_current_week_range,
    get_weekly_inputs,
    build_weekly_summary,
    generate_text_brief,
)


WEEKLY_FILE = "data/processed/weekly_inputs.csv"


# ============================================================
# PAGE
# ============================================================

st.title("📝 Weekly Safety Brief")

st.write(
    "This report is automatically generated from "
    "the risk predictions submitted during the current week."
)


# ============================================================
# CHECK DATA
# ============================================================

if not os.path.exists(WEEKLY_FILE):

    st.info(
        "No weekly safety inputs have been recorded yet. "
        "Go to Risk Prediction and submit a prediction first."
    )

    st.stop()


try:

    df = pd.read_csv(
        WEEKLY_FILE
    )

except pd.errors.EmptyDataError:

    st.info(
        "No weekly safety inputs have been recorded yet."
    )

    st.stop()

except Exception as e:

    st.error(
        f"Could not load weekly safety data: {e}"
    )

    st.stop()


if df.empty:

    st.info(
        "No weekly safety inputs have been recorded yet."
    )

    st.stop()


# ============================================================
# CURRENT WEEK
# ============================================================

start, end = get_current_week_range()


st.subheader(
    f"Reporting Period: "
    f"{start.strftime('%B %d, %Y')} - "
    f"{end.strftime('%B %d, %Y')}"
)


# ============================================================
# FILTER CURRENT WEEK
# ============================================================

weekly_df = get_weekly_inputs(
    df
)


if weekly_df.empty:

    st.warning(
        "No risk predictions have been submitted "
        "during the current week."
    )

    st.info(
        "Submit a prediction from the Risk Prediction "
        "page to populate this report."
    )

    st.stop()


# ============================================================
# BUILD SUMMARY
# ============================================================

summary = build_weekly_summary(
    weekly_df
)


# ============================================================
# METRICS
# ============================================================

st.subheader("Weekly Overview")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Inputs",
        summary["total_inputs"]
    )


with col2:

    st.metric(
        "HIGH Risk",
        summary["high_risk"]
    )


with col3:

    st.metric(
        "NON-HIGH Risk",
        summary["non_high_risk"]
    )

# ============================================================
# TOP HAZARDS
# ============================================================

st.subheader("Top Hazards")

if summary["top_hazards"]:

    hazard_df = pd.DataFrame(
        list(
            summary["top_hazards"].items()
        ),
        columns=[
            "Hazard",
            "Count"
        ]
    )

    st.bar_chart(
        hazard_df.set_index("Hazard")
    )

else:

    st.info(
        "No hazard data available."
    )


# ============================================================
# TOP ACTIVITIES
# ============================================================

st.subheader("Top Activities")

if summary["top_activities"]:

    activity_df = pd.DataFrame(
        list(
            summary["top_activities"].items()
        ),
        columns=[
            "Activity",
            "Count"
        ]
    )

    st.bar_chart(
        activity_df.set_index("Activity")
    )

else:

    st.info(
        "No activity data available."
    )


# ============================================================
# ENVIRONMENTAL FACTORS
# ============================================================

st.subheader(
    "Environmental Factors"
)

if summary["top_environmental_factors"]:

    environment_df = pd.DataFrame(
        list(
            summary[
                "top_environmental_factors"
            ].items()
        ),
        columns=[
            "Factor",
            "Count"
        ]
    )

    st.dataframe(
        environment_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No environmental factor data available."
    )


# ============================================================
# HUMAN FACTORS
# ============================================================

st.subheader("Human Factors")

if summary["top_human_factors"]:

    human_df = pd.DataFrame(
        list(
            summary[
                "top_human_factors"
            ].items()
        ),
        columns=[
            "Factor",
            "Count"
        ]
    )

    st.dataframe(
        human_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No human factor data available."
    )


# ============================================================
# GENERATE TEXT BRIEF
# ============================================================

st.divider()

st.subheader("📄 Weekly Safety Brief")

brief = generate_text_brief(
    weekly_df,
    summary
)

st.markdown(
    brief
)


# ============================================================
# DOWNLOAD
# ============================================================

st.download_button(
    label="⬇️ Download Weekly Brief",
    data=brief,
    file_name=(
        f"weekly_safety_brief_"
        f"{start.isoformat()}.md"
    ),
    mime="text/markdown"
)