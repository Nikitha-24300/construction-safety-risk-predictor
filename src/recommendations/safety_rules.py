# ------------------------------------
# Preventive Action Recommendations
# ------------------------------------

SAFETY_RULES = {

    "Absorption": {
        "risk": "HIGH",
        "toolbox": "Chemical Exposure Safety",
        "actions": [
            "Conduct chemical exposure risk assessment",
            "Inspect chemical containers before use",
            "Wear chemical-resistant gloves",
            "Wear safety goggles or face shield",
            "Use appropriate protective clothing",
            "Ensure eyewash and safety shower are accessible",
            "Maintain proper chemical labeling",
            "Provide adequate ventilation"
        ]
    },

    "Bite/sting/scratch": {
        "risk": "MEDIUM",
        "toolbox": "Animal and Insect Safety",
        "actions": [
            "Conduct pre-task area inspection",
            "Check for insects, animals, nests, and hives",
            "Maintain good housekeeping",
            "Control pests regularly",
            "Wear appropriate protective clothing",
            "Wear gloves and safety footwear where required",
            "Avoid disturbing animals or nests",
            "Report bites, stings, or scratches immediately"
        ]
    },

    "Card-vascular/resp. fail.": {
        "risk": "HIGH",
        "toolbox": "Emergency Response Safety",
        "actions": [
            "Conduct emergency preparedness assessment",
            "Maintain accessible first-aid facilities",
            "Provide trained first-aiders and CPR responders",
            "Ensure AED is available where required",
            "Maintain emergency communication systems",
            "Control exposure to hazardous gases and fumes",
            "Ensure adequate workplace ventilation",
            "Conduct emergency response drills"
        ]
    },

    "Caught in or between": {
        "risk": "HIGH",
        "toolbox": "Caught-In and Caught-Between Safety",
        "actions": [
            "Conduct pre-task risk assessment",
            "Identify and control pinch points",
            "Inspect machine guards before use",
            "Never bypass safety guards",
            "Follow Lockout/Tagout (LOTO) procedures",
            "Keep hands clear of moving parts",
            "Use proper tools for clearing blockages",
            "Perform regular equipment maintenance"
        ]
    },

    "Fall (from elevation)": {
        "risk": "HIGH",
        "toolbox": "Working at Height Safety",
        "actions": [
            "Conduct work-at-height risk assessment",
            "Inspect ladders and scaffolds before use",
            "Install and maintain guardrails",
            "Use approved fall protection systems",
            "Inspect harnesses and lanyards before use",
            "Secure ladders properly before climbing",
            "Maintain three-point contact on ladders",
            "Keep elevated work areas free from obstructions"
        ]
    },

    "Fall (same level)": {
        "risk": "MEDIUM",
        "toolbox": "Slip, Trip and Fall Prevention",
        "actions": [
            "Conduct pre-task area inspection",
            "Maintain good housekeeping",
            "Keep walkways clear of obstructions",
            "Clean spills immediately",
            "Secure cables and hoses",
            "Maintain adequate lighting",
            "Repair damaged or uneven flooring",
            "Wear appropriate safety footwear"
        ]
    },

    "Ingestion": {
        "risk": "HIGH",
        "toolbox": "Chemical Ingestion Prevention",
        "actions": [
            "Conduct chemical handling risk assessment",
            "Maintain proper chemical labeling",
            "Store chemicals in approved containers",
            "Never store chemicals in food containers",
            "Prohibit eating and drinking in hazardous areas",
            "Wash hands before eating or drinking",
            "Maintain good personal hygiene",
            "Wear appropriate PPE"
        ]
    },

    "Inhalation": {
        "risk": "HIGH",
        "toolbox": "Respiratory Protection Safety",
        "actions": [
            "Conduct airborne exposure risk assessment",
            "Inspect ventilation systems regularly",
            "Provide adequate ventilation",
            "Use local exhaust ventilation where required",
            "Keep chemical containers closed when not in use",
            "Monitor airborne contaminants where required",
            "Wear approved respiratory protection",
            "Provide respiratory protection training"
        ]
    },

    "Other": {
        "risk": "STANDARD",
        "toolbox": "General Hazard Control",
        "actions": [
            "Conduct detailed hazard identification",
            "Conduct task-specific risk assessment",
            "Identify the root cause of the incident",
            "Implement appropriate engineering controls",
            "Follow approved safe work procedures",
            "Wear mandatory PPE",
            "Provide required safety training",
            "Conduct regular workplace inspections"
        ]
    },

    "Rep. Motion/pressure": {
        "risk": "MEDIUM",
        "toolbox": "Ergonomic and Repetitive Motion Safety",
        "actions": [
            "Conduct ergonomic risk assessment",
            "Inspect workstations for ergonomic hazards",
            "Maintain proper working posture",
            "Use ergonomically designed tools",
            "Reduce repetitive movements where possible",
            "Rotate tasks where appropriate",
            "Provide adequate rest breaks",
            "Report early signs of discomfort"
        ]
    },

    "Rubbed/abraded": {
        "risk": "MEDIUM",
        "toolbox": "Contact and Abrasion Safety",
        "actions": [
            "Conduct pre-task hazard assessment",
            "Inspect work surfaces for rough edges",
            "Remove or cover abrasive surfaces",
            "Install guards on hazardous surfaces",
            "Wear suitable protective gloves",
            "Wear appropriate protective clothing",
            "Maintain good housekeeping",
            "Inspect PPE before use"
        ]
    },

    "Shock": {
        "risk": "HIGH",
        "toolbox": "Electrical Safety",
        "actions": [
            "Conduct electrical risk assessment",
            "Inspect electrical equipment before use",
            "Ensure proper grounding and earthing",
            "Follow Lockout/Tagout (LOTO) procedures",
            "De-energize equipment before maintenance",
            "Do not use damaged cables or plugs",
            "Use appropriate electrical PPE",
            "Restrict electrical work to authorized personnel"
        ]
    },

    "Struck against": {
        "risk": "MEDIUM",
        "toolbox": "Struck-Against Safety",
        "actions": [
            "Conduct pre-task area inspection",
            "Maintain good housekeeping",
            "Keep walkways clear of obstructions",
            "Maintain adequate clearance around equipment",
            "Provide adequate lighting",
            "Mark low beams, pipes, and protruding objects",
            "Remove unnecessary obstacles",
            "Wear mandatory PPE"
        ]
    },

    "Struck-by": {
        "risk": "HIGH",
        "toolbox": "Struck-By and Falling Object Safety",
        "actions": [
            "Conduct pre-task risk assessment",
            "Identify line-of-fire hazards",
            "Secure tools and materials properly",
            "Inspect lifting equipment before use",
            "Establish exclusion zones",
            "Never stand under suspended loads",
            "Separate pedestrians from moving equipment",
            "Wear mandatory PPE"
        ]
    }
}


# ------------------------------------
# Recommendation Function
# ------------------------------------

def get_recommendation(event_type):

    if not isinstance(event_type, str):
        event_type = ""

    # Exact hazard type match
    if event_type in SAFETY_RULES:
        return SAFETY_RULES[event_type]

    # Case-insensitive match
    for hazard, recommendation in SAFETY_RULES.items():

        if hazard.lower() == event_type.lower():
            return recommendation

    # Default recommendation
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