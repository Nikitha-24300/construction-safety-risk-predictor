import streamlit as st

from src.analysis.patterns import (
    load_data,
    analyze_patterns
)

from src.recommendations.safety_rules import (
    get_recommendation
)

from src.reports.weekly_brief import (
    generate_weekly_brief
)


st.title("📝 Weekly Safety Brief")

st.write(
    "Generate a safety brief from historical incident "
    "patterns and standard preventive controls."
)


if st.button(
    "Generate Weekly Safety Brief",
    type="primary"
):

    try:

        # ----------------------------------
        # Load incidents
        # ----------------------------------

        df = load_data()


        # ----------------------------------
        # Analyze patterns
        # ----------------------------------

        with st.spinner(
            "Analyzing incident patterns..."
        ):

            patterns = analyze_patterns(
                df
            )


        # ----------------------------------
        # Generate recommendations
        # ----------------------------------

        recommendations = []

        if "event_type" in df.columns:

            event_types = (
                df["event_type"]
                .dropna()
                .astype(str)
                .unique()
            )

            for event_type in event_types:

                recommendation = (
                    get_recommendation(
                        event_type
                    )
                )

                # Avoid duplicates
                if recommendation not in recommendations:

                    recommendations.append(
                        recommendation
                    )


        # ----------------------------------
        # Generate brief
        # ----------------------------------

        with st.spinner(
            "Generating weekly safety brief..."
        ):

            brief = generate_weekly_brief(
                patterns,
                recommendations
            )


        st.success(
            "Weekly safety brief generated."
        )


        st.markdown("---")

        st.markdown(
            brief
        )


        # ----------------------------------
        # Download
        # ----------------------------------

        st.download_button(
            label="Download Safety Brief",
            data=brief,
            file_name="weekly_safety_brief.md",
            mime="text/markdown"
        )


    except Exception as e:

        st.error(
            f"Could not generate weekly brief: {e}"
        )