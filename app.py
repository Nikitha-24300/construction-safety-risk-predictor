import streamlit as st


st.set_page_config(
    page_title="Construction Safety Risk Predictor",
    page_icon="🦺",
    layout="wide"
)


st.title("🦺 Construction Safety Risk Predictor")

st.markdown(
    """
    ## AI-Assisted Construction Safety Monitoring

    This MVP analyzes historical construction incident data to:

    - Predict safety risk
    - Identify recurring hazard patterns
    - Highlight contributing factors
    - Recommend preventive controls
    - Generate a weekly safety brief

    ### Privacy & Safety

    The system focuses on **hazards and controls**, not individual
    worker profiling or blame.
    """
)

st.divider()

# Load basic statistics
try:
    import pandas as pd

    df = pd.read_csv(
        "data/processed/incidents.csv"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Incidents",
            len(df)
        )

    with col2:
        if "severity" in df.columns:
            st.metric(
                "Fatal Incidents",
                int(
                    (df["severity"].astype(str).str.lower() == "fatal")
                    .sum()
                )
            )
        else:
            st.metric("Fatal Incidents", "N/A")

    with col3:
        if "activity" in df.columns:
            st.metric(
                "Activity Types",
                df["activity"].nunique()
            )
        else:
            st.metric("Activity Types", "N/A")

except Exception as e:

    st.warning(
        f"Could not load incident statistics: {e}"
    )

st.divider()

st.info(
    "Use the pages in the sidebar to explore risk predictions, "
    "recurring patterns, preventive actions, planned activities, "
    "and the weekly safety brief."
)