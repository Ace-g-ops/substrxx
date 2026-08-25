"""
Test harness for classify_affected_departments()
Run: python test_department_classification.py
"""
import re


def _contains_keyword(text: str, keyword: str) -> bool:
    """Boundary only at the START of the keyword: blocks 'car' matching
    inside 'scar', but still allows 'whisper' to match 'whispers',
    'road' to match 'roadside', etc."""
    return re.search(rf"\b{re.escape(keyword)}\w*", text) is not None


def classify_affected_departments(changes: list) -> dict:
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

        if any(_contains_keyword(text, k) for k in ["sound", "dialogue", "audio", "whisper", "shout",
                                    "scream", "phone", "radio", "music", "rain",
                                    "traffic", "generator", "silence"]):
            department_impact["sound_continuity"] += 1
        if any(_contains_keyword(text, k) for k in ["camera", "shot", "angle", "close-up", "wide shot",
                                    "pan", "zoom", "tracking"]):
            department_impact["camera"] += 1
        if any(_contains_keyword(text, k) for k in [
            "light", "lighting", "illumination", "dark",
             "bright", "shadow", "night", "day"]):
            department_impact["lighting"] += 1
        if any(_contains_keyword(text, k) for k in [
            "set", "location", "room", "street", "road",
            "props", "car", "vehicle", "generator"]):
            department_impact["production_design"] += 1
        if any(_contains_keyword(text, k) for k in [
            "costume", "wardrobe", "dress", "shirt", "uniform"]):
            department_impact["costume"] += 1
        if any(_contains_keyword(text, k) for k in [
            "makeup", "hair", "blood", "bruise", "scar"]):
            department_impact["makeup"] += 1
        if any(_contains_keyword(text, k) for k in [
            "stunt", "fight", "action", "chase", "explosion"]):
            department_impact["stunts"] += 1
        if any(_contains_keyword(text, k) for k in [
            "vfx", "visual effect", "cgi", "digital", "green screen"]):
            department_impact["visual_effects"] += 1

    affected = [d for d, c in department_impact.items() if c > 0]
    return {"affected_departments": affected, "impact_counts": department_impact}


# --- Test cases, built from your own demo scenario (Section 16) ---
TEST_CASES = [
    {
        "name": "Location changed to roadside + night",
        "changes": [{"old_lines": ["INT. BEDROOM - DAY"],
                     "new_lines": ["EXT. ROADSIDE - NIGHT"]}],
        "expect_contains": ["lighting", "production_design"],
    },
    {
        "name": "Whisper added",
        "changes": [{"old_lines": ["MAYA speaks normally."],
                     "new_lines": ["MAYA whispers to him."]}],
        "expect_contains": ["sound_continuity"],
    },
    {
        "name": "Generator running nearby",
        "changes": [{"old_lines": [""],
                     "new_lines": ["A generator hums in the background."]}],
        "expect_contains": ["sound_continuity", "production_design"],
    },
    {
        "name": "Phone conversation added",
        "changes": [{"old_lines": [""],
                     "new_lines": ["MAYA answers her phone."]}],
        "expect_contains": ["sound_continuity"],
    },
    {
        "name": "Rain begins",
        "changes": [{"old_lines": [""],
                     "new_lines": ["Rain starts falling heavily."]}],
        "expect_contains": ["sound_continuity"],
    },
    {
        # This is the substring-bug case: "scar" contains "car"
        "name": "BUG CHECK: scar should NOT trigger production_design",
        "changes": [{"old_lines": ["She looks unharmed."],
                     "new_lines": ["She has a scar on her cheek."]}],
        "expect_contains": ["makeup"],
        "expect_absent": ["production_design"],
    },
]

if __name__ == "__main__":
    passed, failed = 0, 0
    for case in TEST_CASES:
        result = classify_affected_departments(case["changes"])
        affected = set(result["affected_departments"])

        missing = [d for d in case.get("expect_contains", []) if d not in affected]
        wrongly_present = [d for d in case.get("expect_absent", []) if d in affected]

        ok = not missing and not wrongly_present
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1

        print(f"[{status}] {case['name']}")
        print(f"    affected: {sorted(affected)}")
        if missing:
            print(f"    MISSING expected: {missing}")
        if wrongly_present:
            print(f"    WRONGLY PRESENT: {wrongly_present}")
        print()

    print(f"Result: {passed} passed, {failed} failed out of {len(TEST_CASES)}")