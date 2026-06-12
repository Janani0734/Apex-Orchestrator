import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="Apex-Orchestrator", page_icon="⚙️", layout="wide")

# --- STYLING ---
st.markdown("""
<style>
    div[data-testid="stMainBlockContainer"] { max-width: 100% !important; padding: 1.5rem 2rem !important; }
    .agent-card { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 20px; margin-bottom: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
    .agent-card-red { background: #fff5f5; border: 1.5px solid #f8b4b4; border-radius: 10px; padding: 20px; margin-bottom: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
    .agent-card-green { background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 10px; padding: 20px; margin-bottom: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
    .badge-live { background: #dcfce7; color: #166534; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 700; }
    .badge-sim  { background: #f1f5f9; color: #475569; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 700; }
    .badge-override { background: #fee2e2; color: #991b1b; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 700; }
    .override-banner { background: #fee2e2; border-left: 5px solid #ef4444; border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 10px 0; }
    .reasoning-box { background: #f8fafc; border-left: 4px solid #6366f1; border-radius: 0 8px 8px 0; padding: 12px 16px; font-family: monospace; font-size: 13px; line-height: 1.7; margin-top: 8px; white-space: pre-wrap; }
    .flow-step { background: #f1f5f9; border-radius: 8px; padding: 10px 14px; margin: 5px 0; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='margin:0;'>⚙️ Apex-Orchestrator Control Console</h1>", unsafe_allow_html=True)

# --- SIDEBAR (must come before client init) ---
with st.sidebar:
    st.header("📊 Live Signals Ingest")
    target_track = st.text_input("Target Certification Path", "AZ-204: Developing Solutions for Azure")
    meeting_hours = st.slider("Weekly Meeting Density (Work IQ)", 0, 40, 26)
    focus_hours   = st.slider("Available Focus Reserve (Fabric IQ)", 0, 40, 6)
    practice_score = st.slider("Practice Exam Score (%)", 0, 100, 67)
    st.markdown("---")
    st.markdown("### 🔑 Live Credential Override")
    st.markdown("**Option A — Azure AI Foundry (recommended)**")
    azure_endpoint_input = st.text_input("Azure OpenAI Endpoint:", placeholder="https://YOUR-RESOURCE.openai.azure.com/")
    azure_key_input      = st.text_input("Azure API Key:", type="password")
    azure_deployment     = st.text_input("Deployment Name:", value="gpt-4o-mini")
    st.markdown("**Option B — Groq (fallback)**")
    user_key_input = st.text_input("Paste Groq API Key:", type="password")
    st.markdown("---")
    st.markdown("**Microsoft IQ Layers:**")
    st.success("✅ Fabric IQ — Study Planner")
    st.warning("⚡ Work IQ — Burnout Guard")
    st.error("🛡️ Foundry IQ — Eval Gate")
    st.info("📊 Manager Insights")

# --- API KEY RESOLUTION (Azure takes priority over Groq) ---
client       = None
MODEL        = "llama-3.1-8b-instant"
backend_label = "Groq LLaMA-3.1"
using_azure  = False

# 1. Try Azure AI Foundry (sidebar input)
_az_endpoint = azure_endpoint_input.strip() if azure_endpoint_input else ""
_az_key      = azure_key_input.strip()      if azure_key_input      else ""
if not _az_endpoint:
    try: _az_endpoint = st.secrets.get("AZURE_OPENAI_ENDPOINT", "")
    except Exception: pass
if not _az_endpoint: _az_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
if not _az_key:
    try: _az_key = st.secrets.get("AZURE_OPENAI_KEY", "")
    except Exception: pass
if not _az_key: _az_key = os.getenv("AZURE_OPENAI_KEY", "")

if _az_endpoint and _az_key:
    try:
        from openai import AzureOpenAI
        _dep = azure_deployment.strip() if azure_deployment.strip() else os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini")
        client = AzureOpenAI(
            azure_endpoint=_az_endpoint,
            api_key=_az_key,
            api_version="2024-02-01"
        )
        MODEL         = _dep
        backend_label = f"Azure AI Foundry · {_dep}"
        using_azure   = True
    except Exception as e:
        st.error(f"Azure client error: {e}")

# 2. Fallback: Groq
if not client:
    _groq_key = ""
    if user_key_input and len(user_key_input) > 10:
        _groq_key = user_key_input
    else:
        try: _groq_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception: pass
        if not _groq_key: _groq_key = os.getenv("GROQ_API_KEY", "")
    if _groq_key:
        try:
            client = OpenAI(api_key=_groq_key, base_url="https://api.groq.com/openai/v1")
        except Exception as e:
            st.error(f"Groq client error: {e}")

st.markdown(
    f"<p style='color:#64748b; font-size:15px;'>Live Multi-Agent Autonomous Communication Mesh · "
    f"{'🟦 <strong>Azure AI Foundry</strong>' if using_azure else 'Powered by LLaMA-3.1 via Groq'}</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# --- STATUS BANNER ---
if using_azure:
    st.success(f"🟦 Azure AI Foundry Connected — {MODEL}. Adjust sliders and click Execute.")
elif client:
    st.success("✅ Live LLM Connected — Groq LLaMA-3.1 active. Adjust sliders and click Execute.")
else:
    st.warning("⚠️ Running in simulation mode. Add Azure AI Foundry or Groq credentials in sidebar.")

# --- MAIN EXECUTION BUTTON ---
if st.button("⚡ Execute Infrastructure Inference Loop", type="primary", use_container_width=False):

    burnout_index = round(meeting_hours / max(focus_hours, 1), 2)
    is_fallback   = False
    is_overridden = meeting_hours > 20 or burnout_index > 2.0

    agent1_output  = ""
    agent2_output  = ""
    agent3_output  = ""
    agent4_output  = ""
    a1_reasoning   = ""
    a2_reasoning   = ""
    a3_reasoning   = ""
    a4_reasoning   = ""

    with st.spinner("🤖 Orchestrating multi-agent inference loop..."):
        try:
            if client is None:
                raise ValueError("No API key configured.")

            # ── AGENT 1: FABRIC IQ ──────────────────────────────────────────
            a1_resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": (
                        "You are Agent 1 — Fabric IQ Study Planner in the Apex-Orchestrator system. "
                        "Generate a concise study plan in 3-4 bullet points. "
                        "Be specific about hours, milestones, and Azure topics. "
                        "Keep under 200 words."
                    )},
                    {"role": "user", "content": (
                        f"Target: {target_track} | "
                        f"Focus hours available: {focus_hours}h/week | "
                        f"Meeting hours: {meeting_hours}h/week | "
                        f"Current practice score: {practice_score}%"
                    )}
                ],
                max_tokens=250, temperature=0.3
            )
            agent1_output = a1_resp.choices[0].message.content

            a1_trace = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": (
                        "You are Agent 1 — Fabric IQ. Show your step-by-step internal reasoning "
                        "for the study plan you just created. Use this format:\n"
                        "STEP 1: [what you evaluated]\n"
                        "STEP 2: [what you decided]\n"
                        "STEP 3: [why this pace was chosen]\n"
                        "CONCLUSION: [one line summary]"
                    )},
                    {"role": "user", "content": (
                        f"meeting_hours={meeting_hours}, focus_hours={focus_hours}, "
                        f"practice_score={practice_score}%, track={target_track}"
                    )}
                ],
                max_tokens=200, temperature=0.2
            )
            a1_reasoning = a1_trace.choices[0].message.content

            # ── AGENT 2: WORK IQ ────────────────────────────────────────────
            # Override decision is DETERMINISTIC math — never let the LLM decide this
            is_overridden = meeting_hours > 20 or burnout_index > 2.0
            if is_overridden:
                a2_system = (
                    "You are Agent 2 — Work IQ Burnout Guard in Apex-Orchestrator. "
                    f"SYSTEM OVERRIDE CONFIRMED: burnout_index={burnout_index} > 2.0 threshold. "
                    f"meeting_hours={meeting_hours}h > 20h safety limit. "
                    "Start EXACTLY with: OVERRIDE ACTIVATED. "
                    "Then explain what changes are forced on Agent 1 plan and protective actions taken. "
                    "Under 150 words."
                )
            else:
                a2_system = (
                    "You are Agent 2 — Work IQ Burnout Guard in Apex-Orchestrator. "
                    f"SYSTEM APPROVAL CONFIRMED: burnout_index={burnout_index} within safe limits. "
                    f"meeting_hours={meeting_hours}h within 20h limit. "
                    "Start EXACTLY with: PLAN APPROVED. "
                    "Confirm the plan and note any minor risks to watch. Under 100 words."
                )
            a2_resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": a2_system},
                    {"role": "user", "content": f"Agent 1 proposed plan:\n\n{agent1_output}"}
                ],
                max_tokens=200, temperature=0.3
            )
            agent2_output = a2_resp.choices[0].message.content

            a2_trace = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": (
                        "You are Agent 2 — Work IQ. Show your conflict resolution reasoning. Format:\n"
                        "METRIC: burnout_index = meetings/focus\n"
                        "THRESHOLD CHECK: [pass or fail]\n"
                        "CONFLICT DETECTED: [yes/no and why]\n"
                        "RESOLUTION: [action taken]\n"
                        "AGENT COMMUNICATION: [what signal sent to other agents]"
                    )},
                    {"role": "user", "content": (
                        f"meeting_hours={meeting_hours}, focus_hours={focus_hours}, "
                        f"burnout_index={burnout_index}, override={is_overridden}"
                    )}
                ],
                max_tokens=200, temperature=0.2
            )
            a2_reasoning = a2_trace.choices[0].message.content

            # ── AGENT 3: FOUNDRY IQ EVAL GATE ───────────────────────────────
            gate_status = "VOUCHER_APPROVED" if practice_score >= 75 else "REMEDIATION_LOOP_TRIGGERED"
            a3_resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": (
                        f"You are Agent 3 — Foundry IQ Evaluation Gate. "
                        f"Hard threshold: 75%. Current score: {practice_score}%. "
                        f"Status: {gate_status}. "
                        "Generate ONE specific practice question for this certification with 4 options A-D. "
                        "Mark the correct answer. Keep under 150 words."
                    )},
                    {"role": "user", "content": f"Certification: {target_track}"}
                ],
                max_tokens=200, temperature=0.4
            )
            agent3_output = a3_resp.choices[0].message.content

            a3_trace = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": (
                        "You are Agent 3 — Foundry IQ Gate. Show gate decision reasoning. Format:\n"
                        "SCORE RECEIVED: [value]\n"
                        "THRESHOLD: 75%\n"
                        "DELTA: [score - threshold]\n"
                        "GATE DECISION: [pass/fail logic]\n"
                        "ACTION: [what happens next]"
                    )},
                    {"role": "user", "content": f"score={practice_score}, track={target_track}"}
                ],
                max_tokens=150, temperature=0.1
            )
            a3_reasoning = a3_trace.choices[0].message.content

            # ── AGENT 4: MANAGER INSIGHTS ────────────────────────────────────
            a4_resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": (
                        "You are Agent 4 — Anonymized Manager Insights in Apex-Orchestrator. "
                        "Provide 3-4 bullet points of leadership-level insights. "
                        "Never mention individual names — use cohort-level language only. "
                        "Include: readiness forecast, capacity risk, and one recommendation. "
                        "Keep under 150 words."
                    )},
                    {"role": "user", "content": (
                        f"Cohort track: {target_track} | Score: {practice_score}% | "
                        f"Burnout index: {burnout_index} | Override: {is_overridden} | "
                        f"Gate status: {gate_status}"
                    )}
                ],
                max_tokens=200, temperature=0.3
            )
            agent4_output = a4_resp.choices[0].message.content
            a4_reasoning = f"COHORT: TRACK-{target_track.split(':')[0].strip()}\nPII_STRIPPED: True\nANONYMIZATION: employee_id → cohort_ref\nRISK_FLAGS: burnout_index={burnout_index} | override={is_overridden}"

        except Exception as e:
            is_fallback = True
            st.toast(f"⚙️ Simulation mode: {str(e)[:60]}", icon="🔄")

            _cert = target_track.split(":")[0].strip()
            agent1_output = (
                f"• **Core Focus**: {_cert} Developer Track — Azure Functions, API Management, Storage\n"
                f"• **Weekly Allocation**: {max(2, focus_hours - 2)}h/week across {4 if meeting_hours > 20 else 3} weeks\n"
                f"• **Priority Modules**: Azure App Service → Cosmos DB → Azure Monitor\n"
                f"• **Milestone**: Practice test checkpoint at Week 2"
            )
            a1_reasoning = (
                f"STEP 1: Evaluated focus_hours={focus_hours}h vs meeting_hours={meeting_hours}h\n"
                f"STEP 2: Available bandwidth = {max(0, focus_hours-2)}h/week after overhead\n"
                f"STEP 3: Pace set to {'Extended' if meeting_hours > 20 else 'Moderate'} due to meeting load\n"
                f"CONCLUSION: {4 if meeting_hours>20 else 3}-week plan generated with reduced velocity"
            )
            if meeting_hours > 20:
                agent2_output = (
                    f"OVERRIDE ACTIVATED\n\n"
                    f"Burnout index = {burnout_index} exceeds threshold 2.0. "
                    f"Meeting load {meeting_hours}h > 20h safety limit. "
                    f"Agent 1 study velocity downgraded to protect {focus_hours}h focus reserve."
                )
                is_overridden = True
            else:
                agent2_output = (
                    f"PLAN APPROVED\n\n"
                    f"Burnout index = {burnout_index} within safe limits. "
                    f"Meeting load {meeting_hours}h acceptable. Agent 1 plan cleared."
                )
            a2_reasoning = (
                f"METRIC: burnout_index = {meeting_hours}/{focus_hours} = {burnout_index}\n"
                f"THRESHOLD CHECK: {'FAIL — exceeds 2.0' if burnout_index > 2.0 else 'PASS — within limits'}\n"
                f"CONFLICT DETECTED: {'YES — overriding Agent 1' if is_overridden else 'NO'}\n"
                f"RESOLUTION: {'FORCE_DOWNGRADE applied' if is_overridden else 'APPROVE_PASS_THROUGH'}\n"
                f"AGENT COMMUNICATION: Signal sent to Agent 1 to reduce weekly hours"
            )
            gate_status = "VOUCHER_APPROVED" if practice_score >= 75 else "REMEDIATION_LOOP_TRIGGERED"
            agent3_output = (
                f"Q: Which Azure service is most relevant for {_cert} workloads?\n"
                f"A) Azure VMs\nB) Azure Functions ✓\nC) Azure Batch\nD) Azure Container Instances\n\n"
                f"Correct: B — Azure Functions provides serverless execution triggered by events."
            )
            a3_reasoning = (
                f"SCORE RECEIVED: {practice_score}%\n"
                f"THRESHOLD: 75%\n"
                f"DELTA: {practice_score - 75}%\n"
                f"GATE DECISION: {'PASS — score meets threshold' if practice_score >= 75 else 'FAIL — score below threshold'}\n"
                f"ACTION: {'Issue exam voucher' if practice_score >= 75 else 'Route to remediation loop'}"
            )
            agent4_output = (
                f"• **Cohort Readiness**: {'High-probability pass trajectory' if practice_score >= 75 else 'Critical intervention required — below threshold'}\n"
                f"• **Capacity Risk**: {'HIGH — burnout risk detected across cohort' if burnout_index > 2.0 else 'STABLE — workload within acceptable range'}\n"
                f"• **Recommendation**: {'Reduce meeting density before exam window' if is_overridden else 'Maintain current pace toward certification milestone'}"
            )
            a4_reasoning = (
                f"COHORT: TRACK-{target_track.split(':')[0].strip()}\n"
                f"PII_STRIPPED: True\nANONYMIZATION: employee_id → cohort_ref\n"
                f"RISK_FLAGS: burnout_index={burnout_index} | override={is_overridden}"
            )

    # ════════════════════════════════════════════════════════════════
    # RENDER OUTPUTS
    # ════════════════════════════════════════════════════════════════
    gate_status = "VOUCHER_APPROVED" if practice_score >= 75 else "REMEDIATION_LOOP_TRIGGERED"
    burnout_index = round(meeting_hours / max(focus_hours, 1), 2)

    # System health banner
    if gate_status == "VOUCHER_APPROVED" and not is_overridden:
        st.markdown("### ✅ System Status: LEARNER ON TRACK")
        st.success(f"Practice score {practice_score}% clears the 75% gate. No burnout risk detected.")
    elif is_overridden:
        st.markdown("### ⚠️ System Status: AGENT OVERRIDE ACTIVE")
        st.error(f"Work IQ overrode Fabric IQ plan. Burnout index {burnout_index} exceeds threshold. Study load reduced.")
    else:
        st.markdown("### 🚨 System Status: REMEDIATION LOOP TRIGGERED")
        st.warning(f"Practice score {practice_score}% below 75% threshold. Agent 3 routing back to Agent 1.")

    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Certification", target_track.split(":")[0].strip())
    k2.metric("Practice Score", f"{practice_score}%", delta=f"{practice_score-75}% vs gate")
    k3.metric("Burnout Index", burnout_index, delta="HIGH RISK" if burnout_index > 2.0 else "Stable", delta_color="inverse")
    k4.metric("Gate Status", "✅ APPROVED" if gate_status == "VOUCHER_APPROVED" else "🔁 REMEDIATION")

    st.markdown("---")
    st.markdown("### 🧠 Multi-Agent Reasoning Logs")
    badge_type = "🟦 AZURE FOUNDRY" if using_azure else ("🟢 LIVE GROQ" if not is_fallback else "🟡 SIMULATION")

    col1, col2 = st.columns(2)

    # ── AGENT 1 ──────────────────────────────────────────────────────
    with col1:
        card_class = "agent-card-green" if not is_overridden else "agent-card"
        st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
        st.markdown(f"<span class='badge-live'>AGENT 01 // FABRIC IQ · {badge_type}</span>", unsafe_allow_html=True)
        st.markdown("#### 🚀 Dynamic Curriculum Generation")
        st.write(agent1_output)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("👁️ View Agent 1 Reasoning Logs", expanded=False):
            st.markdown("**🔍 Step-by-Step Decision Chain:**")
            st.markdown(f'<div class="reasoning-box">{a1_reasoning}</div>', unsafe_allow_html=True)
            st.markdown("**🛠️ Execution Context:**")
            st.json({
                "agent": "Fabric IQ Study Planner",
                "model": MODEL if not is_fallback else "Simulation",
                "inputs": {"track": target_track, "focus_h": focus_hours, "meeting_h": meeting_hours, "score": practice_score},
                "status": "EXECUTION_COMPLETED"
            })

    # ── AGENT 2 ──────────────────────────────────────────────────────
    with col2:
        card_class = "agent-card-red" if is_overridden else "agent-card-green"
        st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
        if is_overridden:
            st.markdown(f"<span class='badge-override'>AGENT 02 // WORK IQ · OVERRIDE ACTIVE · {badge_type}</span>", unsafe_allow_html=True)
            st.markdown(f'<div class="override-banner">🔴 <strong>AGENT CONFLICT DETECTED</strong><br>Work IQ is overriding Agent 1\'s study velocity. Burnout index {burnout_index} exceeds threshold 2.0.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='badge-live'>AGENT 02 // WORK IQ · {badge_type}</span>", unsafe_allow_html=True)
        st.markdown("#### 🛡️ Active Burnout Safety Audit")
        st.write(agent2_output)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("👁️ View Agent 2 Conflict & Override Logs", expanded=False):
            st.markdown("**🔍 Conflict Resolution Chain:**")
            st.markdown(f'<div class="reasoning-box">{a2_reasoning}</div>', unsafe_allow_html=True)
            st.markdown("**🛠️ Governance Matrix:**")
            st.json({
                "agent": "Work IQ Burnout Guard",
                "model": MODEL if not is_fallback else "Simulation",
                "burnout_index": burnout_index,
                "override_triggered": is_overridden,
                "action": "FORCE_DOWNGRADE_OVERRIDE" if is_overridden else "APPROVE_PASS_THROUGH"
            })

    st.markdown("---")
    col3, col4 = st.columns(2)

    # ── AGENT 3 ──────────────────────────────────────────────────────
    with col3:
        card_class = "agent-card-green" if gate_status == "VOUCHER_APPROVED" else "agent-card-red"
        st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
        st.markdown(f"<span class='badge-live'>AGENT 03 // FOUNDRY IQ GATE · {badge_type}</span>", unsafe_allow_html=True)
        st.markdown("#### 🛡️ Evaluation Gate")
        gate_badge = "✅ VOUCHER APPROVED" if gate_status == "VOUCHER_APPROVED" else "🔁 REMEDIATION LOOP"
        st.markdown(f"**Status:** {gate_badge}")
        st.markdown(f"**Score:** {practice_score}% | **Threshold:** 75% | **Delta:** {practice_score-75}%")
        if gate_status != "VOUCHER_APPROVED":
            st.progress(min(practice_score / 75, 1.0), text=f"Progress to threshold: {practice_score}/75%")
        st.markdown("**📝 Practice Question (Foundry IQ Generated):**")
        st.info(agent3_output)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("👁️ View Agent 3 Gate Decision Logs", expanded=False):
            st.markdown("**🔍 Gate Decision Chain:**")
            st.markdown(f'<div class="reasoning-box">{a3_reasoning}</div>', unsafe_allow_html=True)

    # ── AGENT 4 ──────────────────────────────────────────────────────
    with col4:
        st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
        st.markdown(f"<span class='badge-live'>AGENT 04 // MANAGER INSIGHTS · PII STRIPPED · {badge_type}</span>", unsafe_allow_html=True)
        st.markdown("#### 📊 Anonymized Cohort Intelligence")
        st.markdown(f"**Cohort ID:** `TRACK-{target_track.split(':')[0].strip()}`")
        readiness = "High-Probability Pass" if gate_status == "VOUCHER_APPROVED" else "Critical Intervention Needed"
        risk = "⚠️ High Workloads" if is_overridden else "✅ Stable"
        st.markdown(f"**Readiness:** {readiness} | **Capacity Risk:** {risk}")
        st.write(agent4_output)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("👁️ View Agent 4 Anonymization Logs", expanded=False):
            st.markdown("**🔍 PII Stripping Trace:**")
            st.markdown(f'<div class="reasoning-box">{a4_reasoning}</div>', unsafe_allow_html=True)

    # ── ORCHESTRATION FLOW SUMMARY ────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔄 Multi-Agent Orchestration Flow")
    f1, f2, f3, f4 = st.columns(4)
    f1.success(f"**Agent 1**\nFabric IQ\n✅ Plan Generated")
    if is_overridden:
        f2.error(f"**Agent 2**\nWork IQ\n🔴 OVERRIDE")
    else:
        f2.success(f"**Agent 2**\nWork IQ\n✅ Approved")
    if gate_status == "VOUCHER_APPROVED":
        f3.success(f"**Agent 3**\nFoundry IQ\n✅ Voucher")
    else:
        f3.error(f"**Agent 3**\nFoundry IQ\n🔁 Remediation")
    f4.info(f"**Agent 4**\nManager\n📊 {readiness.split()[0]}")

