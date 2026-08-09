import streamlit as st
import pandas as pd

from src.analysis.patterns import (
    load_data,
    analyze_patterns
)


st.title("🔎 Recurring Risk Patterns")

try:

    df = load_data()

    results = analyze_patterns(df)

except Exception as e:

    st.error(
        f"Pattern analysis failed: {e}"
    )

    st.stop()


st.subheader("Top Activities")

if "activity" in results:

    activity = results["activity"]

    st.bar_chart(
        activity.head(10)
    )

    st.dataframe(
        activity.head(10).rename("Incident Count")
    )


st.subheader("Recurring Event Types")

if "events" in results:

    events = results["events"]

    st.bar_chart(
        events.head(10)
    )

    st.dataframe(
        events.head(10).rename("Incident Count")
    )


st.subheader("Environmental Factors")

if "environment" in results:

    environment = results["environment"]

    st.bar_chart(
        environment.head(10)
    )

    st.dataframe(
        environment.head(10).rename("Incident Count")
    )


st.subheader("Human Factors")

if "human" in results:

    human = results["human"]

    st.bar_chart(
        human.head(10)
    )

    st.dataframe(
        human.head(10).rename("Incident Count")
    )