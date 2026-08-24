from google.adk.agents import Agent  
from script_tools import compare_script_versions 

comparison_agent = Agent(
    name="script_comparison_agent",
    model="gemini-3.6-flash",
    description="Finds differences between two screenplay versions.",
    instruction="Compare the old and revised screenplay and report only supported changes.",
    tools=[compare_script_versions],
)

root_agent = Agent(
    name="revision_impact_agent",
    model="gemini-3.6-flash",
    description="Coordinates screenplay revision analysis.",
    instruction=(
      "Delegate comparison to the relevant specialist and combine the results for human review."
    ),
    sub_agents=[comparison_agent],
)