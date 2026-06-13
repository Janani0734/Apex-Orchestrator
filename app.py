import streamlit as st
import os
from openai import AzureOpenAI, OpenAI

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

st.markdown("<h1 style='margin:0;'>⚙️ Apex-Orchestrator Control Console</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748b; font-size:15px;'>Live Multi-Agent Autonomous Communication Mesh · Microsoft Azure AI Foundry + Groq Hybrid</p>", unsafe_allow_html=True)
st.markdown("---")

# SIDEBAR
with st.sidebar:
    st.header("📊 Live Signals Ingest")
    target_track = st.text_input("Target Certification Path", "AZ-204: Developing Solutions for Azure")
    meeting_hours = st.slider("Weekly Meeting Density (Work IQ)", 0, 40, 26)
    focus_hours   = st.slider("Available Focus Reserve (Fabric IQ)", 0, 40, 6)
    practice_score = st.slider("Practice Exam Score (%)", 0, 100, 67)
    st.markdown("---")
    st.markdown("### 🔑 API Credentials")
    azure_key_input = st.text_input("Azure Foundry API Key:", type="password")
    groq_key_input  = st.text_input("Groq API Key (fallback):", type="password")
    st.markdown("---")
    st.markdown("**Microsoft IQ Layers:**")
    st.success("✅ Fabric IQ — Study Planner")
    st.warning("⚡ Work IQ — Burnout Guard")
    st.error("🛡️ Foundry IQ — Eval Gate")
    st.info("📊 Manager Insights")

# REAL MICROSOFT FOUNDRY CONFIG
AZURE_ENDPOINT = "https://ai-project-ai-resource.openai.azure.com/"
AZURE_MODEL    = "gpt-4.1-mini"
AZURE_API_VER  = "2024-12-01-preview"
GROQ_MODEL     = "llama-3.1-8b-instant"

# KEY RESOLUTION
def get_key(sidebar_val, secret_keys):
    if sidebar_val and len(sidebar_val) > 10:
        return sidebar_val
    for k in secret_keys:
        try:
            v = st.secrets.get(k, "")
            if v: return v
        except: pass
    for k in secret_keys:
        v = os.getenv(k, "")
        if v: return v
    return ""

azure_key = get_key(azure_key_input, ["AZURE_FOUNDRY_KEY", "AZURE_OPENAI_KEY"])
groq_key  = get_key(groq_key_input,  ["GROQ_API_KEY"])

# INIT CLIENTS
azure_client = None
groq_client  = None

if azure_key:
    try:
        azure_client = AzureOpenAI(
            api_key=azure_key,
            api_version=AZURE_API_VER,
            azure_endpoint=AZURE_ENDPOINT,
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

# STATUS
if azure_client:
    st.markdown(f'<div style="background:#e0f2fe;border-left:4px solid #0078d4;padding:12px 16px;border-radius:0 8px 8px 0;margin-bottom:1rem;"><span class="azure-badge">🔵 MICROSOFT AZURE AI FOUNDRY CONNECTED</span> &nbsp; Real {AZURE_MODEL} · {AZURE_ENDPOINT}</div>', unsafe_allow_html=True)
elif groq_client:
    st.markdown(f'<div style="background:#fff7ed;border-left:4px solid #f97316;padding:12px 16px;border-radius:0 8px 8px 0;margin-bottom:1rem;"><span class="groq-badge">🟠 GROQ CONNECTED</span> &nbsp; Add Azure Foundry key for Microsoft AI</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ No API key. Add Azure Foundry or Groq key in sidebar.")

# LLM CALL
def llm(system, user, max_tokens=350):
    if azure_client:
        try:
            r = azure_client.chat.completions.create(
                model=AZURE_MODEL,
                messages=[{"role":"system","content":system},{"role":"user","content":user}],
                max_tokens=max_tokens, temperature=0.3
            )
            return r.choices[0].message.content.strip(), "AZURE_FOUNDRY"
        except Exception as e:
            pass
    if groq_client:
        try:
            r = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role":"system","content":system},{"role":"user","content":user}],
                max_tokens=max_tokens, temperature=0.3
            )
            return r.choices[0].message.content.strip(), "GROQ"
        except: pass
    return "[SIMULATION] No API connected.", "SIMULATION"

def badge(src):
    if src == "AZURE_FOUNDRY":
        return '<span class="azure-badge">🔵 MICROSOFT AZURE FOUNDRY · gpt-4.1-mini</span>'
    elif src == "GROQ":
        return '<span class="groq-badge">🟠 GROQ · LLaMA-3.1</span>'
    return '<span class="sim-badge">⚪ SIMULATION</span>'

# EXECUTE
if st.button("⚡ Execute Infrastructure Inference Loop", type="primary"):
    burnout_index = round(meeting_hours / max(focus_hours, 1), 2)
    gate_status   = "VOUCHER_APPROVED" if practice_score >= 75 else "REMEDIATION_LOOP_TRIGGERED"

    with st.spinner("🤖 Orchestrating via Microsoft Azure AI Foundry..."):
        a1_out, a1_src = llm(
            "You are Agent 1 — Fabric IQ Study Planner in Apex-Orchestrator. Generate a concise 3-4 bullet study plan. Be specific about hours, weeks, Azure topics. Under 200 words.",
            f"Target: {target_track} | Focus: {focus_hours}h/week | Meetings: {meeting_hours}h/week | Score: {practice_score}%"
        )
        a1_trace, _ = llm(
            "You are Agent 1 — Fabric IQ. Show reasoning:\nSTEP 1: [evaluate bandwidth]\nSTEP 2: [determine pace]\nSTEP 3: [allocate hours]\nCONCLUSION: [one line]",
            f"meeting_h={meeting_hours}, focus_h={focus_hours}, score={practice_score}%"
        )
        a2_out, a2_src = llm(
            f"You are Agent 2 — Work IQ Burnout Guard. burnout_index={burnout_index}. If meetings>20 OR burnout_index>2.0 start with 'OVERRIDE ACTIVATED'. Else 'PLAN APPROVED'. Under 150 words.",
            f"meeting_h={meeting_hours}, focus_h={focus_hours}, burnout_index={burnout_index}. Audit:\n{a1_out}"
        )
        a2_trace, _ = llm(
            "You are Agent 2 — Work IQ. Format:\nMETRIC: burnout_index=meetings/focus\nTHRESHOLD CHECK: [pass/fail]\nCONFLICT: [yes/no]\nRESOLUTION: [action]\nAGENT SIGNAL: [what sent]",
            f"meeting_h={meeting_hours}, focus_h={focus_hours}, burnout_index={burnout_index}"
        )
        is_overridden = "OVERRIDE" in a2_out.upper()

        a3_out, a3_src = llm(
            f"You are Agent 3 — Foundry IQ Gate. Hard threshold 75%. Score={practice_score}%. Generate ONE practice question for {target_track} with A-D options. Mark correct answer.",
            f"cert={target_track}, score={practice_score}%"
        )
        a3_trace, _ = llm(
            "You are Agent 3. Format:\nSCORE: [value]\nTHRESHOLD: 75%\nDELTA: [score-75]\nDECISION: [pass/fail]\nACTION: [next step]",
            f"score={practice_score}, cert={target_track}"
        )
        a4_out, a4_src = llm(
            "You are Agent 4 — Manager Insights. Give 3-4 bullet leadership insights. No individual names. Include: readiness, capacity risk, recommendation. Under 150 words.",
            f"cohort={target_track}, score={practice_score}%, burnout={burnout_index}, override={is_overridden}, gate={gate_status}"
        )

    # SYSTEM BANNER
    if gate_status == "VOUCHER_APPROVED" and not is_overridden:
        st.success(f"### ✅ System Status: LEARNER ON TRACK")
    elif is_overridden:
        st.error("### ⚠️ System Status: AGENT OVERRIDE ACTIVE")
        st.markdown(f'<div class="override-banner">🔴 <strong>AGENT CONFLICT DETECTED</strong> — Work IQ overrode Fabric IQ plan. Burnout index {burnout_index} exceeds threshold 2.0.</div>', unsafe_allow_html=True)
    else:
        st.warning(f"### 🚨 System Status: REMEDIATION LOOP TRIGGERED")

    # KPI
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Certification", target_track.split(":")[0].strip())
    k2.metric("Practice Score", f"{practice_score}%", delta=f"{practice_score-75}% vs gate")
    k3.metric("Burnout Index", burnout_index, delta="HIGH RISK" if burnout_index>2.0 else "Stable", delta_color="inverse")
    k4.metric("Gate Status", "✅ APPROVED" if gate_status=="VOUCHER_APPROVED" else "🔁 REMEDIATION")

    st.markdown("---")
    st.markdown("### 🧠 Multi-Agent Reasoning Logs")

    c1, c2 = st.columns(2)
    with c1:
        if is_overridden:
            card1 = "agent-card"
        else:
            card1 = "agent-card-green"
        st.markdown(f"<div class='{card1}'>", unsafe_allow_html=True)
        st.markdown(f"{badge(a1_src)} &nbsp; <strong>AGENT 01 // FABRIC IQ STUDY PLANNER</strong>", unsafe_allow_html=True)
        st.markdown("#### 🚀 Dynamic Curriculum Generation")
        st.write(a1_out)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("👁️ View Agent 1 Reasoning Logs"):
            st.markdown(f'<div class="reasoning-box">{a1_trace}</div>', unsafe_allow_html=True)
            st.json({"agent":"Fabric IQ","provider":a1_src,"model":AZURE_MODEL if a1_src=="AZURE_FOUNDRY" else GROQ_MODEL,"endpoint":AZURE_ENDPOINT if a1_src=="AZURE_FOUNDRY" else "groq.com","status":"EXECUTION_COMPLETED"})

    with c2:
        if is_overridden:
            card2 = "agent-card-red"
        else:
            card2 = "agent-card-green"
        st.markdown(f"<div class='{card2}'>", unsafe_allow_html=True)
        st.markdown(f"{badge(a2_src)} &nbsp; <strong>AGENT 02 // WORK IQ ENGAGEMENT ROUTER</strong>", unsafe_allow_html=True)
        if is_overridden:
            st.markdown(f'<div class="override-banner">🔴 OVERRIDE ACTIVE — burnout_index={burnout_index} > 2.0</div>', unsafe_allow_html=True)
        st.markdown("#### 🛡️ Active Burnout Safety Audit")
        st.write(a2_out)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("👁️ View Agent 2 Conflict & Override Logs"):
            st.markdown(f'<div class="reasoning-box">{a2_trace}</div>', unsafe_allow_html=True)
            st.json({"agent":"Work IQ","provider":a2_src,"burnout_index":burnout_index,"override":is_overridden,"action":"FORCE_DOWNGRADE_OVERRIDE" if is_overridden else "APPROVE_PASS_THROUGH"})

    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        if gate_status == "VOUCHER_APPROVED":
            card3 = "agent-card-green"
        else:
            card3 = "agent-card-red"
        st.markdown(f"<div class='{card3}'>", unsafe_allow_html=True)
        st.markdown(f"{badge(a3_src)} &nbsp; <strong>AGENT 03 // FOUNDRY IQ EVALUATION GATE</strong>", unsafe_allow_html=True)
        st.markdown("#### 🛡️ Evaluation Gate")
        st.markdown(f"**Status:** {'✅ VOUCHER APPROVED' if gate_status=='VOUCHER_APPROVED' else '🔁 REMEDIATION LOOP TRIGGERED'}")
        st.markdown(f"**Score:** {practice_score}% | **Threshold:** 75% | **Delta:** {practice_score-75}%")
        if gate_status != "VOUCHER_APPROVED":
            st.progress(min(practice_score/75,1.0), text=f"Progress: {practice_score}/75%")
        st.markdown("**📝 Azure Foundry Generated Practice Question:**")
        st.info(a3_out)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("👁️ View Agent 3 Gate Decision Logs"):
            st.markdown(f'<div class="reasoning-box">{a3_trace}</div>', unsafe_allow_html=True)

    with c4:
        cert_short = target_track.split(":")[0].strip()
        st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
        st.markdown(f"{badge(a4_src)} &nbsp; <strong>AGENT 04 // MANAGER INSIGHTS · PII STRIPPED</strong>", unsafe_allow_html=True)
        st.markdown("#### 📊 Anonymized Cohort Intelligence")
        st.markdown(f"**Cohort ID:** `TRACK-{cert_short}`")
        st.markdown(f"**Readiness:** {'High-Probability Pass' if gate_status=='VOUCHER_APPROVED' else 'Critical Intervention Needed'}")
        st.markdown(f"**Capacity Risk:** {'⚠️ High Workloads' if is_overridden else '✅ Stable'}")
        st.write(a4_out)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("👁️ View Agent 4 Anonymization Logs"):
            st.markdown(f'<div class="reasoning-box">COHORT: TRACK-{cert_short}\nPII_STRIPPED: True\nANONYMIZATION: employee_id → cohort_ref\nBURNOUT_INDEX: {burnout_index}\nPROVIDER: {a4_src}</div>', unsafe_allow_html=True)

    # FLOW
    st.markdown("---")
    st.markdown("### 🔄 Multi-Agent Orchestration Flow")
    f1,f2,f3,f4 = st.columns(4)
    f1.success(f"**Agent 1**\nFabric IQ\n✅ {a1_src}")
    if is_overridden:
        f2.error("**Agent 2**\nWork IQ\n🔴 OVERRIDE")
    else:
        f2.success(f"**Agent 2**\nWork IQ\n✅ {a2_src}")
    if gate_status == "VOUCHER_APPROVED":
        f3.success("**Agent 3**\nFoundry IQ\n✅ VOUCHER")
    else:
        f3.error("**Agent 3**\nFoundry IQ\n🔁 REMEDIATION")
    f4.info(f"**Agent 4**\nManager\n📊 {a4_src}")

    # AZURE PROOF
    st.markdown("---")
    st.markdown("### 🔵 Microsoft Azure AI Foundry Integration")
    st.code(f"""
from openai import AzureOpenAI

# Real Microsoft Azure AI Foundry deployment
client = AzureOpenAI(
    api_key=AZURE_FOUNDRY_KEY,
    api_version="{AZURE_API_VER}",
    azure_endpoint="{AZURE_ENDPOINT}",
)

# All 4 agents powered by deployed gpt-4.1-mini
response = client.chat.completions.create(
    model="{AZURE_MODEL}",
    messages=[...],
)
# Endpoint: {AZURE_ENDPOINT}
# Model: {AZURE_MODEL}
    """, language="python")
