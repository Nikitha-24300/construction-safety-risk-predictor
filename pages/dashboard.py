import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Construction Safety Dashboard",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Construction Safety Dashboard")


# ============================================================
# LOAD DATASET
# ============================================================

try:
    df = pd.read_csv("data/processed/incidents.csv")
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()


# ============================================================
# INCIDENT OVERVIEW
# ============================================================

st.subheader("📊 Incident Overview")

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


# ============================================================
# INCIDENT SEVERITY
# ============================================================

if "severity" in df.columns:

    st.subheader("⚠️ Incident Severity")

    severity_counts = df["severity"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(severity_counts)

    with col2:
        st.dataframe(
            severity_counts.rename("Number of Incidents"),
            use_container_width=True
        )


st.divider()


# ============================================================
# RISK CLASSIFICATION
# ============================================================

if "risk_level" in df.columns:

    st.subheader("🚨 Risk Classification")

    risk_counts = df["risk_level"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(risk_counts)

    with col2:
        st.dataframe(
            risk_counts.rename("Number of Incidents"),
            use_container_width=True
        )


st.divider()


# ============================================================
# CONSTRUCTION ACTIVITY & HAZARD CATEGORIES
# ============================================================

st.subheader("🏗️ Construction Activity & Hazard Categories")

activity_categories = {

    "Working at Height": [
        "Roof work",
        "Ladders",
        "Elevated platforms",
        "Fall hazards",
        "Scaffolding",
        "Scaffold erection/dismantling",
        "Scaffold inspection",
        "Working from scaffolds",
        "Falls/collapse"
    ],

    "Lifting & Material Handling": [
        "Crane operations",
        "Hoisting",
        "Heavy material movement",
        "Suspended loads",
        "Struck-by/crushing hazards"
    ],

    "Excavation & Trenching": [
        "Excavation",
        "Trenches",
        "Soil collapse",
        "Underground utilities",
        "Falls into excavation"
    ],

    "Concrete Work": [
        "Concrete pouring",
        "Formwork",
        "Reinforcement/rebar",
        "Pump operations",
        "Structural collapse hazards"
    ],

    "Electrical Work": [
        "Temporary electrical systems",
        "Power tools",
        "Electrical installations",
        "Energized equipment",
        "Shock/electrocution"
    ],

    "Demolition": [
        "Structural demolition",
        "Falling materials",
        "Dust exposure",
        "Unexpected structural failure"
    ],

    "Heavy Equipment / Vehicles": [
        "Excavators",
        "Bulldozers",
        "Dump trucks",
        "Forklifts",
        "Reversing/struck-by hazards"
    ],

    "Welding / Hot Work": [
        "Welding",
        "Cutting",
        "Grinding",
        "Fire",
        "Burns/fumes"
    ],

    "Confined Spaces": [
        "Tanks",
        "Pits",
        "Utility spaces",
        "Oxygen deficiency/toxic atmosphere"
    ]
}


selected_category = st.selectbox(
    "Select a construction activity category:",
    list(activity_categories.keys())
)


st.write(f"### {selected_category}")

hazards = activity_categories[selected_category]

for hazard in hazards:
    st.write(f"• {hazard}")


st.divider()


# ============================================================
# ACTIVITY ANALYSIS
# ============================================================

if "activity" in df.columns:

    st.subheader("📈 Most Reported Activities")

    activity_counts = (
        df["activity"]
        .astype(str)
        .value_counts()
        .head(10)
    )

    st.bar_chart(activity_counts)


st.divider()


# ============================================================
# ACTIVITY + SEVERITY ANALYSIS
# ============================================================

if "activity" in df.columns and "severity" in df.columns:

    st.subheader("📊 Activity vs Severity")

    activity_severity = pd.crosstab(
        df["activity"],
        df["severity"]
    ).head(10)

    st.dataframe(
        activity_severity,
        use_container_width=True
    )


st.divider()


# ============================================================
# LOCATION ANALYSIS
# ============================================================

if "location_type" in df.columns:

    st.subheader("📍 Incident Location Analysis")

    location_counts = (
        df["location_type"]
        .astype(str)
        .value_counts()
        .head(10)
    )

    st.bar_chart(location_counts)


st.divider()


# ============================================================
# HISTORICAL INCIDENT SEARCH
# ============================================================

if "description" in df.columns:

    st.subheader("🔎 Search Historical Incidents")

    search_text = st.text_input(
        "Search incident descriptions",
        placeholder="Example: scaffold, fall, crane, forklift..."
    )

    if search_text:

        results = df[
            df["description"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

        st.write(
            f"Found **{len(results)}** matching incidents."
        )

        columns_to_show = [
            column
            for column in [
                "severity",
                "risk_level",
                "activity",
                "location_type",
                "description"
            ]
            if column in results.columns
        ]

        st.dataframe(
            results[columns_to_show].head(20),
            use_container_width=True
        )


st.divider()


# ============================================================
# DATASET INFORMATION
# ============================================================

st.subheader("📋 Dataset Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Records",
        len(df)
    )

with col2:
    st.metric(
        "Columns",
        len(df.columns)
    )

with col3:
    st.metric(
        "Missing Values",
        int(df.isna().sum().sum())
    )


with st.expander("View Dataset Columns"):
    st.write(list(df.columns))