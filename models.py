"""
Apex-Orchestrator: Pydantic v2 Domain Schemas & Security Validators
Mirrors Microsoft IQ layer contracts with strict type enforcement.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import re

# ── Security: Prompt Injection Blocklist ─────────────────────────────────────
INJECTION_PATTERNS = [
    r"ignore\s+previous",
    r"disregard\s+instructions",
    r"system\s+prompt",
    r"jailbreak",
    r"act\s+as\s+(?:if\s+you\s+are|a)",
    r"forget\s+(?:all\s+)?(?:previous|prior)",
    r"you\s+are\s+now",
    r"new\s+instructions",
    r"override\s+(?:all\s+)?(?:previous|prior|system)",
]

def check_injection(value: str) -> str:
    """Blocks adversarial prompt injection attempts at input layer."""
    lower = value.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lower):
            raise ValueError(
                f"[SECURITY BLOCK] Input rejected: adversarial injection pattern detected. "
                f"HTTP 422 — payload neutralized at input middleware."
            )
    return value

# ── Input Schemas ─────────────────────────────────────────────────────────────
class LearnerSignal(BaseModel):
    """Work IQ telemetry signal for a single enterprise learner."""
    learner_id: str = Field(..., description="Anonymized learner reference ID")
    certification_target: str = Field(..., description="Target Azure certification track")
    meeting_hours_per_week: int = Field(..., ge=0, le=60)
    focus_hours_per_week: int = Field(..., ge=0, le=40)
    practice_score_avg: float = Field(..., ge=0, le=100)
    preferred_learning_slot: str = Field(default="Morning")

    @field_validator("certification_target", "learner_id")
    @classmethod
    def block_injections(cls, v: str) -> str:
        return check_injection(v)

    @property
    def burnout_index(self) -> float:
        return round(self.meeting_hours_per_week / max(self.focus_hours_per_week, 1), 2)

    @property
    def is_burnout_risk(self) -> bool:
        return self.burnout_index > 2.0 or self.meeting_hours_per_week > 20

# ── Fabric IQ Output Schema ───────────────────────────────────────────────────
class StudyModule(BaseModel):
    phase: str
    topic: str
    estimated_hours: float

class FabricIQProposal(BaseModel):
    """Structured output from Fabric IQ Study Planner agent."""
    learner_id: str
    certification_target: str
    pace_tier: str
    duration_weeks: int = Field(..., ge=1, le=12)
    weekly_hours: float
    modules: List[StudyModule]
    reasoning_trace: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)

# ── Work IQ Output Schema ─────────────────────────────────────────────────────
class WorkIQConsensus(BaseModel):
    """Structured output from Work IQ Engagement Router agent."""
    learner_id: str
    burnout_index: float
    override_triggered: bool
    override_reason: Optional[str] = None
    communication_channel: str
    optimal_notification_window: str
    disruption_risk_level: str
    action_taken: str  # APPROVE_PASS_THROUGH or FORCE_DOWNGRADE_OVERRIDE
    reasoning_trace: str

# ── Foundry IQ Output Schema ──────────────────────────────────────────────────
class ComplianceCitation(BaseModel):
    """Grounded citation from Foundry IQ knowledge base."""
    source: str
    excerpt: str
    confidence: float = Field(..., ge=0.0, le=1.0)

class FoundryIQGateResult(BaseModel):
    """Structured output from Foundry IQ Evaluation Gate agent."""
    learner_id: str
    practice_score: float
    threshold: float = 75.0
    delta: float
    gate_status: str  # VOUCHER_APPROVED or REMEDIATION_LOOP_TRIGGERED
    next_action: str
    practice_question: str
    citation: ComplianceCitation
    reasoning_trace: str
    loop_iteration: int = Field(default=0, ge=0)

# ── Manager Insights Output Schema ────────────────────────────────────────────
class ManagerInsightsReport(BaseModel):
    """Anonymized cohort-level intelligence for engineering leadership."""
    cohort_reference_id: str  # PII stripped — no individual identifiers
    readiness_forecast: str
    capacity_risk_flag: bool
    burnout_index_cohort: float
    recommended_action: str
    reasoning_trace: str
    pii_stripped: bool = True

# ── Full Orchestration Response ───────────────────────────────────────────────
class OrchestrationResult(BaseModel):
    """Complete multi-agent pipeline output."""
    learner_id: str
    fabric_iq: FabricIQProposal
    work_iq: WorkIQConsensus
    foundry_iq: FoundryIQGateResult
    manager_insights: ManagerInsightsReport
    system_status: str  # ON_TRACK, OVERRIDE_ACTIVE, REMEDIATION_LOOP
    total_agents_executed: int = 4
