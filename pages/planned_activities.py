import os
import streamlit as st
import pandas as pd


st.title("📅 Planned Activities")


file_path = "data/processed/pattern_summary.csv"

if not os.path.exists(file_path):

    st.info(
        "pattern_summary.csv is not available yet. "
        "You can add synthetic planned activities later."
    )

    st.stop()


df = pd.read_csv(file_path)


st.subheader("pattern summary")

st.dataframe(
    df,
    use_container_width=True
)


st.subheader("Activity Summary")

if "activity" in df.columns:

    counts = (
        df["activity"]
        .value_counts()
    )

    st.bar_chart(counts)