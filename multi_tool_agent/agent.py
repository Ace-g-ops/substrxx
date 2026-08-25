from google.adk.agents import Agent  
from google.genai import types
from script_tools import compare_script_versions 
from department_impact_analsyt import classify_affected_departments


comparison_agent = Agent(
    name="script_comparison_agent",
    model="gemini-3.6-flash",
    description="Finds differences between two screenplay versions.",
    instruction="Compare the old and revised screenplay and report only supported changes.",
    tools=[compare_script_versions],
)

classify_affected_department = Agent(
    name="department_impact_agent",
    model="gemini-3.6-flash",
    description="Classifies departments affected by screenplay changes.",
    instruction="Analyze the screenplay changes and classify the affected departments.",
    tools=[classify_affected_departments],
)

sound_continuity_agent = Agent(
    name="sound_continuity_agent",
    model="gemini-3.6-flash",
    description=(
        "Analyses screenplay revisions for sound requirements "
        "and continuity risks."
    ),
    instruction="""
    You are a production sound continuity specialist.

    Analyse the screenplay changes provided to you.

    Identify:
    1. Added, removed, or changed dialogue.
    2. Changes in location, time, weather, or environment. 
    3. Whispering, shouting, off-screen speech, phone calls, and radio calls.
    4. Sound effects such as rain, traffic, vehicles, crowds, generators, and music.
    5. Requirements for room tone, wild tracks, playback, or additional recording.

    For every risk, provide:
    - Scene or location.
    - Relevant script evidence.
    - Sound requirement or risk.
    - Recommended action.
    - Confidence level.

    Do not claim that the final audio will definitely fail.
    Clearly separate facts from assumptions.
    Recommendations must be reviewed by a human.
    """
)

root_agent = Agent(
    name="revision_impact_agent",
    model="gemini-3.5-flash",

    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(initial_delay=1, attempts=2),
        ),
    ),
    description="Coordinates screenplay revision analysis.",
    instruction=(
      "Delegate comparison to the relevant specialist and combine the results for human review."
    ),
    sub_agents=[comparison_agent, sound_continuity_agent, classify_affected_department],
)