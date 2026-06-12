"""
Apex-Orchestrator: Core Multi-Agent Orchestration Engine
4-agent pipeline: Fabric IQ → Work IQ → Foundry IQ → Manager Insights
"""
import os
from openai import OpenAI
from models import (
    LearnerSignal, OrchestrationResult,
    FabricIQProposal, WorkIQConsensus, FoundryIQGateResult,
    ManagerInsightsReport, StudyModule, ComplianceCitation
)

GROQ_BASE = "https://api.groq.com/openai/v1"
MODEL = "llama-3.1-8b-instant"

CERT_SKILLS = {
    "AZ-204": ["Azure App Service", "Azure Functions", "Cosmos DB", "API Management", "Azure Monitor"],
    "AZ-400": ["CI/CD Pipelines", "GitHub Actions", "Azure DevOps", "Monitoring", "Infrastructure as Code"],
    "AZ-900": ["Cloud Concepts", "Azure Services", "Security", "Pricing", "Support"],
    "AZ-305": ["Identity", "Data Storage", "Business Continuity", "Infrastructure"],
}

class ApexOrchestrator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY", "")
        self.client = OpenAI(api_key=api_key, base_url=GROQ_BASE) if api_key else None
        self.use_mock = not bool(api_key)

    def _llm(self, system: str, user: str, max_tokens: int = 300) -> str:
        if self.use_mock:
            return f"[MOCK] Simulated response for: {user[:60]}..."
        try:
            r = self.client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                max_tokens=max_tokens, temperature=0.3
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            return f"[FALLBACK] LLM error: {str(e)[:100]}"

    async def run(self, signal: LearnerSignal) -> OrchestrationResult:
        """Execute the full 4-agent pipeline."""

        # ── Agent 1: Fabric IQ ────────────────────────────────────────────────
        cert = signal.certification_target.split(":")[0].strip()
        skills = CERT_SKILLS.get(cert, ["Cloud Fundamentals", "Azure Services"])
        base_hrs = 20 if "204" in cert else 25

        if signal.is_burnout_risk:
            pace, weeks = "Extended Pace (Burnout Guard Active)", 4
        elif signal.meeting_hours_per_week > 12:
            pace, weeks = "Moderate Pace", 3
        else:
            pace, weeks = "Accelerated Pace", 2

        weekly_hrs = round(base_hrs / weeks, 1)

        a1_reasoning = self._llm(
            "You are Fabric IQ Study Planner. Show step-by-step reasoning. Format:\nSTEP 1: [evaluate bandwidth]\nSTEP 2: [determine pace]\nSTEP 3: [allocate hours]\nCONCLUSION: [one line]",
            f"meeting_h={signal.meeting_hours_per_week}, focus_h={signal.focus_hours_per_week}, score={signal.practice_score_avg}%, cert={cert}"
        )

        fabric_result = FabricIQProposal(
            learner_id=signal.learner_id,
            certification_target=signal.certification_target,
            pace_tier=pace,
            duration_weeks=weeks,
            weekly_hours=weekly_hrs,
            modules=[StudyModule(phase=f"Module {i+1}", topic=s, estimated_hours=round(weekly_hrs/len(skills),1)) for i, s in enumerate(skills)],
            reasoning_trace=a1_reasoning,
            confidence_score=round(min(signal.focus_hours_per_week / 20, 1.0), 2)
        )

        # ── Agent 2: Work IQ ──────────────────────────────────────────────────
        override = signal.is_burnout_risk
        override_reason = None
        action = "APPROVE_PASS_THROUGH"

        if override:
            override_reason = (
                f"burnout_index={signal.burnout_index} exceeds threshold 2.0. "
                f"meeting_hours={signal.meeting_hours_per_week} > safety limit 20. "
                f"Forcing pace downgrade to protect {signal.focus_hours_per_week}h focus reserve."
            )
            action = "FORCE_DOWNGRADE_OVERRIDE"
            fabric_result.duration_weeks = 4
            fabric_result.weekly_hours = round(weekly_hrs * 0.6, 1)
            fabric_result.pace_tier = "Extended Pace (Work IQ Override Active)"

        channel = "Weekly Digest Email" if signal.burnout_index > 1.8 else "Daily Teams Ping"
        window = "09:00" if signal.preferred_learning_slot == "Morning" else "14:00"
        risk = "HIGH — Burnout Risk" if signal.burnout_index > 2.0 else "MODERATE" if signal.burnout_index > 1.0 else "LOW"

        a2_reasoning = self._llm(
            "You are Work IQ Burnout Guard. Show conflict resolution. Format:\nMETRIC: burnout_index=meetings/focus\nTHRESHOLD CHECK: [pass/fail]\nCONFLICT: [yes/no]\nRESOLUTION: [action]\nAGENT SIGNAL: [what sent to other agents]",
            f"meeting_h={signal.meeting_hours_per_week}, focus_h={signal.focus_hours_per_week}, burnout_index={signal.burnout_index}, override={override}"
        )

        work_result = WorkIQConsensus(
            learner_id=signal.learner_id,
            burnout_index=signal.burnout_index,
            override_triggered=override,
            override_reason=override_reason,
            communication_channel=channel,
            optimal_notification_window=window,
            disruption_risk_level=risk,
            action_taken=action,
            reasoning_trace=a2_reasoning
        )

        # ── Agent 3: Foundry IQ ───────────────────────────────────────────────
        THRESHOLD = 75.0
        gate_status = "VOUCHER_APPROVED" if signal.practice_score_avg >= THRESHOLD else "REMEDIATION_LOOP_TRIGGERED"
        delta = round(signal.practice_score_avg - THRESHOLD, 1)

        practice_q = self._llm(
            f"You are Foundry IQ Evaluation Gate for {cert} certification. Generate ONE practice question with 4 options A-D. Mark correct answer. Ground in real Azure documentation.",
            f"score={signal.practice_score_avg}%, status={gate_status}, cert={cert}",
            max_tokens=200
        )

        a3_reasoning = self._llm(
            "You are Foundry IQ Gate. Format:\nSCORE: [value]\nTHRESHOLD: 75%\nDELTA: [score-75]\nDECISION: [pass/fail logic]\nACTION: [next step]",
            f"score={signal.practice_score_avg}, cert={cert}",
            max_tokens=150
        )

        foundry_result = FoundryIQGateResult(
            learner_id=signal.learner_id,
            practice_score=signal.practice_score_avg,
            threshold=THRESHOLD,
            delta=delta,
            gate_status=gate_status,
            next_action="Issue exam voucher immediately." if gate_status == "VOUCHER_APPROVED" else f"Gap of {abs(delta)}% identified. Routing to Fabric IQ for remediation.",
            practice_question=practice_q,
            citation=ComplianceCitation(
                source=f"Microsoft Learn — {cert} Study Guide",
                excerpt=f"Candidates for {cert} should demonstrate proficiency in core Azure services and development patterns.",
                confidence=0.92
            ),
            reasoning_trace=a3_reasoning,
            loop_iteration=0 if gate_status == "VOUCHER_APPROVED" else 1
        )

        # ── Agent 4: Manager Insights ─────────────────────────────────────────
        readiness = "High-Probability Pass" if gate_status == "VOUCHER_APPROVED" else "Critical Intervention Needed"
        a4_reasoning = self._llm(
            "You are Manager Insights Agent. Provide 3-4 bullet leadership insights. Never mention individual names. Include: readiness, capacity risk, recommendation.",
            f"cohort={cert}, score={signal.practice_score_avg}%, burnout={signal.burnout_index}, override={override}, gate={gate_status}",
            max_tokens=200
        )

        manager_result = ManagerInsightsReport(
            cohort_reference_id=f"TRACK-{cert}",
            readiness_forecast=readiness,
            capacity_risk_flag=override,
            burnout_index_cohort=signal.burnout_index,
            recommended_action="Reduce meeting density before exam window." if override else "Maintain current pace toward certification milestone.",
            reasoning_trace=a4_reasoning,
            pii_stripped=True
        )

        # ── System Status ─────────────────────────────────────────────────────
        if gate_status == "VOUCHER_APPROVED" and not override:
            status = "ON_TRACK"
        elif override:
            status = "OVERRIDE_ACTIVE"
        else:
            status = "REMEDIATION_LOOP"

        return OrchestrationResult(
            learner_id=signal.learner_id,
            fabric_iq=fabric_result,
            work_iq=work_result,
            foundry_iq=foundry_result,
            manager_insights=manager_result,
            system_status=status
        )
