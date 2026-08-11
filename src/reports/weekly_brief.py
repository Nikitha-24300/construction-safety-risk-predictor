from datetime import date, timedelta

import pandas as pd


WEEKLY_FILE = "data/processed/weekly_inputs.csv"


def get_current_week_range(reference_date=None):
    """
    Return Monday-Sunday for the week containing reference_date.
    """

    if reference_date is None:
        reference_date = date.today()

    start = (
        reference_date
        - timedelta(days=reference_date.weekday())
    )

    end = start + timedelta(days=6)

    return start, end


def get_weekly_inputs(
    df,
    reference_date=None
):
    """
    Filter the input data to the current week.
    """

    start, end = get_current_week_range(
        reference_date
    )

    df = df.copy()

    if df.empty:
        return df

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    weekly = df[
        (df["date"].dt.date >= start)
        &
        (df["date"].dt.date <= end)
    ].copy()

    return weekly


def build_weekly_summary(weekly_df):
    """
    Create a structured summary of this week's
    safety predictions.
    """

    if weekly_df.empty:

        return {
            "total_inputs": 0,
            "high_risk": 0,
            "non_high_risk": 0,
            "top_activities": {},
            "top_hazards": {},
            "top_environmental_factors": {},
            "top_human_factors": {},
        }


    # -----------------------------------------
    # Risk counts
    # -----------------------------------------

    risk_values = (
        weekly_df["risk_level"]
        .astype(str)
        .str.upper()
    )

    high_risk = (
        risk_values == "HIGH"
    ).sum()

    non_high_risk = (
        risk_values == "NON-HIGH"
    ).sum()


    # -----------------------------------------
    # Top activities
    # -----------------------------------------

    if "activity" in weekly_df.columns:

        top_activities = (
            weekly_df["activity"]
            .value_counts()
            .head(5)
            .to_dict()
        )

    else:

        top_activities = {}


    # -----------------------------------------
    # Top hazards
    # -----------------------------------------

    if "event_type" in weekly_df.columns:

        top_hazards = (
            weekly_df["event_type"]
            .value_counts()
            .head(5)
            .to_dict()
        )

    else:

        top_hazards = {}


    # -----------------------------------------
    # Environmental factors
    # -----------------------------------------

    if "environmental_factor" in weekly_df.columns:

        top_environmental = (
            weekly_df["environmental_factor"]
            .value_counts()
            .head(5)
            .to_dict()
        )

    else:

        top_environmental = {}


    # -----------------------------------------
    # Human factors
    # -----------------------------------------

    if "human_factor" in weekly_df.columns:

        top_human = (
            weekly_df["human_factor"]
            .value_counts()
            .head(5)
            .to_dict()
        )

    else:

        top_human = {}


    return {
        "total_inputs": len(weekly_df),
        "high_risk": int(high_risk),
        "non_high_risk": int(non_high_risk),
        "top_activities": top_activities,
        "top_hazards": top_hazards,
        "top_environmental_factors": top_environmental,
        "top_human_factors": top_human,
    }


def generate_text_brief(
    weekly_df,
    summary
):
    """
    Generate a human-readable weekly safety brief.
    """

    start, end = get_current_week_range()

    lines = []

    lines.append("# Weekly Safety Brief")
    lines.append("")
    lines.append(
        f"**Reporting Period:** "
        f"{start.strftime('%B %d, %Y')} - "
        f"{end.strftime('%B %d, %Y')}"
    )

    lines.append("")

    lines.append("## Weekly Overview")
    lines.append("")

    lines.append(
        f"- Total safety inputs: "
        f"{summary['total_inputs']}"
    )

    lines.append(
        f"- High-risk predictions: "
        f"{summary['high_risk']}"
    )

    lines.append(
        f"- Non-high-risk predictions: "
        f"{summary['non_high_risk']}"
    )

    lines.append("")


    # -----------------------------------------
    # Activities
    # -----------------------------------------

    lines.append("## Top Activities")
    lines.append("")

    if summary["top_activities"]:

        for activity, count in (
            summary["top_activities"].items()
        ):

            lines.append(
                f"- {activity}: {count}"
            )

    else:

        lines.append(
            "- No activity data available."
        )

    lines.append("")


    # -----------------------------------------
    # Hazards
    # -----------------------------------------

    lines.append("## Top Hazards")
    lines.append("")

    if summary["top_hazards"]:

        for hazard, count in (
            summary["top_hazards"].items()
        ):

            lines.append(
                f"- {hazard}: {count}"
            )

    else:

        lines.append(
            "- No hazard data available."
        )

    lines.append("")


    # -----------------------------------------
    # Environmental factors
    # -----------------------------------------

    lines.append(
        "## Environmental Factors"
    )

    lines.append("")

    if summary["top_environmental_factors"]:

        for factor, count in (
            summary[
                "top_environmental_factors"
            ].items()
        ):

            lines.append(
                f"- {factor}: {count}"
            )

    else:

        lines.append(
            "- No environmental data available."
        )

    lines.append("")


    # -----------------------------------------
    # Human factors
    # -----------------------------------------

    lines.append("## Human Factors")
    lines.append("")

    if summary["top_human_factors"]:

        for factor, count in (
            summary["top_human_factors"].items()
        ):

            lines.append(
                f"- {factor}: {count}"
            )

    else:

        lines.append(
            "- No human-factor data available."
        )

    lines.append("")


    # -----------------------------------------
    # Safety focus
    # -----------------------------------------

    lines.append("## Recommended Safety Focus")
    lines.append("")

    if summary["high_risk"] > 0:

        lines.append(
            "⚠️ High-risk activities were identified "
            "this week. Prioritize review of the "
            "identified hazards and appropriate "
            "engineering, administrative, and PPE "
            "controls."
        )

    else:

        lines.append(
            "No HIGH risk predictions were recorded "
            "this week. Continue routine hazard "
            "identification and preventive controls."
        )


    return "\n".join(lines)