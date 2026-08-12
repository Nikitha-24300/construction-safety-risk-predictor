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
    },

    # ==========================================================
    # CONSTRUCTION ACTIVITY CATEGORIES
    # ==========================================================

    "Scaffolding": {
        "risk": "HIGH",
        "toolbox": "Scaffold Safety and Inspection",
        "actions": [
            "Conduct scaffold safety assessment before work",
            "Inspect scaffolding before use",
            "Check scaffold stability and support",
            "Inspect platforms and access points",
            "Provide appropriate guardrails and fall protection",
            "Do not exceed intended scaffold load",
            "Keep scaffold platforms clear of unnecessary materials",
            "Reinspect scaffolding after modification or significant changes"
        ]
    },

    "Working at Height": {
        "risk": "HIGH",
        "toolbox": "Working at Height Safety",
        "actions": [
            "Conduct work-at-height risk assessment",
            "Identify open edges and floor openings",
            "Provide appropriate fall protection",
            "Inspect ladders and access equipment",
            "Provide safe access and egress",
            "Protect exposed edges and openings",
            "Secure tools and materials against falling",
            "Maintain good housekeeping"
        ]
    },

    "Roof Work": {
        "risk": "HIGH",
        "toolbox": "Roof Work Safety",
        "actions": [
            "Conduct roof work risk assessment",
            "Identify roof edges and openings",
            "Identify fragile roof surfaces",
            "Provide appropriate fall protection",
            "Provide safe roof access",
            "Protect roof openings",
            "Control falling-object hazards",
            "Maintain good housekeeping"
        ]
    },

    "Ladders": {
        "risk": "HIGH",
        "toolbox": "Ladder Safety",
        "actions": [
            "Inspect ladders before use",
            "Use the correct ladder for the task",
            "Place ladders on stable surfaces",
            "Secure ladders where required",
            "Maintain safe climbing practices",
            "Do not use damaged ladders",
            "Keep ladder areas clear",
            "Avoid unsafe overreaching"
        ]
    },

    "Lifting & Material Handling": {
        "risk": "HIGH",
        "toolbox": "Lifting and Material Handling Safety",
        "actions": [
            "Conduct lifting risk assessment",
            "Inspect lifting equipment before use",
            "Verify load capacity",
            "Secure loads properly",
            "Establish exclusion zones",
            "Keep personnel away from suspended loads",
            "Control line-of-fire hazards",
            "Maintain clear communication during lifting"
        ]
    },

    "Excavation & Trenching": {
        "risk": "HIGH",
        "toolbox": "Excavation and Trenching Safety",
        "actions": [
            "Conduct excavation risk assessment",
            "Identify underground utilities",
            "Inspect excavation conditions",
            "Provide appropriate protective systems",
            "Provide safe access and egress",
            "Keep materials away from excavation edges",
            "Control water accumulation where required",
            "Prevent unauthorized access"
        ]
    },

    "Concrete Work": {
        "risk": "HIGH",
        "toolbox": "Concrete and Formwork Safety",
        "actions": [
            "Inspect formwork before concrete placement",
            "Check supports and bracing",
            "Verify stability of temporary structures",
            "Control exposed reinforcement hazards",
            "Inspect concrete pumping equipment",
            "Maintain safe communication during concrete placement",
            "Control equipment movement",
            "Maintain good housekeeping"
        ]
    },

    "Electrical Work": {
        "risk": "HIGH",
        "toolbox": "Construction Electrical Safety",
        "actions": [
            "Conduct electrical risk assessment",
            "Inspect temporary electrical systems",
            "Inspect electrical equipment before use",
            "Control access to energized equipment",
            "Follow appropriate isolation procedures",
            "Do not use damaged cables or plugs",
            "Use appropriate electrical PPE",
            "Restrict electrical work to authorized personnel"
        ]
    },

    "Demolition": {
        "risk": "HIGH",
        "toolbox": "Demolition Safety",
        "actions": [
            "Conduct demolition risk assessment",
            "Assess structural conditions",
            "Follow a planned demolition sequence",
            "Establish exclusion zones",
            "Control falling materials",
            "Control dust exposure",
            "Keep unauthorized personnel away",
            "Monitor for structural instability"
        ]
    },

    "Heavy Equipment / Vehicles": {
        "risk": "HIGH",
        "toolbox": "Heavy Equipment and Vehicle Safety",
        "actions": [
            "Inspect equipment before operation",
            "Identify equipment movement areas",
            "Separate pedestrian and vehicle routes",
            "Control reversing operations",
            "Maintain awareness of blind spots",
            "Keep personnel away from moving equipment",
            "Use appropriate communication and signaling",
            "Remove defective equipment from service"
        ]
    },

    "Welding / Hot Work": {
        "risk": "HIGH",
        "toolbox": "Welding and Hot Work Safety",
        "actions": [
            "Inspect hot-work equipment",
            "Control combustible materials",
            "Provide adequate ventilation",
            "Control sparks and hot materials",
            "Use appropriate protective equipment",
            "Maintain fire-prevention controls",
            "Keep the work area clean",
            "Store gas cylinders safely"
        ]
    },

    "Confined Spaces": {
        "risk": "HIGH",
        "toolbox": "Confined Space Safety",
        "actions": [
            "Assess the confined space before entry",
            "Identify potential atmospheric hazards",
            "Perform required atmospheric testing",
            "Provide ventilation where required",
            "Control hazardous energy sources",
            "Establish appropriate emergency arrangements",
            "Maintain communication during work",
            "Prevent unauthorized entry"
        ]
    }
}


# ------------------------------------
# Recommendation Function
# ------------------------------------

def get_recommendation(event_type):

    if not isinstance(event_type, str):
        event_type = ""

    event_type = event_type.strip()

    # Exact match
    if event_type in SAFETY_RULES:
        return SAFETY_RULES[event_type]

    # Case-insensitive match
    for hazard, recommendation in SAFETY_RULES.items():

        if hazard.lower() == event_type.lower():
            return recommendation

    # Related construction keywords
    text = event_type.lower()

    keyword_mapping = {

        "scaffold": "Scaffolding",

        "working at height": "Working at Height",
        "work at height": "Working at Height",

        "roof": "Roof Work",

        "ladder": "Ladders",

        "lifting": "Lifting & Material Handling",
        "hoisting": "Lifting & Material Handling",
        "crane": "Lifting & Material Handling",

        "excavat": "Excavation & Trenching",
        "trench": "Excavation & Trenching",

        "concrete": "Concrete Work",
        "formwork": "Concrete Work",
        "rebar": "Concrete Work",
        "reinforcement": "Concrete Work",

        "electrical": "Electrical Work",
        "electric": "Electrical Work",

        "demolition": "Demolition",

        "excavator": "Heavy Equipment / Vehicles",
        "bulldozer": "Heavy Equipment / Vehicles",
        "dump truck": "Heavy Equipment / Vehicles",
        "forklift": "Heavy Equipment / Vehicles",

        "welding": "Welding / Hot Work",
        "cutting": "Welding / Hot Work",
        "grinding": "Welding / Hot Work",
        "hot work": "Welding / Hot Work",

        "confined space": "Confined Spaces",
        "confined": "Confined Spaces"
    }

    for keyword, category in keyword_mapping.items():

        if keyword in text:
            return SAFETY_RULES[category]

    # Default recommendation
    return {
        "risk": "STANDARD",
        "toolbox": "General Construction Safety",
        "actions": [
            "Conduct pre-task risk assessment",
            "Identify activity-specific hazards",
            "Inspect tools and equipment before use",
            "Use appropriate safety controls",
            "Wear mandatory PPE",
            "Maintain good housekeeping"
        ]
    }