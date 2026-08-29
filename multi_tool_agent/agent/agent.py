from google.adk.agents import Agent  
# from google.genai import types
from script_comparison import compare_script_versions
from google.adk.apps.app import App
from google.adk.agents.context_cache_config import ContextCacheConfig
from substrxx_models import SoundContinuityReport
from substrxx_models import DepartmentImpactReport

comparison_agent = Agent(
    name="script_comparison_agent",
    model="gemini-3.6-flash",
    description="Finds differences between two screenplay versions.",
    instruction=(
        "Call compare_script_versions with the two screenplay texts. "
        "Output ONLY the exact JSON object the tool returns, verbatim, "
        "with no markdown, no headers, no bullet points, no summary, "
        "and no text before or after the JSON."
    ),
    tools=[compare_script_versions],
    output_key="comparison"
)

department_impact_agent = Agent(
    name="department_impact_agent",
    model="gemini-3.6-flash",
    description="Classifies departments affected by screenplay changes.",
    instruction=(
        "Call classify_affected_departments with the provided changes. "
        "Output ONLY the exact JSON object the tool returns, verbatim, "
        "with no markdown, no headers, no bullet points, no summary, "
        "and no text before or after the JSON."
    ),
    output_schema =DepartmentImpactReport,
    output_key="department_impact"
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
    """,
    
    output_schema=SoundContinuityReport,
    output_key="sound_continuity",
)

root_agent = Agent(
    name="revision_impact_agent",
    model="gemini-3.6-flash",
    description="Coordinates screenplay revision analysis.",
    instruction=(
      "Delegate comparison to the relevant specialist and combine the results for human review."
    ),
    sub_agents=[comparison_agent, sound_continuity_agent, department_impact_agent],
)

app = App(
    name="revision_impact_app",
    root_agent=root_agent,
    context_cache_config=ContextCacheConfig(
        min_tokens=2048,
        ttl_seconds=600,
        cache_intervals=5,
    ),
)