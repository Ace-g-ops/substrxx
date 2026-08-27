from pydantic import BaseModel, Field
from typing import Literal, Optional
  
class ChangeEntry(BaseModel):
    change_type: Literal["replace", "delete", "insert"]
    old_lines: list[str]
    new_lines: list[str]
    old_line_range: list[int]
    new_line_range: list[int]
 
class ScriptComparisonReport(BaseModel):
    status: Literal["success", "error"]
    error_message: Optional[str] = None
    total_changes: int = 0
    changes: list[ChangeEntry] = []
 
class DepartmentImpactReport(BaseModel):
    affected_departments: list[str]
    impact_counts: dict[str, int]
 
class SoundRisk(BaseModel):
    scene_or_location: str = Field(description="Scene heading or location where the risk occurs.")
    evidence: str = Field(description="Direct script line(s) supporting this finding.")
    requirement_or_risk: str = Field(description="The sound requirement or continuity risk identified.")
    recommended_action: str = Field(description="What the sound department should do about it.")
    confidence: Literal["fact", "assumption"] = Field(
        description="Whether this is directly supported by the script text or inferred."
    )
 
class SoundContinuityReport(BaseModel):
    risks: list[SoundRisk]
    summary: str = Field(description="One or two sentence overview of overall sound impact.")
 
class RevisionImpactReport(BaseModel):
    """What the Replit API layer will ultimately hand back to the frontend."""
    comparison: ScriptComparisonReport
    department_impact: DepartmentImpactReport
    sound_continuity: SoundContinuityReport
 

