
# ------------------------------------
# Rule-based safety recommendations
# ------------------------------------

SAFETY_RULES = {

    "fall": {
        "risk": "HIGH",
        "toolbox": "Fall Prevention & Working at Height",
        "actions": [
            "Inspect harness before use",
            "Use certified anchor points",
            "Install guardrails",
            "Use secured ladders",
            "Inspect scaffolding before work"
        ]
    },

    "struck": {
        "risk": "HIGH",
        "toolbox": "Struck-By Hazard Awareness",
        "actions": [
            "Wear helmets at all times",
            "Create exclusion zones",
            "Use spotters during lifting",
            "Secure suspended loads"
        ]
    },

    "caught": {
        "risk": "HIGH",
        "toolbox": "Machine & Pinch Point Safety",
        "actions": [
            "Lockout/Tagout before maintenance",
            "Keep hands away from moving parts",
            "Use machine guards",
            "Wear proper gloves"
        ]
    },

    "electrical": {
        "risk": "HIGH",
        "toolbox": "Electrical Safety",
        "actions": [
            "Verify isolation before work",
            "Use insulated tools",
            "Wear arc-rated PPE",
            "Maintain safe clearance"
        ]
    },

    "heat": {
        "risk": "MEDIUM",
        "toolbox": "Heat Stress Prevention",
        "actions": [
            "Drink water every 20 minutes",
            "Schedule shaded breaks",
            "Monitor heat illness symptoms",
            "Rotate workers during extreme heat"
        ]
    }
}

# ------------------------------------
# Recommendation function
# ------------------------------------

def get_recommendation(event_type):

    if not isinstance(event_type, str):
        event_type = ""

    event = event_type.lower()

    for keyword in SAFETY_RULES:

        if keyword in event:
            return SAFETY_RULES[keyword]

    return {
        "risk": "STANDARD",
        "toolbox": "General Construction Safety",
        "actions": [
            "Conduct pre-task risk assessment",
            "Inspect tools before use",
            "Wear mandatory PPE",
            "Maintain good housekeeping"
        ]
    }

# ------------------------------------
# Demo
# ------------------------------------

if __name__ == "__main__":

    sample = get_recommendation("Fall from Roof")

    print("\nRisk:", sample["risk"])
    print("Toolbox Talk:", sample["toolbox"])

    print("\nPreventive Actions:")

    for action in sample["actions"]:
        print("-", action)