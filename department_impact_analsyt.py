from agent.utils import contains_keyword

def classify_affected_departments(changes: list) -> dict:
    """Classify departments affected by screenplay changes."""

    department_impact = {
        "sound_continuity": 0,
        "camera": 0,
        "lighting": 0,
        "production_design": 0,
        "costume": 0,
        "makeup": 0,
        "stunts": 0,
        "visual_effects": 0,
        "other": 0,
    }

    for change in changes:
        old_lines = change.get("old_lines", [])
        new_lines = change.get("new_lines", [])

        text = " ".join(old_lines + new_lines).lower()

        if any(contains_keyword(text, k) for k in [
            "sound", "dialogue", "audio", "whisper", "shout",
            "scream", "phone", "radio", "music", "rain",
            "traffic", "generator", "silence"
        ]):
            department_impact["sound_continuity"] += 1

        if any(contains_keyword(text, k) for k in [
            "camera", "shot", "angle", "close-up", "wide shot",
            "pan", "zoom", "tracking"
        ]):
            department_impact["camera"] += 1

        if any(contains_keyword(text, k) for k in [
            "light", "lighting", "illumination", "dark",
            "bright", "shadow", "night", "day"
        ]):
            department_impact["lighting"] += 1

        if any(contains_keyword(text, k) for k in [
            "set", "location", "room", "street", "road",
            "props", "car", "vehicle", "generator"
        ]):
            department_impact["production_design"] += 1

        if any(contains_keyword(text, k) for k in [
            "costume", "wardrobe", "dress", "shirt", "uniform"
        ]):
            department_impact["costume"] += 1

        if any(contains_keyword(text, k) for k in [
            "makeup", "hair", "blood", "bruise", "scar"
        ]):
            department_impact["makeup"] += 1

        if any(contains_keyword(text, k) for k in [
            "stunt", "fight", "action", "chase", "explosion"
        ]):
            department_impact["stunts"] += 1

        if any(contains_keyword(text, k) for k in [
            "vfx", "visual effect", "cgi", "digital", "green screen"
        ]):
            department_impact["visual_effects"] += 1

    affected = [
        department
        for department, count in department_impact.items()
        if count > 0
    ]

    return {
        "affected_departments": affected,
        "impact_counts": department_impact,
    }