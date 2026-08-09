import os
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# Azure OpenAI configuration
# --------------------------------------------------

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_API_VERSION = os.getenv(
    "AZURE_OPENAI_API_VERSION",
    "2024-10-21"
)


# --------------------------------------------------
# Generate fallback brief
# --------------------------------------------------

def generate_fallback_brief(
    patterns,
    recommendations
):
    """
    Generates a weekly safety brief without Azure OpenAI.

    This makes the MVP work even when Azure credentials
    are unavailable.
    """

    lines = []

    lines.append("# Weekly Construction Safety Brief")
    lines.append("")

    lines.append("## Key Safety Patterns")
    lines.append("")

    # Activities
    if "activity" in patterns:
        lines.append("### Frequently Reported Activities")

        for activity, count in patterns["activity"].head(5).items():
            lines.append(
                f"- {activity}: {count} incidents"
            )

        lines.append("")

    # Events
    if "events" in patterns:
        lines.append("### Recurring Event Types")

        for event, count in patterns["events"].head(5).items():
            lines.append(
                f"- {event}: {count} incidents"
            )

        lines.append("")

    # Environmental factors
    if "environment" in patterns:
        lines.append("### Environmental Factors")

        for factor, count in patterns["environment"].head(5).items():
            lines.append(
                f"- {factor}: {count} incidents"
            )

        lines.append("")

    # Recommendations
    lines.append("## Preventive Actions")
    lines.append("")

    if recommendations:

        for recommendation in recommendations:

            toolbox = recommendation.get(
                "toolbox",
                "General Safety"
            )

            lines.append(
                f"### Toolbox Talk: {toolbox}"
            )

            for action in recommendation.get(
                "actions",
                []
            ):
                lines.append(
                    f"- {action}"
                )

            lines.append("")

    lines.append("## Safety Focus")

    lines.append(
        "Supervisors should review the identified hazards "
        "during pre-task planning and toolbox talks. "
        "Controls should focus on hazard prevention, "
        "proper PPE, equipment inspection, and safe work practices."
    )

    return "\n".join(lines)


# --------------------------------------------------
# Generate Azure OpenAI brief
# --------------------------------------------------

def generate_azure_brief(
    patterns,
    recommendations
):

    try:

        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=AZURE_API_KEY,
            api_version=AZURE_API_VERSION,
            azure_endpoint=AZURE_ENDPOINT
        )

        pattern_text = ""

        if "activity" in patterns:

            pattern_text += "\nTop Activities:\n"

            for activity, count in patterns["activity"].head(5).items():

                pattern_text += (
                    f"- {activity}: {count}\n"
                )

        if "events" in patterns:

            pattern_text += "\nRecurring Events:\n"

            for event, count in patterns["events"].head(5).items():

                pattern_text += (
                    f"- {event}: {count}\n"
                )

        recommendation_text = ""

        for recommendation in recommendations:

            recommendation_text += (
                f"\nToolbox Topic: "
                f"{recommendation.get('toolbox', '')}\n"
            )

            for action in recommendation.get(
                "actions",
                []
            ):

                recommendation_text += (
                    f"- {action}\n"
                )

        prompt = f"""
You are a construction safety assistant.

Create a concise weekly safety brief based only
on the provided historical incident patterns and
standard safety controls.

Focus on hazards and controls, not individual workers.

Do not blame workers.

Do not invent incidents or statistics.

Historical patterns:
{pattern_text}

Recommended controls:
{recommendation_text}

Return:

1. Top safety concerns
2. Recurring hazards
3. Preventive actions
4. Toolbox talk topics
5. Short supervisor focus for the week
"""

        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate concise construction "
                        "safety briefs focused on hazards "
                        "and preventive controls."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=800
        )

        return response.choices[0].message.content

    except Exception as error:

        print(
            "Azure OpenAI unavailable."
        )

        print(
            "Using fallback safety brief."
        )

        print(
            f"Reason: {error}"
        )

        return generate_fallback_brief(
            patterns,
            recommendations
        )


# --------------------------------------------------
# Main public function
# --------------------------------------------------

def generate_weekly_brief(
    patterns,
    recommendations
):

    # Use Azure only when credentials exist
    if (
        AZURE_ENDPOINT
        and AZURE_API_KEY
        and AZURE_DEPLOYMENT
    ):

        return generate_azure_brief(
            patterns,
            recommendations
        )

    # Otherwise use local fallback
    return generate_fallback_brief(
        patterns,
        recommendations
    )


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    print(
        "Weekly brief module loaded successfully."
    )

    print(
        "\nAzure configured:",
        bool(
            AZURE_ENDPOINT
            and AZURE_API_KEY
            and AZURE_DEPLOYMENT
        )
    )