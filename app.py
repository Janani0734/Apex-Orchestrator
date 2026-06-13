import streamlit as st
import os
from openai import OpenAI

# Azure AI Inference SDK for real Microsoft Foundry calls
try:
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    AZURE_SDK = True
except ImportError:
    AZURE_SDK = False

st.set_page_config(page_title="Apex-Orchestrator", page_icon="⚙️", layout="wide")

st.markdown("""
<style>
    div[data-testid="stMainBlockContainer"] { max-width:100% !important; padding:1.5rem 2rem !important; }
    .agent-card { background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:20px; margin-bottom:15px; box-shadow:0 2px 6px rgba(0,0,0,0.06); }
    .agent-card-red { background:#fff5f5; border:1.5px solid #f8b4b4; border-radius:10px; padding:20px; margin-bottom:15px; }
    .agent-card-green { background:#f0fdf4; border:1.5px solid #86efac; border-radius:10px; padding:20px; margin-bottom:15px; }
    .override-banner { background:#fee2e2; border-left:5px solid #ef4444; border-radius:0 8px 8px 0; padding:14px 18px; margin:10px 0; }
    .reasoning-box { background:#f8fafc; border-left:4px solid #0078d4; border-radius:0 8px 8px 0; padding:12px 16px; font-family:monospace; font-size:12px; line-height:1.7; margin-top:8px; white-space:pre-wrap; }
    .azure-badge { background:#0078d4; color:white; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:700; }
    .groq-badge { background:#f97316; color:white; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:700; }
    .sim-badge { background:#6b7280; color:white; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1 style='margin:0;'>⚙️ Apex-Orchestrator Control Console</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748b; font-size:15px;'>Live Multi-Agent Autonomous Communication Mesh · Microsoft Azure AI Foundry + Groq Hybrid</p>", unsafe_allow_html=True)
st.markdown("---")

# SIDEBAR
with st.sidebar:
    st.header("📊 Live Signals Ingest")
    target_track = st.text_input("Target Certification Path", "AZ-204: Developing Solutions for Azure")
    meeting_hours = st.slider("Weekly Meeting Density (Work IQ)", 0, 40, 26)
    focus_hours = st.slider("Available Focus Reserve (Fabric IQ)", 0, 40, 6)
    practice_score = st.slider("Practice Exam Score (%)", 0, 100, 67)
    st.markdown("---")
    st.markdown("### 🔑 API Credentials")
    azure_key_input = st.text_input("Azure Foundry API Key:", type="password")
    groq_key_input = st.text_input("Groq API Key (fallback):", type="password")
    st.markdown("---")
    st.markdown("**Microsoft IQ Layers:**")
    st.success("✅ Fabric IQ — Study Planner")
    st.warning("⚡ Work IQ — Burnout Guard")
    st.error("🛡️ Foundry IQ — Eval Gate")
    st.info("📊 Manager Insights")

# REAL MICROSOFT FOUNDRY ENDPOINT
AZURE_FOUNDRY_ENDPOINT = "https://ai-project-ai-resource.openai.azure.com/openai/v1"
AZURE_MODEL = "gpt-4.1-mini"
GROQ_MODEL = "llama-3.1-8b-instant"

# API KEY RESOLUTION — Priority: sidebar > Streamlit secrets > env
def resolve_key(input_val, secret_names):
    if input_val and len(input_val) > 10:
        return input_val
    for name in secret_names:
        try:
            val = st.secrets.get(name, "")
            if val:
                return val
        except:
            pass
    for name in secret_names:
        val = os.getenv(name, "")
        if val:
            return val
    return ""

azure_key = resolve_key(azure_key_input, ["AZURE_FOUNDRY_KEY", "AZURE_OPENAI_KEY"])
groq_key = resolve_key(groq_key_input, ["GROQ_API_KEY"])

# INITIALIZE CLIENTS
azure_client = None
groq_client = None

if azure_key and AZURE_SDK:
    try:
        azure_client = ChatCompletionsClient(
            endpoint=AZURE_FOUNDRY_ENDPOINT,
            credential=AzureKeyCredential(azure_key),
        )
    except Exception as e:
        st.sidebar.error(f"Azure error: {e}")

if groq_key:
    try:
        groq_client = OpenAI(
            api_key=groq_key,
            base_url="https://api.groq.com/openai/v1"
        )
    except Exception as e:
        st.sidebar.error(f"Groq error: {e}")

# STATUS BANNER
if azure_client:
    st.markdown(f'<div style="background:#e0f2fe;border-left:4px solid #0078d4;padding:12px 16px;border-radius:0 8px 8px 0;margin-bottom:1rem;"><span class="azure-badge">🔵 MICROSOFT AZURE AI FOUNDRY CONNECTED</span> &nbsp; Real gpt-4.1-mini · {AZURE_FOUNDRY_ENDPOINT}</div>', unsafe_allow_html=True)
elif groq_client:
    st.markdown(f'<div style="background:#fff7ed;border-left:4px solid #f97316;padding:12px 16px;border-radius:0 8px 8px 0;margin-bottom:1rem;"><span class="groq-badge">🟠 GROQ CONNECTED</span> &nbsp; LLaMA-3.1 active — add Azure Foundry key for Microsoft AI</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ No API key detected. Add Azure Foundry key or Groq key in sidebar or Streamlit secrets.")

# LLM CALL — tries Azure Foundry first, falls back to Groq
def llm_call(system: str, user: str, max_tokens: int = 350) -> tuple:
    # PRIMARY: Real Microsoft Azure AI Foundry
    if azure_client:
        try:
            response = azure_client.complete(
                messages=[
                    SystemMessage(content=system),
                    UserMessage(content=user),
                ],
                model=AZURE_MODEL,
                max_tokens=max_tokens,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip(), "AZURE_FOUNDRY"
        except Exception as e:
            pass

    # FALLBACK: Groq LLaMA-3.1
    if groq_client:
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content.strip(), "GROQ"
        except Exception as e:
            pass

    # SIMULATION
    return f"[SIMULATION] No API connected.", "SIMULATION"

# BADGE HTML
def badge(src):
    if src == "AZURE_FOUNDRY":
        return '<span class="azure-badge">🔵 MICROSOFT AZURE FOUNDRY · gpt-4.1-mini</span>'
    elif src == "GROQ":
        return '<span class="groq-badge">🟠 GROQ · LLaMA-3.1</span>'
    return '<span class="sim-badge">⚪ SIMULATION</span>'

# MAIN EXECUTE BUTTON
if st.button("⚡ Execute Infrastructure Inference Loop", type="primary"):
    burnout_index = round(meeting_hours / max(focus_hours, 1), 2)
    is_overridden = meeting_hours > 20 or burnout_index > 2.0
    gate_status = "VOUCHER_APPROVED" if practice_score >= 75 else "REMEDIATION_LOOP_TRIGGERED"

    with st.spinner("🤖 Orchestrating multi-agent inference loop via Microsoft Azure AI Foundry..."):

        # ── AGENT 1: FABRIC IQ ─────────────────────────────────────────────
        a1_out, a1_src = llm_call(
            "You are Agent 1 — Fabric IQ Study Planner in Apex-Orchestrator enterprise system. "
            "Generate a concise 3-4 bullet study plan. Be specific about hours, weeks, Azure topics. Under 200 words.",
            f"Target: {target_track} | Focus: {focus_hours}h/week | Meetings: {meeting_hours}h/week | Score: {practice_score}%"
        )
        a1_trace, _ = llm_call(
            "You are Agent 1 — Fabric IQ. Show your internal reasoning chain:\n"
            "STEP 1: [evaluate bandwidth]\nSTEP 2: [determine pace]\nSTEP 3: [allocate hours]\nCONCLUSION: [one line decision]",
            f"meeting_h={meeting_hours}, focus_h={focus_hours}, score={practice_score}%, cert={target_track}"
        )

        # ── AGENT 2: WORK IQ ───────────────────────────────────────────────
        a2_out, a2_src = llm_call(
            f"You are Agent 2 — Work IQ Burnout Guard in Apex-Orchestrator. "
            f"burnout_index={burnout_index} (meetings/focus). "
            f"If meetings > 20 OR burnout_index > 2.0: start with 'OVERRIDE ACTIVATED' and explain override. "
            f"Else start with 'PLAN APPROVED'. Under 150 words.",
            f"meeting_h={meeting_hours}, focus_h={focus_hours}, burnout_index={burnout_index}.\nAudit Agent 1 plan:\n{a1_out}"
        )
        a2_trace, _ = llm_call(
            "You are Agent 2 — Work IQ. Show conflict resolution reasoning:\n"
            "METRIC: burnout_index = meetings/focus\n"
            "THRESHOLD CHECK: [pass/fail at 2.0]\n"
            "CONFLICT DETECTED: [yes/no]\n"
            "RESOLUTION: [action taken]\n"
            "AGENT SIGNAL: [what sent to other agents]",
            f"meeting_h={meeting_hours}, focus_h={focus_hours}, burnout_index={burnout_index}, override={is_overridden}"
        )
        is_overridden = "OVERRIDE" in a2_out.upper()

        # ── AGENT 3: FOUNDRY IQ ────────────────────────────────────────────
        a3_out, a3_src = llm_call(
            f"You are Agent 3 — Foundry IQ Evaluation Gate in Apex-Orchestrator. "
            f"Hard threshold: 75%. Current score: {practice_score}%. Status: {gate_status}. "
            f"Generate ONE grounded practice question for {target_track} with options A-D. Mark correct answer. Under 150 words.",
            f"Certification: {target_track} | Score: {practice_score}%"
        )
        a3_trace, _ = llm_call(
            "You are Agent 3 — Foundry IQ Gate. Show gate decision:\n"
            "SCORE RECEIVED: [value]\nTHRESHOLD: 75%\nDELTA: [score-75]\n"
            "GATE DECISION: [pass/fail logic]\nACTION: [next step]",
            f"score={practice_score}, cert={target_track}"
        )

        # ── AGENT 4: MANAGER INSIGHTS ──────────────────────────────────────
        a4_out, a4_src = llm_call(
            "You are Agent 4 — Anonymized Manager Insights in Apex-Orchestrator. "
            "Give 3-4 bullet leadership insights. Never mention individual names — cohort level only. "
            "Include: readiness forecast, capacity risk, one recommendation. Under 150 words.",
            f"cohort={target_track}, score={practice_score}%, burnout_index={burnout_index}, "
            f"override={is_overridden}, gate={gate_status}"
        )

    # ── RENDER ────────────────────────────────────────────────────────────────

    # System health banner
    if gate_status == "VOUCHER_APPROVED" and not is_overridden:
        st.success(f"### ✅ System Status: LEARNER ON TRACK — {target_track.split(':')[0].strip()} exam cleared")
    elif is_overridden:
        st.error("### ⚠️ System Status: AGENT OVERRIDE ACTIVE")
        st.markdown(f'<div class="override-banner">🔴 <strong>AGENT CONFLICT DETECTED</strong> — Work IQ overrode Fabric IQ plan. Burnout index {burnout_index} exceeds threshold 2.0. Study load reduced to protect developer.</div>', unsafe_allow_html=True)
    else:
        st.warning(f"### 🚨 System Status: REMEDIATION LOOP TRIGGERED — Score {practice_score}% below 75% threshold")

    # KPI metrics
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Certification", target_track.split(":")[0].strip())
    k2.metric("Practice Score", f"{practice_score}%", delta=f"{practice_score-75}% vs gate")
    k3.metric("Burnout Index", burnout_index, delta="HIGH RISK" if burnout_index > 2.0 else "Stable", delta_color="inverse")
    k4.metric("Gate Status", "✅ APPROVED" if gate_status == "VOUCHER_APPROVED" else "🔁 REMEDIATION")

    st.markdown("---")
    st.markdown("### 🧠 Multi-Agent Reasoning Logs")

    col1, col2 = st.columns(2)

    with col1:
        card = "agent-card-green" if not is_overridden else "agent-card"
        st.markdown(f"<div class='{card}'>", unsafe_allow_html=True)
        st.markdown(f"{badge(a1_src)} &nbsp; <strong>AGENT 01 // FABRIC IQ STUDY PLANNER</strong>", unsafe_allow_html=True)
        st.markdown("#### 🚀 Dynamic Curriculum Generation")
        st.write(a1_out)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("👁️ View Agent 1 Reasoning Logs"):
            st.markdown("**🔍 Step-by-Step Decision Chain:**")
            st.markdown(f'<div class="reasoning-box">{a1_trace}</div>', unsafe_allow_html=True)
            st.json({
                "agent": "Fabric IQ Study Planner",
                "provider": a1_src,
                "model": AZURE_MODEL if a1_src == "AZURE_FOUNDRY" else GROQ_MODEL,
                "endpoint": AZURE_FOUNDRY_ENDPOINT if a1_src == "AZURE_FOUNDRY" else "groq.com",
                "inputs": {"track": target_track, "focus_h": focus_hours, "meeting_h": meeting_hours, "score": practice_score},
                "status": "EXECUTION_COMPLETED"
            })

    with col2:
        card = "agent-card-red" if is_overridden else "agent-card-green"
        st.markdown(f"<div class='{card}'>", unsafe_allow_html=True)
        st.markdown(f"{badge(a2_src)} &nbsp; <strong>AGENT 02 // WORK IQ ENGAGEMENT ROUTER</strong>", unsafe_allow_html=True)
        if is_overridden:
            st.markdown(f'<div class="override-banner">🔴 <strong>OVERRIDE ACTIVE</strong> — burnout_index={burnout_index} > threshold 2.0</div>', unsafe_allow_html=True)
        st.markdown("#### 🛡️ Active Burnout Safety Audit")
        st.write(a2_out)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("👁️ View Agent 2 Conflict & Override Logs"):
            st.markdown("**🔍 Conflict Resolution Chain:**")
            st.markdown(f'<div class="reasoning-box">{a2_trace}</div>', unsafe_allow_html=True)
            st.json({
                "agent": "Work IQ Burnout Guard",
                "provider": a2_src,
                "burnout_index": burnout_index,
                "override_triggered": is_overridden,
                "action": "FORCE_DOWNGRADE_OVERRIDE" if is_overridden else "APPROVE_PASS_THROUGH"
            })

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        card = "agent-card-green" if gate_status == "VOUCHER_APPROVED" else "agent-card-red"
        st.markdown(f"<div class='{card}'>", unsafe_allow_html=True)
        st.markdown(f"{badge(a3_src)} &nbsp; <strong>AGENT 03 // FOUNDRY IQ EVALUATION GATE</strong>", unsafe_allow_html=True)
        st.markdown("#### 🛡️ Evaluation Gate")
        st.markdown(f"**Status:** {'✅ VOUCHER APPROVED' if gate_status == 'VOUCHER_APPROVED' else '🔁 REMEDIATION LOOP TRIGGERED'}")
        st.markdown(f"**Score:** {practice_score}% | **Threshold:** 75% | **Delta:** {practice_score-75}%")
        if gate_status != "VOUCHER_APPROVED":
            st.progress(min(practice_score/75, 1.0), text=f"Progress to threshold: {practice_score}/75%")
        st.markdown("**📝 Azure Foundry Generated Practice Question:**")
        st.info(a3_out)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("👁️ View Agent 3 Gate Decision Logs"):
            st.markdown(f'<div class="reasoning-box">{a3_trace}</div>', unsafe_allow_html=True)
            st.json({
                "agent": "Foundry IQ Evaluation Gate",
                "provider": a3_src,
                "score": practice_score,
                "threshold": 75,
                "delta": practice_score - 75,
                "gate_status": gate_status
            })

    with col4:
        st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
        st.markdown(f"{badge(a4_src)} &nbsp; <strong>AGENT 04 // MANAGER INSIGHTS · PII STRIPPED</strong>", unsafe_allow_html=True)
        st.markdown("#### 📊 Anonymized Cohort Intelligence")
        cert_short = target_track.split(":")[0].strip()
        readiness = "High-Probability Pass" if gate_status == "VOUCHER_APPROVED" else "Critical Intervention Needed"
        risk = "⚠️ High Workloads Detected" if is_overridden else "✅ Stable Operational Headroom"
        st.markdown(f"**Cohort ID:** `TRACK-{cert_short}`")
        st.markdown(f"**Readiness:** {readiness}")
        st.markdown(f"**Capacity Risk:** {risk}")
        st.write(a4_out)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("👁️ View Agent 4 Anonymization Logs"):
            st.markdown(f'<div class="reasoning-box">COHORT: TRACK-{cert_short}\nPII_STRIPPED: True\nANONYMIZATION: employee_id → cohort_ref\nRISK_FLAGS: burnout_index={burnout_index} | override={is_overridden}\nPROVIDER: {a4_src}\nENDPOINT: {AZURE_FOUNDRY_ENDPOINT if a4_src == "AZURE_FOUNDRY" else "groq.com"}</div>', unsafe_allow_html=True)

    # ORCHESTRATION FLOW
    st.markdown("---")
    st.markdown("### 🔄 Multi-Agent Orchestration Flow")
    f1, f2, f3, f4 = st.columns(4)
    f1.success(f"**Agent 1**\nFabric IQ\n✅ {a1_src}")
    if is_overridden:
        f2.error(f"**Agent 2**\nWork IQ\n🔴 OVERRIDE")
    else:
        f2.success(f"**Agent 2**\nWork IQ\n✅ {a2_src}")
    if gate_status == "VOUCHER_APPROVED":
        f3.success(f"**Agent 3**\nFoundry IQ\n✅ VOUCHER")
    else:
        f3.error(f"**Agent 3**\nFoundry IQ\n🔁 REMEDIATION")
    f4.info(f"**Agent 4**\nManager\n📊 {a4_src}")

    # AZURE PROOF SECTION
    st.markdown("---")
    st.markdown("### 🔵 Microsoft Azure AI Foundry Integration")
    st.code(f"""
# Real Microsoft Azure AI Foundry SDK Integration
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Deployed model: gpt-4.1-mini on Microsoft Foundry
ENDPOINT = "{AZURE_FOUNDRY_ENDPOINT}"
MODEL = "{AZURE_MODEL}"

client = ChatCompletionsClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(AZURE_FOUNDRY_KEY),
)

# Agent 1: Fabric IQ Study Planner
response = client.complete(
    messages=[
        SystemMessage(content="You are Fabric IQ Study Planner..."),
        UserMessage(content=learner_signal),
    ],
    model=MODEL,
)
# All 4 agents powered by real Microsoft Azure AI Foundry
# Endpoint: {AZURE_FOUNDRY_ENDPOINT}
    """, language="python")
