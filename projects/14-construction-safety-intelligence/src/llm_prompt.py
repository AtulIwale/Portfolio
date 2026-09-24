"""
Prompt and output schema for the LLM step (used by src/llm_label.py and notebook 3).

The definitions below describe the nine cause groups built in notebook 1 from OSHA's event
titles (see RULES in src/cleaning.py). The LLM only ever sees the narrative text.
"""

CAUSE_GROUPS = {
    "Fall to lower level": "The worker fell from a height to a lower level: from a ladder, roof, scaffold, lift, platform, structure or vehicle, through an opening or skylight, or into a trench or hole. Includes falls stopped by a harness.",
    "Slip, trip or same-level fall": "The worker slipped, tripped or fell on the same level (floor or ground), with no real drop in height.",
    "Struck by or against object": "The worker was hit by a falling, flying, swinging, rolling or handled object, material or tool (including tool kickback and saw or grinder injuries), or by a moving part of a machine such as a bucket or boom; or the worker struck against an object. Not a vehicle driving into a person.",
    "Caught in or crushed": "A body part was caught, pinched, compressed, entangled or crushed in or between machinery, equipment or objects; or the worker was buried or crushed by a collapsing structure, trench cave-in or material.",
    "Vehicle or mobile equipment": "A worker on foot was struck or run over by a vehicle or mobile machine (truck, forklift, loader, roller), or a vehicle or machine overturned or collided.",
    "Electrical": "Electric shock, electrocution or arc flash, including contact with power lines.",
    "Heat stress": "Heat illness from a hot environment: heat exhaustion, heat stroke, dehydration, heat cramps.",
    "Fire, explosion or burn": "Fire, explosion, flash fire, ignition of vapours or clothing, or contact with hot objects or substances (not an electrical arc).",
    "Other": "Anything else: chemical or carbon monoxide exposure, insect or animal bites, violence, overexertion or lifting injuries, medical events.",
}

EQUIPMENT = ["ladder", "scaffold", "roof", "aerial or scissor lift", "crane or hoist", "excavator or earthmoving machine",
             "forklift", "truck or other vehicle", "power tool", "hand tool", "welding or hot work", "trench or excavation",
             "electrical equipment or power line", "structure, floor opening or edge", "none or unclear"]

SYSTEM = f"""You code construction injury reports for a safety team.
Read the incident narrative and return a JSON object with exactly these keys:

"cause_group": one of {list(CAUSE_GROUPS)}
"fall_height_ft": the height in feet that the worker FELL (not the height of the ladder, wall or trench), as a number; null if the worker did not fall to a lower level or no height is given. Convert metres to feet.
"equipment": the main equipment, structure or tool involved, one of {EQUIPMENT}
"task": what the worker was doing, in at most 8 words
"confidence": "high", "medium" or "low"

Cause group definitions:
""" + "\n".join(f"- {k}: {v}" for k, v in CAUSE_GROUPS.items()) + """

Choose the group for the event that directly caused the injury. Use only the narrative; do not guess details it does not state.
Return JSON only."""

# Few-shot examples come from the TRAINING years (2015-2022), never from the test years.
FEW_SHOT = [
    ("An employee was conducting work on second story balcony when they leaned on a guard rail and it fell off. The employee fell approximately 12 feet to the concrete below and sustained broken ribs.",
     {"cause_group": "Fall to lower level", "fall_height_ft": 12, "equipment": "structure, floor opening or edge", "task": "working on a second-storey balcony", "confidence": "high"}),
    ("An employee was climbing a 16-20 foot extension ladder to secure it. While stepping onto the roof to tie off the ladder, the ladder slipped and the employee fell. The employee landed on paver stones on a walkway and was hospitalized with a broken arm and leg.",
     {"cause_group": "Fall to lower level", "fall_height_ft": None, "equipment": "ladder", "task": "stepping from ladder onto roof", "confidence": "high"}),
    ("An employee was holding a piece of metal attached to a cable when the cable pulled and the employee's hand was caught between a metal part and pipe, causing an amputation of the left middle finger above the second joint.",
     {"cause_group": "Caught in or crushed", "fall_height_ft": None, "equipment": "none or unclear", "task": "holding metal attached to a cable", "confidence": "high"}),
    ("While pulling electrical line using a tugger and tensioner, an employee came in contact with a live electric current and sustained burns to the left hand.",
     {"cause_group": "Electrical", "fall_height_ft": None, "equipment": "electrical equipment or power line", "task": "pulling electrical line with a tugger", "confidence": "high"}),
    ("An employee was welding tube steel above his head when a spark entered his coat and caught it on fire. He received second and third degree burns to his left arm from his elbow to his fingers.",
     {"cause_group": "Fire, explosion or burn", "fall_height_ft": None, "equipment": "welding or hot work", "task": "welding tube steel overhead", "confidence": "high"}),
    ("As an employee was walking on site, he felt lightheaded and headed over to the gang box, where he blacked out. He was hospitalized for possible heat-related illness.",
     {"cause_group": "Heat stress", "fall_height_ft": None, "equipment": "none or unclear", "task": "walking on site", "confidence": "high"}),
    ("Employees were using gas-powered tools in the basement to cut a cement floor. One employee was found unconscious. A second employee suffered dizziness, difficulty breathing, and headaches. Both employees were hospitalized due to exposure to carbon monoxide.",
     {"cause_group": "Other", "fall_height_ft": None, "equipment": "power tool", "task": "cutting a cement floor in a basement", "confidence": "high"}),
    ("An employee was walking out of a construction trailer when she slipped on ice and fell to the ground, resulting in a broken leg. The employee was admitted to the hospital for surgery.",
     {"cause_group": "Slip, trip or same-level fall", "fall_height_ft": None, "equipment": "none or unclear", "task": "walking out of a site trailer", "confidence": "high"}),
    ("An employee was operating a wire brush handheld grinder to smooth out concrete. The grinder hit the side of a stair and kicked back, hitting the employee's left leg and causing a 2\" deep and 4\" wide laceration on his thigh.",
     {"cause_group": "Struck by or against object", "fall_height_ft": None, "equipment": "power tool", "task": "grinding concrete with a wire brush", "confidence": "high"}),
    ("An employee was kneeling down to take measurements for a curtain wall when a forklift operator drove through a door and ran over the employee's left foot, fracturing it.",
     {"cause_group": "Vehicle or mobile equipment", "fall_height_ft": None, "equipment": "forklift", "task": "taking measurements for a curtain wall", "confidence": "high"}),
]


def messages(narrative, few_shot=False):
    import json
    msgs = [{"role": "system", "content": SYSTEM}]
    if few_shot:
        for text, answer in FEW_SHOT:
            msgs.append({"role": "user", "content": f"Narrative: {text}"})
            msgs.append({"role": "assistant", "content": json.dumps(answer)})
    msgs.append({"role": "user", "content": f"Narrative: {narrative}"})
    return msgs


def validate(obj):
    """Return a clean dict, or raise ValueError. Guards against answers outside the allowed lists."""
    if obj.get("cause_group") not in CAUSE_GROUPS:
        raise ValueError(f"unknown cause_group {obj.get('cause_group')!r}")
    h = obj.get("fall_height_ft")
    if h is not None:
        h = float(h)
        if not 0 < h < 1000:
            h = None
    eq = obj.get("equipment") if obj.get("equipment") in EQUIPMENT else "none or unclear"
    conf = obj.get("confidence") if obj.get("confidence") in ("high", "medium", "low") else "low"
    return {"cause_group": obj["cause_group"], "fall_height_ft": h, "equipment": eq,
            "task": str(obj.get("task", ""))[:80], "confidence": conf}
