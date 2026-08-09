import streamlit as st
import pandas as pd


st.title("📊 Safety Dashboard")

try:
    df = pd.read_csv(
        "data/processed/incidents.csv"
    )
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()


st.subheader("Incident Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Incidents",
        len(df)
    )

with col2:
    if "severity" in df.columns:
        fatal = (
            df["severity"]
            .astype(str)
            .str.lower()
            .eq("fatal")
            .sum()
        )
        st.metric("Fatal", int(fatal))
    else:
        st.metric("Fatal", "N/A")

with col3:
    if "severity" in df.columns:
        nonfatal = (
            df["severity"]
            .astype(str)
            .str.lower()
            .eq("nonfatal")
            .sum()
        )
        st.metric("Non-Fatal", int(nonfatal))
    else:
        st.metric("Non-Fatal", "N/A")

with col4:
    if "activity" in df.columns:
        st.metric(
            "Activities",
            df["activity"].nunique()
        )
    else:
        st.metric("Activities", "N/A")


st.divider()

if "severity" in df.columns:

    st.subheader("Incident Severity")

    severity_counts = (
        df["severity"]
        .value_counts()
    )

    st.bar_chart(severity_counts)


if "activity" in df.columns:

    st.subheader("Most Reported Activities")

    activity_counts = (
        df["activity"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(activity_counts)